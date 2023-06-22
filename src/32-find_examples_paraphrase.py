#!/usr/bin/env python3

import numpy as np
import json
import argparse

args = argparse.ArgumentParser()
args.add_argument(
    "-i1", "--input1",
    default="data/eval_EVAL/paraphrase_pegasus.jsonl"
)
args.add_argument(
    "-i2", "--input2",
    default="data/eval_EVAL/paraphrase_parrot.jsonl"
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

# example 1: high lit preservation, low met preservation
for s, n, preserved in zip(data_src, data_new1, data_preserved1):
    if preserved["text_lit"] == "5" and preserved["text_met"] == "2":
        print("SRC", s)
        print("NEW", n)
        print(preserved)
        print()

# example 2: high difference
for s, n1, preserved1, n2, preserved2 in zip(data_src, data_new1, data_preserved1, data_new2, data_preserved2):
    if n1["text_met"] == s["text_met"] or n2["text_met"] == s["text_met"]:
        continue
    if preserved1["text_met"] == "2" and preserved2["text_met"] == "5":
        print("SRC ", s)
        print("NEW1", n1)
        print(preserved1)
        print("NEW2", n2)
        print(preserved2)
        print()

# example 2: high difference
for s, n1, preserved1, n2, preserved2 in zip(data_src, data_new1, data_sentsim1, data_new2, data_sentsim2):
    if n1["text_met"].strip(".") == s["text_met"] or n2["text_met"].strip(".") == s["text_met"]:
        continue
    if preserved1["text_met"] < preserved2["text_met"] - 0.3:
        print("SRC ", s)
        print("NEW1", n1)
        print(preserved1)
        print("NEW2", n2)
        print(preserved2)
        print()