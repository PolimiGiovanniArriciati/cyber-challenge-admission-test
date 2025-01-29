import sys
import numpy as np
import cProfile
from tqdm import tqdm, trange
from sympy import divisors
from itertools import combinations

# Compute and print results
amici_moltiplicatori = {
    n**2: zip(divisors(n**2), divisors(n**2)[::-1])
    for n in trange(1, 10_000 + 1, desc="computing possible roots")
}

# look for all the possible root values
def count_intervals_opt(N, arr):
    possible_equivalences = compute_indexes(N, arr)
    M = np.zeros((N, N), dtype=int)
    for pos, el in enumerate(tqdm(arr, desc="looking for intervals in the array")):
        for i0, i1 in possible_equivalences[el - 1]:
            if i0[i0 > pos].size == 0 or i1[i1 > pos].size == 0:
                continue
            val1_index = i0[i0 > pos][0]
            val2_index = i1[i1 > pos][0]
            if val1_index == val2_index:
                # pick the next one.
                if i0[i0 > pos].size == 1 and i1[i1 > pos].size == 1:
                    # there is only one value to be joint and is not possible to create the triplet, skip
                    continue
                val2_index = i1[i1 > pos][1]
            M[0 : pos + 1, max(val1_index, val2_index) :] = 1
            if max(val1_index, val2_index) == pos + 2:
                # the best possible case is found, can break the loop for this element
                break
    return np.sum(M)


def compute_indexes(N, arr):
    max_val = np.max(arr)
    indexes = np.arange(N, dtype=int)
    possible_equivalences = [[] for _ in range(max_val)]
    for val in trange(
        1, max_val + 1, desc="applying roots on index!?"
    ):  # can this be optimized? what values should we consider?
        val_sq = val**2
        for val2, val3 in amici_moltiplicatori[val_sq]:
            if val2 <= val3 and val3 <= max_val:  # val3 is int
                # put in possible_equivalences the indexes of the other values
                assert val2 * val3 == val_sq, f"{val2} * {val3} != {val_sq}"
                val3 = int(val3)
                i0 = indexes[arr == val]
                i1 = indexes[arr == val2]
                i2 = indexes[arr == val3]
                if i0.size == 0 or i1.size == 0 or i2.size == 0:
                    continue
                possible_equivalences[val - 1].append(np.array((i1, i2), dtype=object))
                possible_equivalences[val2 - 1].append(np.array((i0, i2), dtype=object))
                possible_equivalences[val3 - 1].append(np.array((i0, i1), dtype=object))
    return possible_equivalences


def count_intervals(N, a):
    "OG solution for debugging purposes only"
    cases = set()
    for i in range(N):
        for j in range(i + 1, N):
            for k in range(j + 1, N):
                if (
                    a[i] * a[j] == a[k] ** 2
                    or a[i] * a[k] == a[j] ** 2
                    or a[j] * a[k] == a[i] ** 2
                ):
                    for k in range(k, N):
                        cases.add((i, k))
                        for ii in range(0, i):
                            cases.add((ii, k))
    return len(cases)


def challenge():
    if sys.argv.__len__() > 1:
        input = sys.argv[1]
    else:
        input = "input.txt"
    print(f"Reading from: {input}")
    fin = open(input, "r")  # Input file provided by the platform
    fout = open("output.txt", "w")  # Output file to submit

    T = int(fin.readline().strip())

    for _ in trange(T, desc="Test cases"):
        N = int(fin.readline().strip())
        a = np.array(list(map(int, fin.readline().strip().split())))
        # ret = count_intervals(N, a)
        ret = count_intervals_opt(N, a)
        fout.write(f"{ret}\n")


cProfile.run("challenge()", "output.prof")
