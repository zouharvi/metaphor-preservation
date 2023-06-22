#!/usr/bin/env python3

from sentence_transformers import SentenceTransformer, util
import argparse
import tqdm
import json

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', device="cuda")


args = argparse.ArgumentParser()
args.add_argument("-i", "--input", default="data/output/dataset.jsonl")
args.add_argument("-o", "--output", default="data/eval_sentsim/dataset.jsonl")
args = args.parse_args()

data_new = [json.loads(x) for x in open(args.input, "r")]
data_src = [json.loads(x) for x in open("data/output/dataset.jsonl", "r")]
data_out = []

def get_sentsim(text1, text2):
    embedding_1= model.encode(text1, convert_to_tensor=True)
    embedding_2 = model.encode(text2, convert_to_tensor=True)
    return float(util.pytorch_cos_sim(embedding_1, embedding_2)[0,0].cpu())

for line_src, line_new in tqdm.tqdm(zip(data_src, data_new), total=len(data_src)):
    if line_src["text_lit"]:
        line_src["text_lit"] = get_sentsim(line_src["text_lit"], line_new["text_lit"])
    if line_src["text_met"]:
        line_src["text_met"] = get_sentsim(line_src["text_met"], line_new["text_met"])

    data_out.append(line_src)

open(args.output, "w").write("\n".join([
    json.dumps(o, ensure_ascii=False) for o in data_out
]) + "\n")




# for MODEL in "paraphrase_bart" "paraphrase_parrot" "paraphrase_paws" "paraphrase_pegasus" "translate_deepl_cs" "translate_deepl_de" "translate_google_cs" "translate_google_de" "translate_nllb_cs" "translate_nllb_de" "translate_opus_cs" "translate_opus_de"; do
#     echo "Running $MODEL";
#     ./src/24-eval_sentsim.py -i "data/output/${MODEL}.jsonl" -o "data/eval_sentsim/${MODEL}.jsonl";
# done
