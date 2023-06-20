#!/usr/bin/env python3

import json
import os
import tqdm
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
tokenizer = PegasusTokenizer.from_pretrained('tuner007/pegasus_paraphrase')
model = PegasusForConditionalGeneration.from_pretrained('tuner007/pegasus_paraphrase').to(DEVICE)

def paraphrase_text(input_text, num_return_sequences=1, num_beams=10):
    batch = tokenizer(
        [input_text],
        truncation=True,
        padding='longest',
        max_length=60,
        return_tensors="pt"
    ).to(DEVICE)
    translated = model.generate(
        **batch, max_length=60, num_beams=num_beams,
        num_return_sequences=num_return_sequences, temperature=1.5
    )
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]
    return tgt_text

os.makedirs("data/output", exist_ok=True)
data = [json.loads(x) for x in open("data/output/dataset.jsonl", "r")]

out_file = open(f"data/output/paraphrase_pegasus.jsonl", "w")
for line in tqdm.tqdm(data):
    if line["text_lit"]:
        line["text_lit"] = paraphrase_text(line["text_lit"])
    if line["text_met"]:
        line["text_met"] = paraphrase_text(line["text_met"])

# save at the end
out_file.write("\n".join([
    json.dumps(o, ensure_ascii=False) for o in data
]) + "\n")
