import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from scipy.optimize import nnls
from scipy.linalg import pinv, qr
from itertools import product
import warnings
from tqdm import tqdm


def check_solvable(W, C):
    WC = np.column_stack([W, C])

    # print(np.linalg.matrix_rank(W), np.linalg.matrix_rank(WC))
    solvable = np.linalg.matrix_rank(W) == np.linalg.matrix_rank(WC)

    return solvable


def get_X(df):
    cat_cols = [
        col for col in df.columns
        if df[col].dtype == 'category'
    ]

    df_agg = df.groupby(
        cat_cols, observed=True)[['FACTOR']].sum().sort_index().reset_index()

    return df_agg


def get_X_I(df):
    cat_cols = [
        col for col in df.columns
        if df[col].dtype == 'category'
    ]

    df_agg = df.groupby(
        cat_cols,
        observed=True
    )[['FACTOR', 'ID_VIV']].apply(
        lambda df: (list(df.FACTOR), list(df.ID_VIV))
    ).sort_index().reset_index()

    df_agg['FACTOR'] = [sum(x[0]) for x in df_agg[0]]
    df_agg['ID_VIV'] = [x[1] for x in df_agg[0]]
    df_agg['F_LIST'] = [x[0] for x in df_agg[0]]
    df_id_viv = df_agg.drop(columns=[0, 'FACTOR'])
    df_agg = df_agg.drop(columns=[0, 'ID_VIV', 'F_LIST'])

    index = np.sort(np.unique(np.concatenate(df_id_viv.ID_VIV)))
    columns = df_agg.index
    I = pd.DataFrame(
        np.zeros((len(index), len(columns)), dtype=int),
        index=index,
        columns=columns)

    for idx, row in df_id_viv.iterrows():
        for f, idv in zip(row.F_LIST, row.ID_VIV):
            # Households have their own expansion factor
            # Its the same as the one found on the people table
            # So just add 1 per person in household
            I.loc[idv, idx] += 1

    return df_agg, I


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
    return pd.DataFrame(w_dict, index=X.index).T


