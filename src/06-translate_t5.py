#!/usr/bin/env python3

import json
import os
import tqdm
from transformers import T5Tokenizer, T5ForConditionalGeneration

# TODO: move to GPU?
tokenizer = T5Tokenizer.from_pretrained('t5-large')
model = T5ForConditionalGeneration.from_pretrained('t5-large', return_dict=True)

os.makedirs("data/output", exist_ok=True)
data = [json.loads(x) for x in open("data/dataset.jsonl", "r")]

LANG_TO_NAME = {
    "cs": "Czech",
    "de": "German",
}

def translate_text(text, target_lang):
    target_lang = LANG_TO_NAME[target_lang]

    # batch size 1
    input_ids = tokenizer(
        f"translate English to {target_lang}: "+text,
        return_tensors="pt",
    ).input_ids

    outputs = model.generate(input_ids)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(decoded)
    print(type(decoded))
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
