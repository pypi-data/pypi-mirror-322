from collections import defaultdict


def filter_results(res_haps, extra_gl):
    """
    Filter the result to the ones consistent with the extra_gl.
    res_muugs: dictionary:
    {
        'MaxProb': 1.2370678464000013e-16,
        'Haps': {'A*01:01+A*33:03^B*08:01+B*44:03^C*07:01+C*07:01^DQB1*02:01+DQB1*02:01^DRB1*03:01+DRB1*07:01': 1.5523456571675956e-16},
        'Pops': {'CAU,CAU': 1.5523456571675956e-16}
    }
    res_haps: dictionary:
    {
        'MaxProb': 1.2370678464000013e-16,
        'Haps': [['A*01:01~B*08:01~C*07:01~DQB1*02:01~DRB1*03:01', 'A*33:03~B*44:03~C*07:01~DQB1*02:01~DRB1*07:01'],
                 ['A*33:03~B*08:01~C*07:01~DQB1*02:01~DRB1*03:01', 'A*01:01~B*44:03~C*07:01~DQB1*02:01~DRB1*07:01'],
                 ['A*01:01~B*44:03~C*07:01~DQB1*02:01~DRB1*03:01', 'A*33:03~B*08:01~C*07:01~DQB1*02:01~DRB1*07:01'],
                 ['A*33:03~B*44:03~C*07:01~DQB1*02:01~DRB1*03:01', 'A*01:01~B*08:01~C*07:01~DQB1*02:01~DRB1*07:01']],
        'Probs': [1.2370678464000013e-16, 2.990312032960011e-17, 3.0052635931248134e-22, 1.6243602208000046e-18],
        'Pops': [['CAU', 'CAU'], ['CAU', 'CAU'], ['CAU', 'CAU'], ['CAU', 'CAU']]
    }
    Extra GL:  C*07:01+C*07:01^DQB1*02:01+DQB1*02:01
    Short GL:  A*01:01+A*33:03^B*08:01+B*44:03^DRB1*03:01+DRB1*07:01
    """

    split_extra_gl_into_locus = extra_gl.split("^")

    dct = {locus.split("*")[0]: [set(locus.split("+")[0].split("/")), set(locus.split("+")[1].split("/"))]
           for locus in split_extra_gl_into_locus}

    haps = res_haps["Haps"]
    filter_idx = []
    for idx, pair in enumerate(haps):
        check = True
        hap1, hap2 = pair[0], pair[1]
        for allele1, allele2 in zip(hap1.split("~"), hap2.split("~")):
            loc = allele1.split("*")[0]
            if loc in dct:
                if not ((allele1 in dct[loc][0] and allele2 in dct[loc][1]) or (
                        allele1 in dct[loc][1] and allele2 in dct[loc][0])):
                    check = False
                    break
        if check:
            filter_idx.append(idx)
    res_haps["Haps"] = [res_haps["Haps"][idx] for idx in filter_idx]
    res_haps["Probs"] = [res_haps["Probs"][idx] for idx in filter_idx]
    res_haps["Pops"] = [res_haps["Pops"][idx] for idx in filter_idx]
    if not res_haps["Probs"]:
        return {"Haps": [], "Probs": [], "Pops": []}

    return res_haps


def create_subject_dict(file_path):
    subject_dict = {}

    # Open and read the file
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            subject_id = line.split(',', 1)[0]

            if subject_id not in subject_dict:
                subject_dict[subject_id] = []

            subject_dict[subject_id].append(line)

    return subject_dict

def create_haps(path_pmug):
    subject_dict = create_subject_dict(path_pmug)
    all_haps = {"subject_id": [], "res_haps": []}

    for idx, id in enumerate(subject_dict.keys()):
        res_haps = {"Haps": [], "Probs": [], "Pops": []}
        rows = subject_dict[id]
        for row in rows:
            row = row.split(',')
            pair1 = str(row[1]).split(';')
            haps1, pops1 = pair1[0], pair1[1]
            pair2 = str(row[2]).split(';')
            haps2, pops2 = pair2[0], pair2[1]
            prob = float(row[3])

            res_haps["Haps"].append([haps1, haps2])
            res_haps["Pops"].append([pops1, pops2])
            res_haps["Probs"].append(prob)

        all_haps["subject_id"].append(id)
        all_haps["res_haps"].append(res_haps)

    return all_haps

