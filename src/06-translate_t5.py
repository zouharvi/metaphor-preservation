#!/usr/bin/env python3

import json
import os
import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-cs")
model = AutoModelForSeq2SeqLM.from_pretrained(
    "Helsinki-NLP/opus-mt-en-cs").to(DEVICE)

os.makedirs("data/output", exist_ok=True)
data = [json.loads(x) for x in open("data/output/dataset.jsonl", "r")]

def translate_text(text, target_lang):
    # batch size 1
    input_ids = tokenizer(
        text, return_tensors="pt",
    ).input_ids.to(DEVICE)
    outputs = model.generate(input_ids)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded


for target_lang in ["cs", "de"]:
    out_file = open(f"data/output/translate_t5_{target_lang}.jsonl", "w")
    for line in tqdm.tqdm(data):
        if line["text_lit"]:
            line["text_lit"] = translate_text(line["text_lit"], target_lang)
        if line["text_met"]:
            line["text_met"] = translate_text(line["text_met"], target_lang)

    # save at the end
    out_file.write("\n".join([
        json.dumps(o, ensure_ascii=False) for o in data
    ]) + "\n")
