#!/usr/bin/env python3

import glob
import re
import subprocess
import sys

if len(sys.argv) < 3:
    raise RuntimeError("Usage: python3 sym2pj64.py OBJ_DIR IN_FILE OUT_FILE")

obj_dir = sys.argv[1]
in_path = sys.argv[2]
out_path = sys.argv[3]

sym_types = {}
lines = []
try:
    lines = open('src/c/output/debug.txt', 'r').readlines()
except:
    pass

for line in lines:
    m = re.match('^[0-9a-fA-F]+.*\.([^\s]+)\s+[0-9a-fA-F]+\s+([^.$][^\s]+)\s+$', line)
    if m:
        sym_type = m.group(1)
        name = m.group(2)
        sym_types[name] = 'code' if sym_type == 'text' else 'data'

in_file = open(in_path, 'r')
out_file = open(out_path, 'w')

for line in in_file:
    parts = line.strip().split(' ')
    if len(parts) < 2:
        continue
    address, label = parts
    if address[0] != '8':
        continue
    if label[0] == '.':
        continue
    label_type = sym_types.get(label) or ('data' if label.isupper() else 'code')
    out_line = ','.join([address, label_type, label])
    print(out_line, file=out_file)

in_file.close()
out_file.close()
