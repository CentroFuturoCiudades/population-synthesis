import numpy as np
from scipy import stats


def binned_ll(boundaries, counts, distribution, Ctrunc=1):
    """ Returns the log likelihood of binned data
    for distribution. """

    return np.sum(
        counts * np.log(
            np.diff(distribution.cdf(boundaries))/Ctrunc
        )
    )


def ks_distance(cdf1, cdf2):
    """ Computes the KS distance between two empirical CDFs. """

    assert cdf1.shape == cdf2.shape

    diff = np.abs(cdf1 - cdf2)

    return diff.max()


def fit_score_p(boundaries, counts, distribution, fitting_f, mat_eng,
                bmin, bmax=np.inf,
                reps=1000, rng=None,
                inv_samp=False):
    """ Find the bootstraped p-value for goodness of fit.
    Based on the Kolmogorov statistic.
    """
    if rng is None:
        rng = np.random.default_rng()

    bmin_idx = np.where(boundaries == bmin)[0][0]
    Nbmin = counts[bmin_idx:].sum()

    # Find the cumulative distributions above bmin
    ecdf = np.cumsum(counts[bmin_idx:])/Nbmin

    # We must adjust the cdf to the truncated dist
    # to compare above bmin
    cdf = (
        (distribution.cdf(boundaries[bmin_idx:]) - distribution.cdf(bmin))
        / (distribution.cdf(bmax) - distribution.cdf(bmin))
    )

    # Find the ks distance above bmin
    Dstar = ks_distance(ecdf, cdf[1:])

    # generate reps bootstraped samples from dist
    # We want to compare the fit just above bmin,
    # in the fitted region.
    # In this case we always use trunceted distributions
    if inv_samp:
        # use inverse sampling to sample from truncated dist
        urvs = rng.uniform(
            low=distribution.cdf(bmin),
            high=distribution.cdf(bmax),
            size=(reps, Nbmin)
        )
        bs = distribution.ppf(urvs)
    else:
        bs = distribution.rvs(size=(reps, Nbmin))

    # Fit distribution to samples
    ds = np.zeros(reps, dtype=float)
    for i, sample in enumerate(bs):
        # Bin the data
        bs_counts = np.histogram(sample, boundaries)[0]

        # Fit model
        bs_dist = fitting_f(
            mat_eng, boundaries, bs_counts, bmin, verbose=False
        )

        # Get cdf and the ecfd
        bs_cdf = (
            (bs_dist.cdf(boundaries[bmin_idx:]) - bs_dist.cdf(bmin))
            / (bs_dist.cdf(bmax) - bs_dist.cdf(bmin))
        )
        bs_ecdf = np.cumsum(bs_counts[bmin_idx:])/Nbmin

        # Find KS statistic
        ds[i] = ks_distance(bs_ecdf, bs_cdf[1:])

    # Compare with Dstar
    p = np.sum(ds >= Dstar)/reps

    return p, ds, Dstar
