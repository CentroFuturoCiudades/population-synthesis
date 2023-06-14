import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from scipy.optimize import nnls
from scipy.linalg import pinv, qr
from itertools import product
import warnings
from tqdm import tqdm


def get_X(df):
    cat_cols = [
        col for col in df.columns
        if df[col].dtype == 'category'
    ]

    df_agg = df.groupby(
        cat_cols, observed=True)[['FACTOR']].sum().sort_index().reset_index()

    return df_agg


def get_w_vec(X, const):

    def get_mask(X, const):

        mask_list = []
        for col, vals in const.items():
            # Loop over columns included in the constraint
            or_list = []  # Stores mask for valid entries for col

            for val in vals:
                assert val in X[col].cat.categories, (col, val)
                if val not in X[col].values:
                    continue
                # Loop or values in the column
                or_list.append((X[col] == val).values)

            # Mask stores valid entris for particular comb of cols (AND clause)
            if len(or_list) > 0:
                mask_list.append(np.any(or_list, axis=0))
            else:
                mask_list.append(np.zeros_like(X[col]))

        mask = np.all(mask_list, axis=0)
        return mask

    mask = get_mask(X, const)

    return mask.astype(int)


def get_W(X, const_dict):
    w_dict = {}
    for k, const in const_dict.items():
        if k == 'POBTOT':
            w = np.ones(len(X), dtype=int)
        else:
            w = get_w_vec(X, const)
        w_dict[k] = w
    return pd.DataFrame(w_dict).T


def find_conf_const(W, C):
    # Find one independent set of w vectors
    mask = np.abs(np.diag(qr(W.T.values)[1])) > 1e-10
    W_ind = W.loc[mask].copy()
    W_dep = W.loc[~mask].copy()

    # Find the matrix that build dependent vectors
    # from independent vectors
    # This is a special case of non noegative
    # matrix factorization with a known factor
    A = round(W_dep @ pinv(W_ind)).astype(int)
    C_ind = C[W_ind.index]

    # Check which dependent have inconsistent constraints
    # by comparing the explicit constraints with the linear
    # combinations of independent constraints
    # Append all involve constraints to list
    conf_consts = []
    for cname, c_w in A.iterrows():
        csum = np.sum(c_w.values * C_ind.values)
        if csum != C.loc[cname]:
            conf_consts.append(cname)
            conf_consts.extend(W_ind.index[c_w.astype(bool)])
    conf_consts = set(conf_consts)

    return list(conf_consts)


def fill_zero_nn(X, C_non_zero, constraints):
    # Iterate over constrains and add missing
    # attribute combinations to the list
    X_new_list = []  # holds new or replicated attribute combinations
    constraints_new = {}
    for const_name in C_non_zero.keys():
        # Get the dictionary of col: valus for the constraint
        const_dict = constraints[const_name].copy()
        constraints_new[const_name] = const_dict

        # Find all constrined attribute combinations
        columns = list(const_dict.keys())
        attr_combs = product(*const_dict.values())

        # Find integer attr representation
        attr_combs_df = pd.DataFrame(attr_combs, columns=columns)
        attr_combs = attr_combs_df.copy()
        for col in columns:
            attr_combs[col] = attr_combs[col].astype(X[col].dtype).cat.codes
        attr_combs = attr_combs.values

        # Get only involved columns in X with integer codes
        X_arr = X[columns].copy()
        for col in columns:
            X_arr[col] = X_arr[col].cat.codes
        X_arr = X_arr.values

        # Iterate over each atribute comb and find
        # nearest neighbors in X
        X2_list = []
        # print(const_name)
        # print(attr_combs_df)
        for attr_c, attr_val in zip(attr_combs, attr_combs_df.values):
            # Get distance to the attribute combination
            dist = cdist(attr_c[None, :], X_arr, metric='hamming').ravel()

            # Get mask of nearest neighbors
            min_dist = dist.min()
            dist_mask = dist == min_dist

            # Select nearest neighbors from X
            X2 = X[dist_mask].copy()

            # Replace values in X2
            for col, val in zip(columns, attr_val):
                X2[col] = val
                X2[col] = X2[col].astype(X[col].dtype)
                assert X2[col].isna().sum() == 0
            # Collapse X
            X2 = X2.groupby(
                list(X2.columns.drop(['FACTOR'])),
                observed=True
            )[['FACTOR']].sum().reset_index()
            X2_list.append(X2)
        X2 = pd.concat(X2_list, ignore_index=True)
        assert len(X2) > 0
        X_new_list.append(X2)

    # Merge all new combs
    X_new = pd.concat(X_new_list, axis=0, ignore_index=True)
    # print(X_new.shape)
    X_new = X_new.groupby(
        list(X_new.columns.drop(['FACTOR'])),
        observed=True
    )[['FACTOR']].max().reset_index()
    # print(X_new.shape)

    # For the weights use the minimum norm solution with positivity constraints
    # ERROR, some weights are negative
    W_new = get_W(X_new, constraints_new)
    C_new = C_non_zero[W_new.index]
    factors_new, err = nnls(W_new.values, C_new.values)
    # print(len(factors_new), err, C_new, constraints_new)
    X_new['FACTOR'] = factors_new
    # Filter zeroes
    X_new = X_new[X_new.FACTOR > 0]

    # Reweight new combinations according to the contraint marginal
    # for i, const_marg in enumerate(C_non_zero.values):
    #     old_factor = X_new_list[i].FACTOR
    #     X_new_list[i]['FACTOR'] = old_factor * const_marg / old_factor.sum()

    # X_new = pd.concat([X] + X_new_list, axis=0, ignore_index=True)
    # # Collapse
    # X_new = X_new.groupby(
    #     list(X_new.columns.drop(['FACTOR'])),
    #     observed=True
    # )[['FACTOR']].sum().reset_index()

    X_new = pd.concat([X, X_new], axis=0, ignore_index=True)
    # Collapse, needed only when fixing conflicting contraints
    # when dealing with zero constraints this has no effect
    X_new = X_new.groupby(
        list(X_new.columns.drop(['FACTOR'])),
        observed=True
    )[['FACTOR']].first().reset_index()

    return X_new


