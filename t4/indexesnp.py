import sys
import numpy as np

if sys.argv.__len__() > 1:
    input = sys.argv[1]
else:
    input = "input.txt"
print(f"Reading from: {input}")
fin = open(input, "r")  # Input file provided by the platform
fout = open("output.txt", "w")  # Output file to submit

#
# FACCIO SCHIFO IN OPERAZIONI CON NUMPY/VETTORI :(
#


def count_intervals_min_max(N, arr):
    """do some kind of search from top and bottom
    does not work"""
    M = np.zeros((N, N), dtype=int)
    arr = np.array(arr)
    sort_a = np.argsort(arr)
    indexes = np.arange(N, dtype=int)
    for n, i, min_val in zip(indexes, sort_a, arr[sort_a]):
        for j, max_val in zip(sort_a[:n:-1], arr[sort_a[:n:-1]]):
            # if M[i, j] == 0:  # indexes that are not already checked
            mid_val = max_val**2 / min_val
            if mid_val % 1 == 0:
                for k in indexes[arr == mid_val]:
                    if len({i, j, k}) == 3:
                        mn = min(i, j, k)
                        mx = max(i, j, k)
                        M[0 : mn + 1, mx:] = 1
            mid_val = np.sqrt(max_val / min_val)
            if mid_val % 1 == 0:
                for k in indexes[arr == mid_val]:
                    if len({i, j, k}) == 3:
                        mn = min(i, j, k)
                        mx = max(i, j, k)
                        M[0:mn, mx:] = 1
    print(M)
    print(np.sum(M))
    return np.sum(M[np.unique(M)])


# look for all the possible root values
def count_intervals(N, arr):
    M = np.zeros((N, N), dtype=int)
    possible_equivalences = compute_indexes(N, arr)
    for i, val in enumerate(arr):
        for i0, i1 in possible_equivalences[val - 1]:
            if i0[i0 > i].size == 0 or i1[i1 > i].size == 0:
                continue
            val1_index = i0[i0 > i][0]
            val2_index = i1[i1 > i][0]
            if val1_index == val2_index:
                # pick the next one.
                if i0[i0 > i].size == 1 and i1[i1 > i].size == 1:
                    # there is only one value to be joint and is not possible to create the triplet, skip
                    continue
                val2_index = i1[i1 > i][1]
            M[0 : i + 1, max(val1_index, val2_index) :] = 1
    # am I missing anything?
    print(M)
    print(np.sum(M))
    return np.sum(M)


def compute_indexes(N, arr):
    indexes = np.arange(N, dtype=int)
    possible_equivalences = [[] for _ in range(np.max(arr))]
    for val in range(
        1, np.max(arr) + 1
    ):  # can this be optimized? what values should we consider?
        val_sq = val**2
        for val2 in range(1, val_sq + 1):
            val3 = val_sq / val2
            if 0 == val3 % 1 and val2 <= val3 and val3 <= np.max(arr):  # val3 is int
                # put in possible_equivalences the indexes of the other values
                val3 = int(val3)
                assert val2 * val3 == val**2
                i0 = indexes[arr == val]
                i1 = indexes[arr == val2]
                i2 = indexes[arr == val3]
                if i0.size == 0 or i1.size == 0 or i2.size == 0:
                    continue
                possible_equivalences[val - 1].append(np.array((i1, i2), dtype=object))
                possible_equivalences[val2 - 1].append(np.array((i0, i2), dtype=object))
                possible_equivalences[val3 - 1].append(np.array((i0, i1), dtype=object))
    return possible_equivalences


T = int(fin.readline().strip())

for _ in range(T):
    N = int(fin.readline().strip())
    a = np.array(list(map(int, fin.readline().strip().split())))
    ret = count_intervals(N, a)
    fout.write(f"{ret}\n")
