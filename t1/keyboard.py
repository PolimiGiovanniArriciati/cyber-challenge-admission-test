#!/bin/env python3

import sys

# Decomment here if you want to read to/write from file
# fin = open("input.txt", "r")  # Input file provided by the platform
# fout = open("output.txt", "w")  # Output file to submit

# Decomment here to read to/write from command line
# fin = sys.stdin  # Input
# fout = sys.stdout  # Output

from string import ascii_lowercase

def find_key(L, s):
    # WRITE YOUR CODE HERE
    missing = set(ascii_lowercase)-set(s)
    return missing

if sys.argv.__len__() > 1:
    input = sys.argv[1]
else:
    input = "input.txt"
print(f"Reading from: {input}")
print(sys.argv)
fin = open(input, "r")  # Input file provided by the platform
fout = open("output.txt", "w")  # Output file to submit

N = int(fin.readline().strip())

for _ in range(N):
    L = int(fin.readline().strip())
    s = fin.readline().strip()
    m = find_key(L, s)
    assert len(m) == 1, f"There should be exactly one missing key, but found more than one. ({m})"
    fout.write(f"{m.pop()}\n")
    