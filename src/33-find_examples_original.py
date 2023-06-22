#!/usr/bin/env python3

import numpy as np
import json
import argparse

args = argparse.ArgumentParser()
args.add_argument(
    "-i1", "--input1",
    default="data/eval_EVAL/paraphrase_pegasus.jsonl"
)
args = args.parse_args()

# values1
# data_preserved1 = [
#     json.loads(x) for x in open("data/eval_preserved_fixed/dataset.jsonl", "r")
# ]
# data_preserved1 = [x for x in data_preserved1 if x["dataset"] == "fmo"]
data_present1 = [
    json.loads(x) for x in open("data/eval_present_fixed/dataset.jsonl", "r")
]
data_present1 = [x for x in data_present1 if x["dataset"] == "fmo"]
# data_sentsim1 = [
#     json.loads(x) for x in open("data/eval_sentsim/dataset.jsonl", "r")
# ]
# data_sentsim1 = [x for x in data_sentsim1 if x["dataset"] == "fmo"]


# texts
data_src = [
    json.loads(x) for x in open("data/output/dataset.jsonl", "r")
]
data_src = [x for x in data_src if x["dataset"] == "fmo"]

print(data_present1)

# example 0
for s, values in zip(data_src, data_present1):
    if values["text_lit"] == "5" and values["text_met"] == "1":
        print("SRC", s)
        print(values)
        print()
