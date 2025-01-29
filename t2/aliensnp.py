#!/Users/gio/.virtualenvs/main/bin/python3
import sys
import cProfile
import numpy as np
from tqdm import tqdm

if sys.argv.__len__() > 1:
    input = sys.argv[1]
else:
    input = "2025-aliens_aliens-1_1738072310.txt"
    # input = "input.txt"
print(f"Reading from: {input}")
fin = open(input, "r")  # Input file provided by the platform
fout = open("outputnp.txt", "w")  # Output file to submit

CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# @profile
def execute_code(code):
    s = np.array([])
    for C in tqdm(code):
        match C[0]:
            case "add":
                s = np.append(s, CHARACTERS.index(C[1]))
            case "del":
                s = s[:-1]
            case "swap":
                x, y = CHARACTERS.index(C[1]),\
                        CHARACTERS.index(C[2])
                indexes_x = np.where(s == x)
                indexes_y = np.where(s == y)
                s[indexes_x] = y
                s[indexes_y] = x
            case "rot":
                k = int(C[1])
                s = (s+k)%len(CHARACTERS)
            case _:
                raise ValueError(f"Invalid operation: {C[0]}")
    s = "".join([CHARACTERS[i] for i in s.astype(int)])
    # print(s)
    return s

def function():
    N = int(fin.readline().strip())
    code = []
    # prev = None
    for _ in range(N):
        s = fin.readline().strip().split(" ")
        # assert s[0] in ["add", "del", "swap", "rot"], f"Invalid operation: {s[0]}, {s}, {len(code)}"
        # if prev[0] == s[0]:
        #     if s[0] in ["add", "rot"]:
        #         code[-1].append(s[1])
        #     elif s[0] in ["swap"]:
        #         code[-1].append(s[1])
        #         code[-1].append(s[2])
        code.append(s)
    s = execute_code(code)
    fout.write(s)

# cProfile.run("function()", 'output.prof')

if __name__ == "__main__":
    function()