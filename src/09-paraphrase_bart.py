#!/usr/bin/env python3

import json
import os
import tqdm
import torch
from transformers import BartForConditionalGeneration, BartTokenizer

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

model = BartForConditionalGeneration.from_pretrained('eugenesiow/bart-paraphrase').to(DEVICE)
tokenizer = BartTokenizer.from_pretrained('eugenesiow/bart-paraphrase')

def paraphrase_text(input_text):
    batch = tokenizer(input_text, return_tensors='pt').to(DEVICE)
    generated_ids = model.generate(batch['input_ids'])
    generated_sentence = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(generated_sentence)
    return generated_sentence

os.makedirs("data/output", exist_ok=True)
data = [json.loads(x) for x in open("data/dataset.jsonl", "r")]

out_file = open(f"data/output/paraphrase_bart.jsonl", "w")
for line in tqdm.tqdm(data):
    if line["text_lit"]:
        line["text_lit"] = paraphrase_text(line["text_lit"])
    if line["text_met"]:
        line["text_met"] = paraphrase_text(line["text_met"])

# save at the end
out_file.write("\n".join([
    json.dumps(o, ensure_ascii=False) for o in data
]) + "\n")
