#!/usr/bin/env python3

import openai
import os
import json
import copy
import time
import tqdm
import backoff
import argparse

args = argparse.ArgumentParser()
args.add_argument("-i", "--input", default="data/output/dataset.jsonl")
args.add_argument("-o", "--output", default="data/output_eval/dataset.jsonl")
args = args.parse_args()

os.makedirs("data/output_eval", exist_ok=True)

openai.api_key = os.getenv("OPENAI_API_KEY")

# in case the process gets killed
data = [json.loads(x) for x in open(args.input, "r")]
if os.path.exists(args.output):
    data_out = [json.loads(x) for x in open(args.output, "r")]
    data = data[len(data_out):]
else:
    data_out = []

@backoff.on_exception(backoff.expo, openai.error.RateLimitError, max_tries=16, jitter=None)
def get_metaphor_rating(text):
    # micro throttle
    time.sleep(0.3)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful and austere assistant for metaphor detection in text. Reply using only a single number 1 to 5 scale and nothing else."},
            {"role": "user", "content": text},
        ],
        max_tokens=1
    )

    # print(completion)
    rating = completion.choices[0].message.content
    return rating

for line in tqdm.tqdm(data):
    line = copy.deepcopy(line)
    if line["text_lit"]:
        line["text_lit"] = get_metaphor_rating(line["text_lit"])
    if line["text_met"]:
        line["text_met"] = get_metaphor_rating(line["text_met"])

    data_out.append(line)

    # resave everything
    out_file = open(args.output, "w")
    out_file.write("\n".join([
        json.dumps(o, ensure_ascii=False) for o in data_out
    ]) + "\n")
