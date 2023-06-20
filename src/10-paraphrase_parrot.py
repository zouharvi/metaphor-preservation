#!/usr/bin/env python3

import json
import os
import tqdm
from parrot import Parrot
import warnings
warnings.filterwarnings("ignore")

parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5", use_gpu=True)

def paraphrase_text(input_text):
    paraphrases = parrot.augment(input_phrase=input_text, use_gpu=True)
    if paraphrases:
        return paraphrases[0][0]
    else:
        return input_text

os.makedirs("data/output", exist_ok=True)
data = [json.loads(x) for x in open("data/dataset.jsonl", "r")]

out_file = open(f"data/output/paraphrase_parrot.jsonl", "w")
for line in tqdm.tqdm(data):
    if line["text_lit"]:
        line["text_lit"] = paraphrase_text(line["text_lit"])
    if line["text_met"]:
        line["text_met"] = paraphrase_text(line["text_met"])

# save at the end
out_file.write("\n".join([
    json.dumps(o, ensure_ascii=False) for o in data
]) + "\n")
