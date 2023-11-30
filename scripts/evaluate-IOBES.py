import sys

from src.util.type import Util

def print_result(p, r, f):
    print("Precision: "+str(p))
    print("Recall: "+str(r))
    print("F1: "+str(f))

def print_p_r_f(tp, tp_inexact, total_g, total_p):
    p = tp / total_p
    r = tp / total_g
    f1 = (2*p*r)/(p+r)
    print("Exact match scores:")
    print_result(p, r, f1)
    p_inexact = tp_inexact / total_p
    r_inexact = tp_inexact / total_g
    f1_inexact = (2*p_inexact*r_inexact)/(p_inexact+r_inexact)
    print("Inexact match scores:")
    print_result(p_inexact, r_inexact, f1_inexact)
    return p, r, p_inexact, r_inexact

def print_p_r_f_macro(tp_d, tp_inexact_d, total_g_d, total_p_d):
    p = 0
    r = 0
    p_inexact = 0
    r_inexact = 0
    total_entities = 0
    p_overall = 0
    r_overall = 0
    p_inexact_overall = 0
    r_inexact_overall = 0
    for type in total_g_d.keys():
        total_entities = total_entities + 1
        tp = tp_d[type]
        tp_inexact = tp_inexact_d[type]
        total_g = total_g_d[type]
        total_p = total_p_d[type]
        type = Util.type_acronym_expansion(type)
        print("For "+type)
        p, r, p_inexact, r_inexact = print_p_r_f(tp, tp_inexact, total_g, total_p)
        print()
        p_overall = p_overall + p
        r_overall = r_overall + r
        p_inexact_overall = p_inexact_overall + p_inexact
        r_inexact_overall = r_inexact_overall + r_inexact

    #average scores
    avg_p = p_overall/total_entities
    avg_r = r_overall/total_entities
    avg_f1 = (2*avg_p*avg_r)/(avg_p+avg_r)
    print("Exact match macro scores:")
    print_result(avg_p, avg_r, avg_f1)
    avg_p = p_inexact_overall/total_entities
    avg_r = r_inexact_overall/total_entities
    avg_f1 = (2*avg_p*avg_r)/(avg_p+avg_r)    
    print("Inexact match scores:")
    print_result(avg_p, avg_r, avg_f1)


def dict_add(key, dict_inst):
    if key in dict_inst.keys():
        count = dict_inst[key]
        count = count+1
        dict_inst[key] = count
    else:
        dict_inst[key] = 1
    return dict_inst

