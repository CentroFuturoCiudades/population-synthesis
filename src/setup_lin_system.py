import numpy as np
import pandas as pd
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


def fill_zero(X, W, C, constraints, X_full):

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
        if len(X2) > 0:
            # print(f'Filling for {const_name} with method 1.')
            X_new_list.append(X2)
            continue

        # Method 2: Replicate nearest neighbors in current X
        # Check if any column have presence in current X
        cols_to_query = [
            col for col, vals in const_dict.items()
            if X[col].isin(vals).any()
        ]
        if len(cols_to_query) > 0:
            warnings.warn(f'Filling for {const_name} by replicating, '
                          'structural zeroes may have been incorrectly filled.')
            query_str = ' & '.join(
                [f'{col} in @const_dict["{col}"]' for col in cols_to_query]
            )
            X2 = X_full.query(query_str).reset_index(drop=True)
            X_new_list.append(X2)
            continue

        # Method 3: Replicate full X table replacing involved columns values
        # Get a list of combinations involved in the constraint
        warnings.warn(f'Filling for {const_name} by replicating, '
                      'structural zeroes may have been incorrectly filled.')
        columns = list(const_dict.keys())
        attr_combs = product(*const_dict.values())
        X2_list = []
        for attr_c in attr_combs:
            # Replace values in X
            X2 = X.copy()
            for col, val in zip(columns, attr_c):
                X2[col] = val
                X2[col] = X2[col].astype(X[col].dtype)
            # Collapse X
            X2 = X2.groupby(
                list(X2.columns.drop(['FACTOR'])),
                observed=True
            )[['FACTOR']].sum().reset_index()
            X2_list.append(X2)
        X2 = pd.concat(X2_list, ignore_index=True)
        assert len(X2) > 0
        X_new_list.append(X2)

    # Reweight new combinations according to the contraint marginal
    for i, const_marg in enumerate(C_non_zero.values):
        old_factor = X_new_list[i].FACTOR
        X_new_list[i]['FACTOR'] = old_factor * const_marg / old_factor.sum()

    return pd.concat([X] + X_new_list, axis=0, ignore_index=True)


def setup_ls(df_survey_dict, df_census, constraints):
    XWC_dict = {}

    personas_cat_full = pd.concat(df for df in df_survey_dict.values())
    X_full = get_X(personas_cat_full)

    for mun, df in tqdm(df_survey_dict.items()):
        X = get_X(df)
        W = get_W(X, constraints)
        C = df_census.loc[mun][W.index].copy()

        # Fill zero cells with non-zero constraints in X
        X = fill_zero(X, W, C, constraints, X_full)
        W = get_W(X, constraints)
        C = df_census.loc[mun][W.index].copy()

        # Drop zero constrainst with all zeroes in W
        W_zero = W.T.sum()[W.T.sum() == 0]
        C_non_zero = C.loc[W_zero.index]
        C_zero = C_non_zero[C_non_zero == 0]
        C_non_zero = C_non_zero[C_non_zero > 0]
        C = C.drop(C_zero.index)
        W = W.drop(C_zero.index)

        # TODO: keep only a set of linearly independent rows in W

        XWC_dict[mun] = {'X': X, 'W': W, 'C': C}

    return XWC_dict
