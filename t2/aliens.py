#!/bin/env python3
import sys
import cProfile
import pstats

if sys.argv.__len__() > 1:
    input = sys.argv[1]
else:
    input = "input.txt"
print(f"Reading from: {input}")
fin = open(input, "r")  # Input file provided by the platform
fout = open("output.txt", "w")  # Output file to submit

CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# @profile
def execute_code(N, code):
    s = []
    for c in code:
        C = c.split(" ")
        match C[0]:
            case "add":
                s = list(s)
                s.append(CHARACTERS.index(C[1]))
            case "del":
                s = list(s)
                s = s[:-1]
            case "swap":
                x, y = CHARACTERS.index(C[1]),\
                        CHARACTERS.index(C[2])
                s = [y if el == x else x if el == y else el for el in s]
            case "rot":
                k = int(C[1])
                s = map(lambda x: (x+k)%len(CHARACTERS), s)
            case _:
                raise ValueError(f"Invalid operation: {C[0]}")

    s = "".join([CHARACTERS[i] for i in s])
    print(s)
    return s

def function():
    N = int(fin.readline().strip())
    code = []
    for _ in range(N):
        s = fin.readline().strip()
        code.append(s)
    s = execute_code(N, code)
    fout.write(s)

cProfile.run("function()", 'output.prof')