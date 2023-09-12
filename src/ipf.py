import numpy as np
from numba import njit


def ipf_classic(x, W, c, max_iters=100, tol=1e-5):
    x = x.copy()
    err = np.zeros(max_iters+1)
    err[0] = np.linalg.norm(W @ x - c, ord=1)
    W_mask = W.astype(bool)
    nc = len(c)
    for niter in range(max_iters):
        for i in range(nc):
            wi = W[i]
            ci = c[i]
            mask = W_mask[i]
            alpha = (ci / (wi @ x))
            # Without indexing
            # x = ((ci / (wi @ x)) ** wi) * x

            # With indexing, but avoiding exponentiation
            # Faster according to tests
            x[mask] = alpha * x[mask]

        delta = W @ x - c
        norm_l1 = np.linalg.norm(delta, ord=1)
        err[niter+1] = norm_l1

    return x, err


@njit
def ipf_classic_numba(x, W, c, max_iters=10000, tol=1e-1):
    x = x.copy()
    nc = len(c)
    nx = len(x)
    converged = False
    for niter in range(max_iters):
        for i in range(nc):
            if c[i] != 0:
                alpha = (c[i] / (W[i] @ x))
            else:
                alpha = 0.0

            for j in range(nx):
                if W[i, j] > 0:
                    x[j] *= alpha

        delta = W @ x - c
        norm_l1 = np.linalg.norm(delta, ord=1)
        if norm_l1 < tol:
            converged = True
            print(f'Converged in {niter} iterations.')
            break

    if not converged:
        print('Warning: Max iterations reached.')

    return x, norm_l1


def ipf_factor(x, W, c, max_iters=100):
    a = np.ones_like(c)
    err = np.zeros(max_iters+1)
    err[0] = np.linalg.norm(W @ x - c, ord=1)
    W_mask = W.astype(bool)
    A = np.ones_like(x)

    nc = len(c)
    for niter in range(max_iters):
        for i in range(nc):
            mask = W_mask[i]

            (np.broadcast_to(a, W.T.shape)).prod(axis=1, where=W.T > 0, out=A)
            a[i] = c[i] / np.sum((A[mask]/a[i]) * x[mask])

        delta = W @ (x * A) - c
        norm_l1 = np.linalg.norm(delta, ord=1)
        err[niter+1] = norm_l1

    return a, err


@njit
def ipf_factor_numba(x, W, c, max_iters=100):
    err = np.zeros(max_iters+1)
    err[0] = np.linalg.norm(W @ x - c, ord=1)
    a = np.ones_like(c)
    A = np.ones_like(x)  # products of a's

    # Create initial vector of A sums
    nx = len(x)
    nc = len(c)

    Asum = np.zeros(nc)
    for i in range(nc):
        for j in range(nx):
            Asum[i] += A[j]*x[j]*W[i, j]

    for niter in range(max_iters):
        for i in range(nc):
            aio = a[i]
            a[i] = c[i] / (Asum[i] / a[i])

            # Update terms
            for j in range(nx):
                if W[i, j] == 0:
                    continue
                Ajo = A[j]
                A[j] = A[j] * (a[i]/aio)
                for l in range(nc):
                    if W[l, j] == 0:
                        continue
                    Asum[l] += (A[j] - Ajo)*x[j]

        delta = W @ (x * A) - c
        norm_l1 = np.linalg.norm(delta, ord=1)
        err[niter+1] = norm_l1

    return a, err


def min_norm_solve():
    return