def find_conf_const(W, C):
    # Find one independent set of w vectors
    rank = np.linalg.matrix_rank(W)

    # r, P = qr(W.T.values, mode='r', pivoting=True)
    # assert (abs(np.diag(r)) > 1e-10).sum() == rank
    # W_ind = W.iloc[P[:rank]].copy()
    # W_dep = W.iloc[P[rank:]].copy()
    # assert np.linalg.matrix_rank(W_ind) == rank

    mask = np.abs(np.diag(qr(W.T.values)[1])) > 1e-10
    W_ind = W.loc[mask].copy()
    W_dep = W.loc[~mask].copy()
    assert np.linalg.matrix_rank(W_ind) == rank

    # W_sorted = list(W.sum(axis=1).sort_values(ascending=False).index)
    # work_arr = np.zeros_like(W)
    # curr_w = W_sorted[0]
    # work_arr[0, :] = W.loc[curr_w].values
    # ind_set = [curr_w]
    # dep_set = []
    # prank = np.linalg.matrix_rank(work_arr)
    # idx = 1
    # for curr_w in W_sorted:
    #     work_arr[idx, :] = W.loc[curr_w].values
    #     crank = np.linalg.matrix_rank(work_arr[:idx+1])
    #     if crank == prank:
    #         dep_set.append(curr_w)
    #     else:
    #         ind_set.append(curr_w)
    #         prank = crank
    #         idx += 1
    # W_ind = W.loc[ind_set]
    # W_dep = W.loc[dep_set]

    A = round(W_dep @ pinv(W_ind), 5)
    C_ind = C[W_ind.index].astype(int)

    # Check which dependent have inconsistent constraints
    # by comparing the explicit constraints with the linear
    # combinations of independent constraints
    # Append all involve constraints to list
    conf_consts = []
    for cname, c_w in A.iterrows():
        csum = round(np.sum(c_w.values * C_ind.values))
        if csum != C.loc[cname]:
            # print(cname)
            conf_consts.append(cname)
            conf_consts.extend(W_ind.index[c_w.astype(bool)])
    conf_consts = set(conf_consts)

    return list(conf_consts)#, rank, A, C_ind, W_ind, W_dep


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
    # Filter zeroes and small values
    X_new = X_new[X_new.FACTOR > 1e-10]

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

    for mun, df in df_survey_dict.items():
        if mun != 'Cerralvo': continue
        print(mun)

        # Get an initial linear system
        X = get_X(df)
        W = get_W(X, constraints)
        C = df_census.loc[mun][W.index].copy()
        print(f'    X has {len(X)} entries.')

        # Fill zero cells with non-zero constraints in X
        # Identify zero cell problems as zero weight vectors
        # with non-zero constraints
        W_zero = W.T.sum()[W.T.sum() == 0]
        C_non_zero = C.loc[W_zero.index]
        C_non_zero = C_non_zero[C_non_zero > 0]
        if len(C_non_zero) > 0:
            print('    Filling zeroes ...')
            X = fill_zero_nn(X, C_non_zero, constraints)
            W = get_W(X, constraints)
            C = df_census.loc[mun][W.index].copy()
            print(f'    X has {len(X)} entries.')

        # Find conflicting constraints
        while not check_solvable(W, C):
            print('    Solving conflicts ...')
            conf_const = find_conf_const(W, C)
            C_conf = C[conf_const]
            X = fill_zero_nn(X, C_conf, constraints)
            W = get_W(X, constraints)
            C = df_census.loc[mun][W.index].copy()
            print(f'    X has {len(X)} entries.')

        # Drop zero constrainst with all zeroes in W
        W_zero = W.T.sum()[W.T.sum() == 0]
        C_non_zero = C.loc[W_zero.index]
        assert (C_non_zero > 0).sum() == 0, mun
        C_zero = C_non_zero[C_non_zero == 0]
        C_non_zero = C_non_zero[C_non_zero > 0]
        C = C.drop(C_zero.index)
        W = W.drop(C_zero.index)

        # Set X->0 for C=0, remove them from X and C
        # This type of constraints may also appear implicitly
        # as a combination of other constraints.
        # In such cases the rate of convergende of IPF is
        # greatly affected since the involve X will converge to
        # 0 increasily slowly.
        # Consider the example of two contraints with x1 and x2:
        # C1 = x1 + x2 = 1, C2 = x1 = 1, Implicit Ci = x2 = 0.
        # But without Ci x1 converges as x1 = x1/(1+x1), which
        # slows down as x1 approaches 0.
        C_zero = C[C == 0]
        W_to_zero = W.loc[C_zero.index]
        to_drop = (W_to_zero.values).sum(axis=0) > 0
        X = X[~to_drop]
        W = W.drop(index=C_zero.index, columns=list(np.nonzero(to_drop)[0]))
        C = C.drop(C_zero.index)

        # Keep only a set of linearly independent rows in W
        # One the conflicting constraints have been solved,
        # dependent contraints are redundant
        # NOTE: this really hurts IPF convergence speed
        # it seems IPF is really bad at handling implicit constraints
        # and really needs a full set ox explicit constraitns, even if
        # redudant from the point of view of the linear system.
        # Yet full row rank is needed for constrained least square
        # solutions.
        # rank = np.linalg.matrix_rank(W.values)
        # r, P = qr(W.T.values, mode='r', pivoting=True)
        # W = W.iloc[P[:rank]].copy()
        # assert np.linalg.matrix_rank(W) == rank
        # C = df_census.loc[mun][W.index].copy()

        assert check_solvable(W, C), mun

        XWC_dict[mun] = {'X': X, 'W': W, 'C': C}
        # if i == 17: break

    return XWC_dict
