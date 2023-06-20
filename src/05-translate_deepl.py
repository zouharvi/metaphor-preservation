#!/usr/bin/env python3

import deepl
from os import environ
import json
import os
import tqdm
import time

os.makedirs("data/output", exist_ok=True)
data = [json.loads(x) for x in open("data/dataset.jsonl", "r")]

translator = deepl.Translator(auth_key=environ.get("DEEPL_AUTH"))

def translate_text(text: str, target_language_code: str):
    # some micro throttle
    time.sleep(0.3)

    result = translator.translate_text(
        text,
        source_lang="en",
        target_lang=target_language_code
    )
    return result.text

for target_lang in ["cs", "de"]:
    out_file = open(f"data/output/translate_deepl_{target_lang}.jsonl", "w")
    for line in tqdm.tqdm(data):
        if line["text_lit"]:
            line["text_lit"] = translate_text(line["text_lit"], target_lang)
        if line["text_met"]:
            line["text_met"] = translate_text(line["text_met"], target_lang)
    
    # save at the end
    out_file.write("\n".join([
        json.dumps(o, ensure_ascii=False) for o in data
    ]) + "\n")
