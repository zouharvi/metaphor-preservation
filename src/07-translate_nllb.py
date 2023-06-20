#!/usr/bin/env python3

import json
import os
import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-1.3B")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-1.3B").to(DEVICE)

os.makedirs("data/output", exist_ok=True)
data = [json.loads(x) for x in open("data/dataset.jsonl", "r")]

LANG_TO_NAME = {
    "cs": "ces_Latn",
    "de": "deu_Latn",
}


def translate_text(text, target_lang):
    target_lang = LANG_TO_NAME[target_lang]

    # batch size 1
    inputs = tokenizer(text, return_tensors="pt").to(DEVICE)
    translated_tokens = model.generate(
        **inputs, forced_bos_token_id=tokenizer.lang_code_to_id[target_lang], max_length=128
    )
    decoded = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
    return decoded

for target_lang in ["cs", "de"]:
    out_file = open(f"data/output/translate_nllb_{target_lang}.jsonl", "w")
    for line in tqdm.tqdm(data):
        if line["text_lit"]:
            line["text_lit"] = translate_text(line["text_lit"], target_lang)
        if line["text_met"]:
            line["text_met"] = translate_text(line["text_met"], target_lang)

    # save at the end
    out_file.write("\n".join([
        json.dumps(o, ensure_ascii=False) for o in data
    ]) + "\n")
