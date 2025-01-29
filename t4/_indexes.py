#!/bin/env python3
import sys
import numpy as np

if sys.argv.__len__() > 1:
    input = sys.argv[1]
else:
    input = "input.txt"
print(f"Reading from: {input}")
fin = open(input, "r")  # Input file provided by the platform
fout = open("output.txt", "w")  # Output file to submit

def count_intervals(N, a):
    # WRITE YOUR CODE HERE
    cases = set()
    count = 0
    for i in range(N):
        for j in range(i+1, N):
            for k in range(j+1, N):
                if (a[i]*a[j] == a[k]**2
                    or a[i]*a[k] == a[j]**2
                    or a[j]*a[k] == a[i]**2
                    ):
                    count += N-k
                    for k in range(k, N):
                        cases.add((i, k))
                        for ii in range(0, i):
                            cases.add((ii, k))
    M = np.zeros((N, N), dtype=int)
    for i, j in cases:
        M[i, j] = 1
    print(M)
    print(np.sum(M))
    return len(cases)

T = int(fin.readline().strip())

for _ in range(T):
    N = int(fin.readline().strip())
    a = list(map(int, fin.readline().strip().split()))
    ret = count_intervals(N, a)
    # print(ret)
    fout.write(f"{ret}\n")
    break