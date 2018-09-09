#!/usr/bin/env python3
import argparse
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--pj64sym', help="Output path for PJ64 debugging symbols")
parser.add_argument('--compile-c', action='store_true', help="Recompile C modules")

args = parser.parse_args()
pj64_sym_path = args.pj64sym
compile_c = args.compile_c

if pj64_sym_path:
    pj64_sym_path = os.path.realpath(pj64_sym_path)

script_dir = os.path.dirname(os.path.realpath(__file__))
run_dir = script_dir + '/..'

if compile_c:
    os.chdir('src/c')
    subprocess.check_call(['make'])
    os.chdir(run_dir)

try:
    subprocess.check_call(['armips', '-sym2', 'temp/symbols', 'src/build.asm'])
except FileNotFoundError:
    subprocess.check_call(['scripts/armips', '-sym2', 'temp/symbols', 'src/build.asm'])

if pj64_sym_path:
    subprocess.check_call(['python3', 'scripts/sym2pj64.py',
        'src/c', 'temp/symbols', pj64_sym_path])
