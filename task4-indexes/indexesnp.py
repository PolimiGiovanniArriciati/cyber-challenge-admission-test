#!/usr/bin/env python
import sys
import numpy as np
import cProfile
from tqdm import tqdm, trange
from sympy import divisors
from itertools import combinations

# Compute and print results
amici_moltiplicatori = {
    n
    ** 2: [
        (val2, val3)
        for val2, val3 in zip(divisors(n**2), divisors(n**2)[::-1])
        if val2 < val3
    ]
    for n in range(1, 10_000 + 1)
    # for n in range(1, 10_000 + 1, desc="computing possible roots")
}
divisors_ = {
    # n: divisors(n**2) for n in trange(1, 10_000 + 1, desc="computing possible roots")
}


def value_appears_twice(val, arr):
    return arr[arr == val].size > 1


def count_intervals_set(N, arr):
    possible_equivalences = compute_possible_equivalences(N, arr) #X*X=X**2 is not present
    M = np.zeros((N, N))
    for pos, val in enumerate(
        tqdm(arr[:-2], desc="looking for intervals in the array")
    ):
        poss_eq = possible_equivalences[val]
        K = 100 if pos + 100 < N else N + 1 - pos
        next_values = arr[pos + 1 : pos + K]
        if not np.any(
            np.in1d(poss_eq[:, 0], next_values) & np.in1d(poss_eq[:, 1], next_values)
        ) and not value_appears_twice(val, next_values):
            continue
        for k in range(3, K):
            next_values = arr[pos + 1 : pos + k]
            pres_eq = poss_eq[
                np.in1d(poss_eq[:, 0], next_values)
                & np.in1d(poss_eq[:, 1], next_values)
            ]
            if pres_eq.size > 0 or value_appears_twice(val, next_values):
                M[0 : pos + 1, pos + k - 1 :] = 1
                break
    return np.sum(M).astype(int)


# look for all the possible root values
def count_intervals_opt(N, arr):
    possible_equivalences = compute_indexes_possible_equivalences(N, arr)
    M = np.zeros((N, N), dtype=int)
    for pos, el in enumerate(tqdm(arr, desc="looking for intervals in the array")):
        min_triplet_index = np.inf
        for i0, i1 in possible_equivalences[el].values():
            # TODO: direct access to the possible_equivalences pairs to prioritize the closest ones.
            # need to check what values are in the next indexes, filtering the ones that re in amici_moltiplicatori[el] e ma anche i divisori?
            i0 = i0[i0 > pos]
            i1 = i1[i1 > pos]
            if i0.size == 0 or i1.size == 0:
                continue
            index_val1 = i0[0]
            index_val2 = i1[0]
            if index_val1 == index_val2:
                assert (
                    el == arr[index_val1] == arr[index_val2]
                ), f"Values are not equal, shouldn't be in this branch..."
                # pick the next one.
                if i0.size == 1 and i1.size == 1:
                    # there is only one value to be joint and is not possible to create the triplet, skip
                    continue
                index_val2 = i1[1]
            if min_triplet_index > max(index_val1, index_val2):
                min_triplet_index = max(index_val1, index_val2)
            if min_triplet_index == pos + 2:
                # the best possible case is found, can break the loop for this element
                break
        if min_triplet_index is not np.inf:
            M[0 : pos + 1, min_triplet_index:] = 1
    return np.sum(M)


def compute_possible_equivalences(N, arr):
    max_val = np.max(arr)
    # pes = {val: [(val, val)] for val in range(1, max_val**2 + 1)}
    pes = {val: [(1, val**2)] for val in range(1, max_val**2 + 1)}
    for val in trange(
        1,
        max_val + 1,
    ):
        val_sq = val**2
        for val2, val3 in amici_moltiplicatori[val_sq]:
            assert val2 * val3 == val_sq, f"{val2} * {val3} != {val_sq}"
            pes[val] = np.append(pes[val], [(val2, val3)], axis=0)
            pes[val2] = np.append(pes[val2], [(val, val3)], axis=0)
            pes[val3] = np.append(pes[val3], [(val2, val)], axis=0)
    pes[1] = pes[1][
        np.all(pes[1] != [1, 1], axis=1)
    ]  # this is to avoid the 1, 1 case and threat as all the other duplicates
    return pes


def compute_indexes_possible_equivalences(N, arr):
    max_val = np.max(arr)
    indexes = np.arange(N, dtype=int)
    possible_equivalences = {val: {} for val in range(1, max_val + 1)}
    for val in trange(
        1,
        max_val + 1,
        # desc="applying roots on index!?"
    ):  # can this be optimized? what values should we consider?
        possible_equivalences[val][(val, val)] = np.array(
            (indexes[arr == val], indexes[arr == val]), dtype=object
        )
        val_sq = val**2
        for val2, val3 in amici_moltiplicatori[val_sq]:
            # put in possible_equivalences the indexes of the other values
            assert val2 * val3 == val_sq, f"{val2} * {val3} != {val_sq}"
            i0 = indexes[arr == val]
            i1 = indexes[arr == val2]
            i2 = indexes[arr == val3]
            if i0.size == 0 or i1.size == 0 or i2.size == 0:
                continue
            possible_equivalences[val][(val2, val3)] = np.array((i1, i2), dtype=object)
            possible_equivalences[val2][(val, val3)] = np.array((i0, i2), dtype=object)
            possible_equivalences[val3][(val, val2)] = np.array((i0, i1), dtype=object)
    return possible_equivalences


def count_intervals(N, a):
    "OG solution for debugging purposes only"
    "to complete task 2 it took?"
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
    M = np.zeros((N, N))
    for i, j in cases:
        M[i, j] = 1
    print(np.sum(M))
    print(M)
    return len(cases)


def challenge():
    if sys.argv.__len__() > 1:
        input = sys.argv[1]
    else:
        input = "input.txt"
    print(f"Reading from: {input}")
    fin = open(input, "r")  # Input file provided by the platform
    fout = open(f"output-{input}", "w")  # Output file to submit

    T = int(fin.readline().strip())

    for _ in trange(T, desc="Test cases"):
        N = int(fin.readline().strip())
        a = np.array(list(map(int, fin.readline().strip().split())))
        ret = count_intervals_set(N, a)
        fout.write(f"{ret}\n")


cProfile.run("challenge()", "output.prof")
