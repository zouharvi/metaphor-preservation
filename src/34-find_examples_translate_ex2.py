#!/usr/bin/env python3

import numpy as np
import json
import argparse

args = argparse.ArgumentParser()
args.add_argument(
    "-i1", "--input1",
    default="data/eval_EVAL/translate_google_cs.jsonl"
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


# texts
data_new1 = [
    json.loads(x) for x in open(args.input1.replace("eval_EVAL", "output"), "r")
]
data_new1 = [x for x in data_new1 if x["dataset"] == "fmo"]
data_src = [
    json.loads(x) for x in open("data/output/dataset.jsonl", "r")
]
data_src = [x for x in data_src if x["dataset"] == "fmo"]

# example 2: literal easier than metaphor?
for i, (s, n1, preserved1) in enumerate(zip(data_src, data_new1, data_preserved1)):
    if preserved1["text_lit"] == "5" and preserved1["text_met"] == "2":
        print("SRC ", s)
        print("NEW1", n1)
        print(preserved1)
        print()