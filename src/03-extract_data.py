#!/usr/bin/env python3

raise Exception("Deprecated")

import json
import collections

files = {}
files_line_counter = collections.defaultdict(int)

def write_to_file(x, line):
    lines_writter = files_line_counter[x]
    files_line_counter[x] += 1
    x = f"data/chunked/{x}_p{lines_writter//50}.txt"
    if x not in files:
        files[x] = open(x, "w")
    files[x].write(line)


data = [json.loads(x) for x in open("data/output/dataset.jsonl", "r")]

for o in data:
    write_to_file(f'{o["dataset"]}_met', f'{o["text_met"]}\n')
    write_to_file(f'{o["dataset"]}_lit', f'{o["text_lit"]}\n')
