# pip install --upgrade pycantonese

import pycantonese
import sys
import os

def strToJyutping(s):
    seg = pycantonese.characters_to_jyutping(s)
    seg_j_full, canto_dict_c, canto_dict_j = [], [], []
    for s1 in seg:
        seg_j = pycantonese.parse_jyutping(s1[1])
        for i, s2 in enumerate(s1[0]):
            seg_mfa = f"{seg_j[i].onset} {seg_j[i].nucleus}{seg_j[i].tone} {seg_j[i].coda}"
            canto_dict_c.append([s2, seg_mfa])
            canto_dict_j.append([str(seg_j[i]), seg_mfa])
            seg_j_full.append(str(seg_j[i]))

    canto_dict_c = "\n".join(['\t'.join(w) for w in canto_dict_c])
    canto_dict_j = "\n".join(['\t'.join(w) for w in canto_dict_j])
    seg_j_full = "\t".join(seg_j_full)
    return seg_j_full, canto_dict_c, canto_dict_j

if __name__ == "__main__":
    if len(sys.argv) > 0:
        if os.path.exists(sys.argv[1]):
            f1 = open(sys.argv[1], "r", encoding="utf8")
            text = f1.read()
            f1_c_name = os.path.basename(sys.argv[1]).split('.')[0]
            f1_c = open(f"{f1_c_name}_j.txt", "w", encoding="utf8")

            f2_c = open("cantonese_pronunciation_c.dict", "w", encoding="utf8")
            f2_j = open("cantonese_pronunciation.dict", "w", encoding="utf8")

            text_L = text.split("\n")
            for i, s in enumerate(text_L):
                seg_j_full, canto_dict_c, canto_dict_j = strToJyutping(s)
                f1_c.write(seg_j_full)
                f2_c.write("".join(canto_dict_c))
                f2_j.write("".join(canto_dict_j))

                f1_c.write("\n")
                f2_c.write("\n")
                f2_j.write("\n")


        else:
            print("File not exist")



