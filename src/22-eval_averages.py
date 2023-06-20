#!/usr/bin/env python3

import json
import numpy as np

data = [json.loads(x) for x in open("data/eval_present/dataset.jsonl", "r")]

trofi_lit_vals = [float(x["text_lit"]) for x in data if x["dataset"]=="trofi" and x["text_lit"]]
trofi_met_vals = [float(x["text_met"]) for x in data if x["dataset"]=="trofi" and x["text_met"]]
fmo_lit_vals = [float(x["text_lit"]) for x in data if x["dataset"]=="fmo"]
fmo_met_vals = [float(x["text_met"]) for x in data if x["dataset"]=="fmo"]
fmo_met_geq_lit = [float(x["text_met"]) >= float(x["text_lit"]) for x in data if x["dataset"]=="fmo"]
fmo_met_gt_lit = [float(x["text_met"]) > float(x["text_lit"]) for x in data if x["dataset"]=="fmo"]
fmo_met_eq_lit = [float(x["text_met"]) == float(x["text_lit"]) for x in data if x["dataset"]=="fmo"]

print(f"Trofi LIT avg: {np.average(trofi_lit_vals):.2f}")
print(f"Trofi MET avg: {np.average(trofi_met_vals):.2f}")
print(f"FMO LIT avg: {np.average(fmo_lit_vals):.2f}")
print(f"FMO MET avg: {np.average(fmo_met_vals):.2f}")
print(f"FMO MET>=LIT: {np.average(fmo_met_geq_lit):.2%}")
print(f"FMO MET>LIT: {np.average(fmo_met_gt_lit):.2%}")
print(f"FMO MET=LIT: {np.average(fmo_met_eq_lit):.2%}")