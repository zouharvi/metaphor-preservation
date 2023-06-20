#!/usr/bin/env python3

import argparse
import json
import collections
import jezecek.fig_utils
import matplotlib.pyplot as plt
import sys
sys.path.append("src")
import utils

args = argparse.ArgumentParser()
args.add_argument(
    "-i", "--input", default="data/eval_present_fixed/dataset.jsonl")
args = args.parse_args()

data = [json.loads(x) for x in open(args.input, "r")]
freqs = collections.defaultdict(lambda: collections.Counter())


for line in data:
    if line["text_lit"]:
        freqs[line["dataset"] + "_lit"].update([int(line["text_lit"])])
    if line["text_met"]:
        freqs[line["dataset"] + "_met"].update([int(line["text_met"])])


STYLE_KWARGS = {
    "edgecolor": "black",
    "linewidth": 2,
}
trofi_sum = sum(freqs["trofi_lit"].values()) + sum(freqs["trofi_met"].values())
fmo_sum = sum(freqs["fmo_lit"].values()) + sum(freqs["fmo_met"].values())

plt.figure(figsize=(4, 2))

plt.barh(
    y=range(1, 6),
    width=[-freqs["trofi_lit"][x] / trofi_sum for x in range(1, 6)],
    left=1,
    color=utils.COLORS[0],
    **STYLE_KWARGS
)
plt.barh(
    y=range(1, 6),
    width=[freqs["trofi_met"][x] / trofi_sum for x in range(1, 6)],
    left=1,
    color=utils.COLORS[1],
    **STYLE_KWARGS
)
plt.barh(
    y=range(1, 6),
    width=[-freqs["fmo_lit"][x] / fmo_sum for x in range(1, 6)],
    left=1.5,
    color=utils.COLORS[0],
    **STYLE_KWARGS
)
plt.barh(
    y=range(1, 6),
    width=[freqs["fmo_met"][x] / fmo_sum for x in range(1, 6)],
    left=1.5,
    color=utils.COLORS[1],
    **STYLE_KWARGS
)
plt.ylabel("Assigned score")
plt.tick_params(axis="x", length=0)
plt.text(0.98, 5, s="Literal", ha="right")
plt.text(1.01, 5, s="Metaphorical", ha="left")
plt.text(1.48, 5, s="Lit.", ha="right")
plt.text(1.54, 5, s="Met.", ha="left")
plt.xticks(
    [1, 1.5],
    ["Trofi", "FMO"]
)
plt.tight_layout(pad=0.1)
plt.savefig("computed/figures/base_violin.svg")
plt.show()