def is_subarray_unordered(large_array, small_array):
    # Convert arrays to sets
    set_large = set(large_array)
    set_small = set(small_array)

    # Check if all elements of small_array are in large_array
    return set_small.issubset(set_large)

def write_best_hap_race_pairs(name_gl, haps, pops, probs, fout, numOfReasults):
    all_res = []

    for i in range(len(probs)):
        pair = haps[i][0] + ";" + pops[i][0] + "," + haps[i][1] + ";" + pops[i][1]
        all_res.append([probs[i], pair])
    all_res.sort(key=lambda x: x[0], reverse=True)
    # write the output to file
    minBestResult = min(numOfReasults,len(all_res))
    for k in range(minBestResult):
        fout.write(
            name_gl
            + ","
            + str(all_res[k][1])
            + ","
            + str(all_res[k][0])
            + ","
            + str(k)
            + "\n"
        )
def write_best_prob(name_gl, res, probs, fout,number_of_pop_results ,sign=","):
    sumProbsDict = defaultdict(list)
    # loop over the result and sum the prob by populations/haplotype
    for k in range(len(res)):
        key = res[k][0] + sign + res[k][1]
        if key in sumProbsDict:
            sumProb = probs[k] + sumProbsDict[key]
            sumProbsDict[key] = sumProb
        else:
            key2 = res[k][1] + sign + res[k][0]
            if key2 in sumProbsDict:
                sumProb = probs[k] + sumProbsDict[key2]
                sumProbsDict[key2] = sumProb
            else:
                sumProbsDict[key] = probs[k]


    multProbs = []
    for k in sumProbsDict:
        multProbs.append([sumProbsDict[k], [k, sumProbsDict[k]]])

    multProbs.sort(key=lambda x: x[0], reverse=True)

    # write the output to file
    minBestResult =min(len(multProbs),number_of_pop_results)
    for k in range(minBestResult):
        fout.write(
            name_gl
            + ","
            + str(multProbs[k][1][0])
            + ","
            + str(multProbs[k][0])
            + ","
            + str(k)
            + "\n"
        )

def write_umug(id,res_haps,fout,numOfResults):

    res_muugs = {}
    for idx ,hap in enumerate(res_haps["Haps"]):
        hap1,hap2 = res_haps["Haps"][idx][0], res_haps["Haps"][idx][1]
        prob = res_haps["Probs"][idx]
        haps = []
        haps.append(hap1.split('~'))
        haps.append(hap2.split('~'))
        muug = ""
        for i in range(len(haps[0])):
            sort_hap = sorted([haps[0][i], haps[1][i]])
            muug += sort_hap[0] + "+" + sort_hap[1] + "^"
        muug = muug[:-1]
        if muug in res_muugs.keys():
            res_muugs[muug] += prob
        else:
            res_muugs[muug] = prob
    pairs = []
    for key in res_muugs.keys():
        pairs.append((key, res_muugs[key]))
    pairs = sorted(pairs, key=lambda x: x[1], reverse=True)
    minResults = min(numOfResults,len(pairs))
    for k in range(minResults):
        fout.write(
            id
            + ","
            + str(pairs[k][0])
            + ","
            + str(pairs[k][1])
            + ","
            + str(k)
            + "\n"
        )

