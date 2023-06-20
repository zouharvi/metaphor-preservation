#!/usr/bin/env python3

import argparse
import json
import collections

args = argparse.ArgumentParser()
args.add_argument("-i", "--input", default="data/eval_present/translate_google_cs.jsonl")
args.add_argument("-o", "--output", default="data/eval_present_fixed/translate_google_cs.jsonl")
args = args.parse_args()

data = [json.loads(x) for x in open(args.input, "r")]

freqs = collections.defaultdict(lambda: collections.Counter())

for line in data:
    if line["text_lit"]:
        try:
            # try to parse
            val = int(line["text_lit"])
            freqs[line["dataset"] + "_lit"].update([val])
        except:
            pass
    if line["text_met"]:
        try:
            # try to parse
            val = int(line["text_met"])
            freqs[line["dataset"] + "_met"].update([val])
        except:
            pass

for line in data:
    if line["text_lit"]:
        try:
            # try to parse
            val = int(line["text_lit"])
        except:
            line["text_lit"] = freqs[line["dataset"] + "_lit"].most_common(1)[0][0]
    if line["text_met"]:
        try:
            # try to parse
            val = int(line["text_met"])
        except:
            line["text_met"] = freqs[line["dataset"] + "_met"].most_common(1)[0][0]


out_file = open(args.output, "w")
out_file.write("\n".join([
    json.dumps(o, ensure_ascii=False) for o in data
]) + "\n")


# for MODEL in "paraphrase_bart" "paraphrase_parrot" "paraphrase_paws" "paraphrase_pegasus" "translate_deepl_cs" "translate_deepl_de" "translate_google_cs" "translate_google_de" "translate_nllb_cs" "translate_nllb_de" "translate_t5_cs" "translate_t5_de"; do
#     echo "Fixing eval_preserved/$MODEL";
#     ./src/23-fix_eval_digits.py -i "data/eval_preserved/${MODEL}.jsonl" -o "data/eval_preserved_fixed/${MODEL}.jsonl";
#     echo "Fixing eval_present/$MODEL";
#     ./src/23-fix_eval_digits.py -i "data/eval_present/${MODEL}.jsonl" -o "data/eval_present_fixed/${MODEL}.jsonl";
# done
