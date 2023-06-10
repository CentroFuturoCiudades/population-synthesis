import numpy as np


def check_solvable(W, C):
    WC = np.column_stack([W, C])

    solvable = np.linalg.matrix_rank(W) == np.linalg.matrix_rank(WC)

    return solvable


def ipf_classic():
    return


def ipf_factor():
    return


def min_norm_solve():
    return