def fill_zero_from_global(X, W, C, constraints, X_full):

    # Identify zero cell problems as zero weight vectors
    # with non-zero constraints
    W_zero = W.T.sum()[W.T.sum() == 0]
    C_non_zero = C.loc[W_zero.index]
    C_non_zero = C_non_zero[C_non_zero > 0]

    # Iterate over constrains and add missing
    # attribute combinations to the list
    X_new_list = []  # holds new or replicated attribute combinations
    for const_name in C_non_zero.keys():
        # Get the dictionary of col: valus for the constraint
        const_dict = constraints[const_name].copy()

        # Method 1: Look for existing combinations in global X
        query_str = ' & '.join(
            [f'{col} in @const_dict["{col}"]' for col in const_dict.keys()]
        )
        X2 = X_full.query(query_str).reset_index(drop=True)
        assert len(X2) > 0
        X_new_list.append(X2)

    # Reweight new combinations according to the contraint marginal
    for i, const_marg in enumerate(C_non_zero.values):
        old_factor = X_new_list[i].FACTOR
        X_new_list[i]['FACTOR'] = old_factor * const_marg / old_factor.sum()

    return pd.concat([X] + X_new_list, axis=0, ignore_index=True)


def setup_ls(df_survey_dict, df_census, constraints):
    XWC_dict = {}

    # personas_cat_full = pd.concat(df for df in df_survey_dict.values())
    # X_full = get_X(personas_cat_full)

    for i, (mun, df) in tqdm(enumerate(df_survey_dict.items())):
        # if mun != 'Pesquería': continue
        print(mun)
        X = get_X(df)
        W = get_W(X, constraints)
        C = df_census.loc[mun][W.index].copy()

        # Fill zero cells with non-zero constraints in X
        # Identify zero cell problems as zero weight vectors
        # with non-zero constraints
        W_zero = W.T.sum()[W.T.sum() == 0]
        C_non_zero = C.loc[W_zero.index]
        C_non_zero = C_non_zero[C_non_zero > 0]
        if len(C_non_zero) > 0:
            print('Filling ...')
            X = fill_zero_nn(X, C_non_zero, constraints)
            W = get_W(X, constraints)
            C = df_census.loc[mun][W.index].copy()
            print('Done.')

        # Drop zero constrainst with all zeroes in W
        # W_zero = W.T.sum()[W.T.sum() == 0]
        # C_non_zero = C.loc[W_zero.index]
        # assert (C_non_zero > 0).sum() == 0, mun
        # C_zero = C_non_zero[C_non_zero == 0]
        # C_non_zero = C_non_zero[C_non_zero > 0]
        # C = C.drop(C_zero.index)
        # W = W.drop(C_zero.index)

        # TODO: keep only a set of linearly independent rows in W

        XWC_dict[mun] = {'X': X, 'W': W, 'C': C}
        # if i == 17: break

    return XWC_dict