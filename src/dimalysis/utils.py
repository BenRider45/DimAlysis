import numpy as np
from itertools import combinations


def rSubset(arr, r):
    return list(combinations(arr, r))
