#!/usr/bin/env python3

import json
from collections import Counter

data_out = []

data = open("raw/trofi.txt", "r").readlines()
data = [
    l.removesuffix(" ./.\n").split("\t")[1:]
    for l in data if l.count("\t") == 2
]
data_out += [
    {"dataset": "trofi", "text_met": None, "text_lit": l[1].replace("\n", " ")}
    for l in data if l[0] == "L"
][:200]
data_out += [
    {"dataset": "trofi", "text_met": l[1].replace("\n", " "), "text_lit": None}
    for l in data if l[0] == "N"
][:200]

data = [
    l.strip() for l in open("raw/fmo.txt", "r").readlines()
    if l.strip() and not l.startswith("###")
]
# and ("#4" in l or not any(l.startswith(x) for x in ["#1", "#2", "#3"]))
data = [data[i * 5:(i + 1) * 5] for i in range(len(data) // 5)]
data_out_fmo = []
for cluster in data:
    sent_met = cluster[0]
    sents_lit = [l.replace("#4", "").strip() for l in cluster if "#4" in l]

    for sent_lit in sents_lit:
        data_out_fmo.append({
            "dataset": "fmo",
            "text_met": sent_met.replace("\n", " "),
            "text_lit": sent_lit.replace("\n", " "),
        })

data_out += data_out_fmo[:200]

open("data/output/dataset.jsonl", "w").write("\n".join([
    json.dumps(o, ensure_ascii=False) for o in data_out
]) + "\n")

print(Counter([
    f'{o["dataset"]}_{o["text_met"] is None}_{o["text_lit"] is None}'
    for o in data_out
]))