def compute_matches(lines_p, lines_g):
    tp = 0
    tp_d = {}
    tp_inexact = 0
    tp_inexact_d = {}
    total_g = 0
    total_g_d = {}
    total_p = 0
    total_p_d = {}
    i = 0

    while i < len(lines_p):
        
        line_p = lines_p[i].strip() 
        line_g = lines_g[i].strip()

        if line_p == "" and line_g == "":
            i = i + 1
            continue

        toks_p = line_p.split()
        #if not len(toks_p) >= 2:
        #    print("predict: "+line_p)
        toks_g = line_g.split("\t")
        if not len(toks_g) >= 2:
            print("gold: "+line_g)

        if "O" in toks_g[len(toks_g)-1]:
            if "S" in toks_p[len(toks_p)-1] or "B" in toks_p[len(toks_p)-1]:
                total_p = total_p + 1
                type_p = toks_p[len(toks_p)-1].split("-")[1]
                total_p_d = dict_add(type_p, total_p_d)
            i = i + 1
            continue

        if not len(toks_g[len(toks_g)-1].split("-")) == 2:
            print("gold: "+line_g)        
        type_g = toks_g[len(toks_g)-1].split("-")[1]

        if "B-" in toks_g[len(toks_g)-1] or "S-" in toks_g[len(toks_g)-1]:
            total_g = total_g + 1
            total_g_d = dict_add(type_g, total_g_d)

        if "O" in toks_p[len(toks_p)-1]:
            i = i + 1
            continue        

        if not len(toks_p[len(toks_p)-1].split("-")) == 2:
            print("predict: "+line_p)
        type_p = toks_p[len(toks_p)-1].split("-")[1]


        if "B-" in toks_p[len(toks_p)-1] or "S-" in toks_p[len(toks_p)-1]:
            total_p = total_p + 1
            total_p_d = dict_add(type_p, total_p_d)

        if ("S-" in toks_g[len(toks_g)-1] and "S-" in toks_p[len(toks_p)-1]) and (type_p == type_g):
            tp = tp + 1
            tp_d = dict_add(type_p, tp_d)
            tp_inexact = tp_inexact + 1
            tp_inexact_d = dict_add(type_p, tp_inexact_d)
        elif "B-" in toks_p[len(toks_p)-1]:         
            if "B-" in toks_g[len(toks_g)-1]:
                if type_p == type_g:
                    tp_inexact = tp_inexact+1
                    tp_inexact_d = dict_add(type_p, tp_inexact_d)
                    i = i + 1
                    while i < len(lines_p):
                        line_p = lines_p[i].strip()
                        line_g = lines_g[i].strip()
                        toks_p = line_p.split()
                        toks_g = line_g.split("\t")
                        if "O" in toks_p[len(toks_p)-1]:
                            break
                        elif "E" in toks_g[len(toks_g)-1]:
                            type_p = toks_p[len(toks_p)-1].split("-")[1]
                            type_g = toks_g[len(toks_g)-1].split("-")[1]                            
                            if type_g == type_p:
                                if "E" in toks_p[len(toks_p)-1]:
                                    tp = tp+1
                                    tp_d = dict_add(type_p, tp_d)
                                elif "I" in toks_p[len(toks_p)-1]:
                                    tp_inexact = tp_inexact-1
                            break
                        elif "B" in toks_p[len(toks_p)-1] or "S" in toks_p[len(toks_p)-1]:
                            i = i - 1
                            break                        

                        i = i + 1
            elif "I-" in toks_g[len(toks_g)-1]:
                if type_p == type_g:
                    tp_inexact = tp_inexact+1
                    tp_inexact_d = dict_add(type_p, tp_inexact_d)
                    i = i + 1
                    while i < len(lines_p):
                        line_p = lines_p[i].strip()
                        line_g = lines_g[i].strip()
                        toks_p = line_p.split()
                        toks_g = line_g.split("\t")
                        if "O" in toks_p[len(toks_p)-1]:
                            break
                        elif "E" in toks_g[len(toks_g)-1]:
                            type_p = toks_p[len(toks_p)-1].split("-")[1]
                            type_g = toks_g[len(toks_g)-1].split("-")[1]                            
                            if type_g == type_p:
                                if "I" in toks_p[len(toks_p)-1]:
                                    tp_inexact = tp_inexact-1
                            break
                        elif "B" in toks_p[len(toks_p)-1] or "S" in toks_p[len(toks_p)-1]:
                            i = i - 1
                            break                        

                        i = i + 1                              

        i = i + 1
        
    return tp, tp_inexact, total_g, total_p, tp_d, tp_inexact_d, total_g_d, total_p_d


def main(file_p, file_g):
    #_p used for predictions
    #_g used for gold-standard data
    #[file_p, file_g] = argv

    fi_p = open(file_p, 'r', encoding='utf-8')
    lines_p = fi_p.readlines()
    fi_g = open(file_g, 'r', encoding='utf-8')
    lines_g = fi_g.readlines()

    assert lines_p == lines_g, 'number of lines in the predictions file and gold data file should be equal.'

    tp, tp_inexact, total_g, total_p, tp_d, tp_inexact_d, total_g_d, total_p_d = compute_matches(lines_p, lines_g)
    print("--------------------------")
    print("Micro scores:")
    print("--------------------------")
    print_p_r_f(tp, tp_inexact, total_g, total_p)

    print()
    print("--------------------------")
    print("Per-type and macro scores:")
    print("--------------------------")
    print()
    print_p_r_f_macro(tp_d, tp_inexact_d, total_g_d, total_p_d)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
