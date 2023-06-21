#!/usr/bin/env python3

from sentence_transformers import SentenceTransformer, util
import argparse
import tqdm
import json
import numpy as np

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', device="cuda")

args = argparse.ArgumentParser()
args.add_argument("-o", "--output", default="data/eval_sentsim/dataset.jsonl")
args = args.parse_args()

data_src = [json.loads(x) for x in open("data/output/dataset.jsonl", "r")]
data_out = []

def get_sentsim(text1, text2):
    embedding_1= model.encode(text1, convert_to_tensor=True)
    embedding_2 = model.encode(text2, convert_to_tensor=True)
    return float(util.pytorch_cos_sim(embedding_1, embedding_2)[0,0].cpu())

values = []
for line_src in tqdm.tqdm(data_src):
    if line_src["text_lit"] and line_src["text_met"]:
        line_src["text_lit"] = get_sentsim(line_src["text_lit"], line_src["text_met"])
        line_src["text_met"] = line_src["text_lit"]
        values.append(line_src["text_lit"])
    else:
        line_src["text_lit"] = None
        line_src["text_met"] = None

    data_out.append(line_src)

print(np.average(values))

open(args.output, "w").write("\n".join([
    json.dumps(o, ensure_ascii=False) for o in data_out
]) + "\n")