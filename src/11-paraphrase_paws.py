#!/usr/bin/env python3

import json
import os
import tqdm
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained("Vamsi/T5_Paraphrase_Paws")  
model = AutoModelForSeq2SeqLM.from_pretrained("Vamsi/T5_Paraphrase_Paws").to(DEVICE)

def paraphrase_text(text):
    text =  "paraphrase: " + text + " </s>"

    encoding = tokenizer.encode_plus(text,pad_to_max_length=True, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"].to("cuda"), encoding["attention_mask"].to(DEVICE)

    outputs = model.generate(
        input_ids=input_ids, attention_mask=attention_masks,
        max_length=256,
        do_sample=True,
        top_k=120,
        top_p=0.95,
        early_stopping=True,
        num_return_sequences=5
    )

    line = tokenizer.decode(outputs[0], skip_special_tokens=True,clean_up_tokenization_spaces=True)
    print(line)
    return line

os.makedirs("data/output", exist_ok=True)
data = [json.loads(x) for x in open("data/output/dataset.jsonl", "r")]

out_file = open(f"data/output/paraphrase_paws.jsonl", "w")
for line in tqdm.tqdm(data):
    if line["text_lit"]:
        line["text_lit"] = paraphrase_text(line["text_lit"])
    if line["text_met"]:
        line["text_met"] = paraphrase_text(line["text_met"])

# save at the end
out_file.write("\n".join([
    json.dumps(o, ensure_ascii=False) for o in data
]) + "\n")
