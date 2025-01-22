from bisect import bisect_left
from collections import Counter, defaultdict


def counter_cumsum(sequence, sub_c):
    result = defaultdict(list)
    for step in range(len(sequence)):
        for key in list(sub_c.keys()) + [0]:
            result[key] += [Counter(sequence[:step]).get(key, 0)]
    return result


def counter_sum(sequence, sub_c):
    result = defaultdict(list)
    cnt = Counter(sequence)
    result = {key: cnt.get(key, 0) for key in sub_c.keys()}
    return result


def counter_sum_norm(sequence, sub_c):
    result = defaultdict(list)
    cnt = Counter(sequence)
    result = {key: cnt.get(key, 0) / total for key, total in sub_c.items()}
    return result


def bin_placement(query, bins):
    if not query or query == 0:
        return 0
    pos = bisect_left(bins, query)
    if pos == 0:
        return bins[0]
    if pos == len(bins):
        return bins[-1]
    before = bins[pos - 1]
    after = bins[pos]
    if after - query < query - before:
        return after
    else:
        return before