def write_umug_pops(id,res_haps,fout,numOfResults):
    res_muugs = {}
    for idx,pop in enumerate(res_haps["Haps"]):
        pop1,pop2 = res_haps["Pops"][idx][0], res_haps["Pops"][idx][1]
        prob = res_haps["Probs"][idx]
        pops = [pop1,pop2]
        pops = sorted(pops)
        muug = pops[0]+','+pops[1]
        if muug in res_muugs.keys():
            res_muugs[muug] += prob
        else:
            res_muugs[muug] = prob
    pairs = []
    for key in res_muugs.keys():
        pairs.append((key, res_muugs[key]))
    pairs = sorted(pairs, key=lambda x: x[1], reverse=True)
    minResults = min(numOfResults,len(pairs))
    for k in range(minResults):
        fout.write(
            id
            + ","
            + str(pairs[k][0])
            + ","
            + str(pairs[k][1])
            + ","
            + str(k)
            + "\n"
        )

def write_filter(subject_id,res_haps,fout_hap_haplo,fout_pop_haplo,fout_hap_muug,fout_pop_muug,number_of_results,number_of_pop_results,MUUG_output,haps_output):
    haps = res_haps["Haps"]
    probs = res_haps["Probs"]
    pops = res_haps["Pops"]
    if haps_output:
        write_best_hap_race_pairs(
            subject_id,
            haps,
            pops,
            probs,
            fout_hap_haplo,
            number_of_results
        )
        write_best_prob(subject_id, pops, probs, fout_pop_haplo,1)
    if MUUG_output:
        write_umug(subject_id,res_haps,fout_hap_muug,number_of_results)
        write_umug_pops(subject_id,res_haps,fout_pop_muug,number_of_pop_results)


def change_output_by_extra_gl(config,gls,path_pmug,path_umug,path_umug_pops,path_pmug_pops,path_miss):
    res_haps = create_haps(path_pmug)
    all_data = {"subject_id": [], "res_haps": [], "extra_gl": [], "short_gl": []}

    if is_subarray_unordered(gls["subject_id"],res_haps["subject_id"]):
        ids= []
        haps = []
        extras = []
        shorts = []
        for idx,id in enumerate(res_haps["subject_id"]):
            ids.append(id)
            haps.append(res_haps["res_haps"][idx])
            gl_idx = gls["subject_id"].index(id)
            extras.append(gls["extra_gl"][gl_idx])
            shorts.append(gls["short_gl"][gl_idx])
        all_data["subject_id"] = ids
        all_data["res_haps"] = haps
        all_data["extra_gl"] = extras
        all_data["short_gl"] = shorts
    else:
        print("error we got umug has ids that are not form the gls")

    MUUG_output = config["output_MUUG"]
    haps_output = config["output_haplotypes"]
    number_of_results = config["number_of_results"]
    number_of_pop_results = config["number_of_pop_results"]

    fout_hap_haplo,fout_pop_haplo,fout_hap_muug,fout_pop_muug ="","","",""

    if haps_output:
        fout_hap_haplo = open(path_pmug, "w")
        fout_pop_haplo = open(path_pmug_pops,"w")
    if MUUG_output:
        fout_hap_muug = open(path_umug,"w")
        fout_pop_muug = open(path_umug_pops,"w")
    miss = open(path_miss,"a")

    for idx,id in enumerate(all_data["subject_id"]):
        subject_id =  id
        res_haps = all_data["res_haps"][idx]
        extra_gl = all_data["extra_gl"][idx]

        if len(extra_gl) > 0:
            res_haps = filter_results(res_haps, extra_gl)

        if len(res_haps["Haps"]) == 0 :
            gl_idx = gls["subject_id"].index(subject_id)
            miss.write(str(gl_idx) + "," + str(subject_id) + "\n")
        else:
            write_filter(subject_id, res_haps, fout_hap_haplo, fout_pop_haplo, fout_hap_muug, fout_pop_muug,number_of_results,number_of_pop_results,MUUG_output,haps_output)

    if MUUG_output:
        fout_hap_muug.close()
        fout_pop_muug.close()
    if haps_output:
        fout_hap_haplo.close()
        fout_pop_haplo.close()
    miss.close()