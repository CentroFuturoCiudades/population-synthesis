import numpy as np
from numba import njit


@njit
def grake(d, X, t, maxiters=1):
    # Start with initial guess for g weights and
    # lagrange multipliers
    w = d.copy()
    l = np.zeros(t.shape)

    for i in range(maxiters):
        # The function to solve is
        f = X.T @ w - t

        # Get Jacobian
        J = get_J(l, w, X)

        # Apply Newton's method
        l = l - np.linalg.pinv(J) @ f

        w = d * np.exp(X @ l)

    return w


@njit
def get_J(l, w, X):

    # N is the number of observations
    # M is the number of constraints(lambdas)
    N = w.shape[0]
    M = l.shape[0]
    J = np.zeros((M, M), dtype=float)

    # w = d * np.exp(X @ l)

    for i in range(M):
        for j in range(M):
            Jij = 0
            for n in range(N):
                Jij += X[n, i] * X[n, j] * w[n]
            J[i, j] = Jij

    return J
