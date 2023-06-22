#!/usr/bin/env python3

import numpy as np
import json
import argparse

args = argparse.ArgumentParser()
args.add_argument(
    "-i1", "--input1",
    default="data/eval_EVAL/translate_nllb_cs.jsonl"
)
args.add_argument(
    "-i2", "--input2",
    default="data/eval_EVAL/translate_nllb_de.jsonl"
)
args = args.parse_args()

# values1
data_preserved1 = [
    json.loads(x) for x in open(args.input1.replace("EVAL", "preserved_fixed"), "r")
]
data_preserved1 = [x for x in data_preserved1 if x["dataset"] == "fmo"]
data_present1 = [
    json.loads(x) for x in open(args.input1.replace("EVAL", "present_fixed"), "r")
]
data_present1 = [x for x in data_present1 if x["dataset"] == "fmo"]
data_sentsim1 = [
    json.loads(x) for x in open(args.input1.replace("EVAL", "sentsim"), "r")
]
data_sentsim1 = [x for x in data_sentsim1 if x["dataset"] == "fmo"]

# values2
data_preserved2 = [
    json.loads(x) for x in open(args.input2.replace("EVAL", "preserved_fixed"), "r")
]
data_preserved2 = [x for x in data_preserved2 if x["dataset"] == "fmo"]
data_present2 = [
    json.loads(x) for x in open(args.input2.replace("EVAL", "present_fixed"), "r")
]
data_present2 = [x for x in data_present2 if x["dataset"] == "fmo"]
data_sentsim2 = [
    json.loads(x) for x in open(args.input2.replace("EVAL", "sentsim"), "r")
]
data_sentsim2 = [x for x in data_sentsim2 if x["dataset"] == "fmo"]

# texts
data_new1 = [
    json.loads(x) for x in open(args.input1.replace("eval_EVAL", "output"), "r")
]
data_new1 = [x for x in data_new1 if x["dataset"] == "fmo"]
data_new2 = [
    json.loads(x) for x in open(args.input2.replace("eval_EVAL", "output"), "r")
]
data_new2 = [x for x in data_new2 if x["dataset"] == "fmo"]
data_src = [
    json.loads(x) for x in open("data/output/dataset.jsonl", "r")
]
data_src = [x for x in data_src if x["dataset"] == "fmo"]

# example 1: Czech easier than German?
for i, (s, n1, preserved1, n2, preserved2) in enumerate(zip(data_src, data_new1, data_preserved1, data_new2, data_preserved2)):
    if preserved1["text_met"] == "4" and preserved2["text_met"] == "1":
        print("SRC ", s)
        print("NEW1", n1)
        print(preserved1)
        print("NEW2", n2)
        print(preserved2)
        print("PRES1", data_present1[i])
        print("PRES2", data_present2[i])
        print()