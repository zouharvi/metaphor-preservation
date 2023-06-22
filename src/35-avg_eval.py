#!/usr/bin/env python3

import numpy as np
import json
import argparse

args = argparse.ArgumentParser()
args.add_argument(
    "-i1", "--input1",
    default="data/eval_EVAL/paraphrase_bart.jsonl"
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

print(np.average([float(x["text_lit"]) for x in data_preserved1]))
print(np.average([float(x["text_met"]) for x in data_preserved1]))