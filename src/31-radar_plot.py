#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import jezecek.fig_utils
import json
import argparse

COLORS = [
    "#3a29bc",
    "#a663aa"
]

args = argparse.ArgumentParser()
args.add_argument(
    "-i", "--input", default="data/eval_EVAL/paraphrase_parrot.jsonl")
args = args.parse_args()

data_preserved = [json.loads(x) for x in open(
    args.input.replace("EVAL", "preserved_fixed"), "r")]
data_preserved = [x for x in data_preserved if x["dataset"] == "fmo"]

data_present = [json.loads(x) for x in open(
    args.input.replace("EVAL", "present_fixed"), "r")]
data_present = [x for x in data_present if x["dataset"] == "fmo"]

data_sentsim = [json.loads(x) for x in open(
    args.input.replace("EVAL", "sentsim"), "r")]
data_sentsim = [x for x in data_sentsim if x["dataset"] == "fmo"]

lit_present = np.average([float(x["text_lit"]) for x in data_present])
met_present = np.average([float(x["text_met"]) for x in data_present])
lit_preserved = np.average([float(x["text_lit"]) for x in data_preserved])
met_preserved = np.average([float(x["text_met"]) for x in data_preserved])
lit_sentsim = np.average([x["text_lit"] for x in data_sentsim]) * 5
met_sentsim = np.average([x["text_met"] for x in data_sentsim]) * 5

# categories = ['Lit. Present', 'Met. Present', 'Lit. Preserved', 'Met. Preserved', 'Lit. Sentsim', 'Met. Sentsim']
categories = ['Present', 'Preserved', 'Sentsim']
# categories = [*categories, categories[0]]

restaurant_lit = [lit_present, lit_preserved, lit_sentsim]
# restaurant_lit = [*restaurant_lit, restaurant_lit[0]]
restaurant_met = [met_present, met_preserved, met_sentsim]
# restaurant_met = [*restaurant_met, restaurant_met[0]]

label_loc_lit = np.linspace(
    start=0, stop=1 * np.pi,
    num=len(restaurant_lit)) + np.pi / 2
label_loc_met = np.linspace(
    stop=0, start=1 * np.pi,
    num=len(restaurant_lit)) - np.pi / 2

plt.figure(figsize=(1.9, 2))
plt.subplot(polar=True)
plt.plot(label_loc_lit, restaurant_lit, label='Lit.', color=COLORS[0])
plt.plot(label_loc_met, restaurant_met, label='Met', color=COLORS[1])

plt.fill_between(
    x=label_loc_lit,
    y1=restaurant_lit,
    color=COLORS[0],
    alpha=0.5,
)
plt.fill_between(
    x=label_loc_met,
    y1=restaurant_met,
    color=COLORS[1],
    alpha=0.5,
)


def get_pretty_name():
    text = args.input.split("/")[-1].removesuffix(".jsonl").replace("_", " ")
    text = text.capitalize()
    text = text.replace("bart", "BART")
    text = text.replace("parrot", "Parrot")
    text = text.replace("paws", "PAWS")
    text = text.replace("pegasus", "Pegasus")
    text = text.replace("google", "Google")
    text = text.replace("t5", "T5")
    text = text.replace("opus", "OPUS")
    text = text.replace("deepl", "DeepL")
    text = text.replace("nllb", "NLLB")
    text = text.replace(" cs", " CS")
    text = text.replace(" de", " DE")
    return text

def get_bare_name():
    text = args.input.split("/")[-1].removesuffix(".jsonl")
    return text


plt.title(get_pretty_name(), y=1.15)
# phantom ticks
plt.thetagrids(
    [0, 180, 90, 270],
    ["", "", "", ""]
)
plt.text(label_loc_lit[1], 6.5, "Preserved", rotation=90, va="center")
plt.text(label_loc_met[1], 6, "Preserved", rotation=90, va="center")
plt.text(label_loc_lit[0], 5.5, "Present", rotation=0, ha="center")
plt.text(label_loc_lit[2], 6.2, "Similarity", rotation=0, ha="center")
plt.yticks(range(1, 6))
plt.tight_layout(pad=0.2)
plt.savefig(f"computed/figures/radar/{get_bare_name()}.svg")
plt.show()


# for MODEL in "paraphrase_bart" "paraphrase_parrot" "paraphrase_paws" "paraphrase_pegasus" "translate_deepl_cs" "translate_deepl_de" "translate_google_cs" "translate_google_de" "translate_nllb_cs" "translate_nllb_de" "translate_opus_cs" "translate_opus_de"; do
#     DISPLAY="" ./src/31-radar_plot.py -i "data/eval_EVAL/${MODEL}.jsonl"
# done
