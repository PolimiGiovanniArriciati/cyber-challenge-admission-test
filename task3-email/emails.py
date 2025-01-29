#!/bin/env python3

import sys
import cProfile

# import numpy as np
from tqdm import tqdm

if sys.argv.__len__() > 1:
    input = sys.argv[1]
else:
    input = "input.txt"
print(f"Reading from: {input}")
fin = open(input, "r")  # Input file provided by the platform
fout = open("output.txt", "w")  # Output file to submit


def find_sum_of_times(N, M, t, f, emails):
    delay = 0
    for email in tqdm(emails):
        time = email
        for i, processing in zip(t, f):
            if time % i == 0:
                pass
            else:
                time += i - time % i
            time += processing
        delay += time
    return delay


N, M = map(int, fin.readline().strip().split())
t = list(map(int, fin.readline().strip().split()))
f = list(map(int, fin.readline().strip().split()))
emails = list(map(int, fin.readline().strip().split()))

delay = find_sum_of_times(N, M, t, f, emails)
print(delay)
fout.write(str(delay) + "\n")
