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


def get_X_I_fast(df):
    df = df.copy()

    cat_cols = [
            col for col in df.columns
            if df[col].dtype == 'category'
    ]

    # Map ID_VIV to integers for fast indexing
    index = np.sort(np.unique(df.ID_VIV.values))
    id_map = {id_viv: i for i, id_viv in enumerate(index)}
    df['ID_VIV'] = df.ID_VIV.map(id_map)

    df_agg = df.groupby(
        cat_cols,
        observed=True
    )[['FACTOR', 'ID_VIV']].apply(
        lambda df: (list(df.FACTOR), list(df.ID_VIV))
    ).sort_index().reset_index()

    # Create an aggregated factor column
    df_agg['FACTOR'] = [sum(x[0]) for x in df_agg[0]]

    # Create a dedicaded columns for id list and factor list
    df_agg['ID_VIV'] = [x[1] for x in df_agg[0]]
    df_agg['F_LIST'] = [x[0] for x in df_agg[0]]

    # Create people dataframe and auxiliary df for I
    df_id_viv = df_agg.drop(columns=[0, 'FACTOR'])
    df_agg = df_agg.drop(columns=[0, 'ID_VIV', 'F_LIST'])

    columns = df_agg.index
    I_ar = np.zeros((len(index), len(columns)), dtype=np.uint8)
    for idx, idv in df_id_viv.ID_VIV.items():
        np.add.at(I_ar, (idv, idx), 1)

    I = pd.DataFrame(
        I_ar,
        index=index,
        columns=columns)

    return df_agg, I


def get_X_I(df):

    # Use only categorical columns
    cat_cols = [
        col for col in df.columns
        if df[col].dtype == 'category'
    ]

    # Create aggregated data frame wit cat cols and
    # a list of factors and ID_VIV per class
    # Sort index to speed up searches
    df_agg = df.groupby(
        cat_cols,
        observed=True
    )[['FACTOR', 'ID_VIV']].apply(
        lambda df: (list(df.FACTOR), list(df.ID_VIV))
    ).sort_index().reset_index()

    # Create an aggregated factor column
    df_agg['FACTOR'] = [sum(x[0]) for x in df_agg[0]]

    # Create a dedicaded columns for id list and factor list
    df_agg['ID_VIV'] = [x[1] for x in df_agg[0]]
    df_agg['F_LIST'] = [x[0] for x in df_agg[0]]

    # Create people dataframe and auxiliary df for I
    df_id_viv = df_agg.drop(columns=[0, 'FACTOR'])
    df_agg = df_agg.drop(columns=[0, 'ID_VIV', 'F_LIST'])
    index = np.sort(np.unique(np.concatenate(df_id_viv.ID_VIV)))
    columns = df_agg.index
    I = pd.DataFrame(
        np.zeros((len(index), len(columns)), dtype=int),
        index=index,
        columns=columns)
    for i, (idx, row) in enumerate(df_id_viv.iterrows()):
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


def get_W(X, const_dict, ignore=[]):
    w_dict = {}
    for k, const in const_dict.items():
        if k in ignore:
            continue
        if k == 'POBTOT':
            w = np.ones(len(X), dtype=int)
        else:
            w = get_w_vec(X, const)
        w_dict[k] = w
    W = pd.DataFrame(w_dict, index=X.index).T

    return W.astype(np.uint8)


def find_conf_const(W, C):

    W = W.astype(float)
    C = C.astype(float)
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


def find_zero_nozero_const(W, C):
    W_zero = W.T.sum()[W.T.sum() == 0]
    C_non_zero = C.loc[W_zero.index]
    C_non_zero = C_non_zero[C_non_zero > 0]

    return C_non_zero


def find_nonzero_zero_const(W, C):
    W_nonzero = W.T.sum()[W.T.sum() > 0]
    C_zero = C.loc[W_nonzero.index]
    C_zero = C_zero[C_zero == 0]

    return C_zero


def get_matrices(personas, viviendas,
                 constraints_ind, constraints_viv,
                 census_series):

    # People linear system
    X, I = get_X_I_fast(personas)
    # The people weight matrix
    W = get_W(X, constraints_ind)

    # The household weight matrix can be obtaibed in blocks
    # We work on the non aggregated household table
    # The household weight matrix for household constraints
    Uh = get_W(viviendas, constraints_viv)
    # The household weight matrix for person level constraints
    Up = (W @ I.T)
    U = pd.concat([Uh, Up])
    # For Y, we need to concatenate the I matrix
    Y = pd.concat([viviendas, I], axis=1)

    C = census_series.loc[U.index]

    return X, I, W, U, Y, C


def find_zero_cell_global(personas_full, viviendas_full,
                          constraints_ind, constraints_viv):
    consts = []

    X_full = get_X(personas_full)
    W_full = get_W(X_full, constraints_ind)
    C_full = W_full @ X_full.FACTOR.values
    consts += C_full[C_full == 0].index.tolist()

    Uh_full = get_W(viviendas_full, constraints_viv)
    C_full_viv = Uh_full @ viviendas_full.FACTOR.values
    consts += C_full_viv[C_full_viv == 0].index.tolist()

    return consts


def replace_mun(df, mun_col, mun_orig, mun_dest):
    muntype = df[mun_col].dtype
    df[mun_col] = df[mun_col].where(
        df[mun_col].isin(
            [
                mun_orig,
                'Blanco por pase', 'No especificado',
                'OtroPais', 'OtraEnt'
            ]
        ),
        'No especificado'
    )
    df[mun_col] = df[mun_col].replace(mun_orig, mun_dest)
    df[mun_col] = df[mun_col].astype(muntype)


def fill_zero_h(mun_dest, XWC_dict, constraints_ind, constraints_viv,
                personas_cat, viviendas_cat, df_mun):
    consts = XWC_dict[mun_dest]['zero_nozero'].index
    assert len(consts) > 0

    query = ' | '.join([f'{const} > 0' for const in consts])
    viviendas_ext_l = []
    personas_ext_l = []

    mun_type = XWC_dict[mun_dest]['X'].MUN.dtype

    # Loop over municipalities
    for mun, mun_dict in XWC_dict.items():
        # Skip current, we know there are no matches
        if mun == mun_dest:
            continue

        # Extract current valurs
        X = mun_dict['X']
        I = mun_dict['I']
        Y = mun_dict['Y']
        U = mun_dict['U']

        # Get household IDs using the U weight matrix
        viv_ids = U.T.query(query).index
        if len(viv_ids) == 0:
            continue

        # Extract list of households, remove I part of dataframe
        viviendas_ext = Y.loc[viv_ids].copy().select_dtypes(
            include=['int64', 'category'])
        viviendas_ext['MUN'] = mun_dest
        viviendas_ext['MUN'] = viviendas_ext['MUN'].astype(Y.MUN.dtype)
        viviendas_ext_l.append(viviendas_ext)

        # Get people IDs using the I matrix
        viv_ids, p_ids = np.array(
            I.loc[viv_ids][I.loc[viv_ids] > 0].stack().index.tolist()).T

        # Reconstruct people list with viv id
        personas_ext = X.loc[p_ids].copy()
        personas_ext['ID_PERSONA'] = 0
        personas_ext['ID_VIV'] = viv_ids
        personas_ext['MUN'] = mun_dest
        personas_ext['MUN'] = personas_ext['MUN'].astype(mun_type)
        replace_mun(personas_ext, 'MUN_TRAB', mun, mun_dest)
        replace_mun(personas_ext, 'MUN_ASI', mun, mun_dest)
        replace_mun(personas_ext, 'MUN_RES_5A', mun, mun_dest)

        personas_ext['TIE_TRASLADO_ESCU'] = personas_ext[
            'TIE_TRASLADO_ESCU'
        ].where(
            personas_ext['TIE_TRASLADO_ESCU'].isin(
                ['No se traslada', 'No especificado', 'Blanco por pase']
            ),
            'No especificado'
        )

        personas_ext['TIE_TRASLADO_TRAB'] = personas_ext[
            'TIE_TRASLADO_TRAB'
        ].where(
            personas_ext['TIE_TRASLADO_TRAB'].isin(
                [
                    'No se traslada', 'No especificado',
                    'Blanco por pase', 'No es posible determinarlo'
                ]
            ),
            'No especificado'
        )

        personas_ext_l.append(personas_ext)

    # Merge dfs
    personas_ext = pd.concat(personas_ext_l)
    viviendas_ext = pd.concat(viviendas_ext_l)

    # Adjust weights using a restricted problem
    # The nnls solution is sparse, which leads to
    # a minimal addition to the original seed
    # Note selection bias may be introduced.
    # Consider adding all entries equally distributing weights.
    constraints_ind_r = {
        k: v for k, v in constraints_ind.items()
        if k in consts
    }
    constraints_viv_r = {
        k: v for k, v in constraints_viv.items()
        if k in consts
    }

    X_r, I_r, W_r, U_r, Y_r, C_r = get_matrices(
        personas_ext, viviendas_ext,
        constraints_ind_r, constraints_viv_r,
        df_mun.loc[mun_dest]
    )

    factors_new, err = nnls(U_r.values.astype(float), C_r)
    # Replace household factor values.
    # People factors are never used and can be ignored.
    assert np.all(Y_r.index == viviendas_ext.index)
    viviendas_ext['FACTOR'] = factors_new
    # Filter data frames
    viviendas_ext = viviendas_ext[viviendas_ext.FACTOR > 1e-10]
    personas_ext = personas_ext[personas_ext.ID_VIV.isin(viviendas_ext.index)]

    # Merge with full dataframes
    personas_ext = pd.concat(
        [personas_cat[mun_dest], personas_ext],
        ignore_index=True
    )
    viviendas_ext = pd.concat(
        [viviendas_cat[mun_dest], viviendas_ext],
        ignore_index=False
    )

    # Create new extended matrices
    X_ext, I_ext, W_ext, U_ext, Y_ext, C_ext = get_matrices(
        personas_ext, viviendas_ext,
        constraints_ind, constraints_viv,
        df_mun.loc[mun_dest]
    )

    return X_ext, I_ext, W_ext, U_ext, Y_ext, C_ext


def setup_ls(personas_cat, viviendas_cat,
             df_mun,
             constraints_ind, constraints_viv,
             ignore_cols_p=[],
             ignore_cols_v=[],
             verbose=True):
    XWC_dict = {}

    # Setup list of ignored constraints
    ignore_const_p = []
    for col in ignore_cols_p:
        for const, coldict in constraints_ind.items():
            if col in coldict.keys():
                ignore_const_p.append(const)
    ignore_const_p = set(ignore_const_p)

    ignore_const_v = []
    for col in ignore_cols_v:
        for const, coldict in constraints_viv.items():
            if col in coldict.keys():
                ignore_const_v.append(const)
    ignore_const_v = set(ignore_const_v)

    # Build initial dict
    print('Building initial dict ... ')
    for mun in personas_cat.keys():
        print(f'    {mun} ...', end='')
        personas = personas_cat[mun]
        viviendas = viviendas_cat[mun]

        X, I, W, U, Y, C = get_matrices(
            personas, viviendas,
            constraints_ind, constraints_viv,
            df_mun.loc[mun]
        )

        # Find zero cell problems
        zero_nozero = find_zero_nozero_const(U, C)

        XWC_dict[mun] = {'X': X, 'I': I, 'W': W,
                         'Y': Y, 'U': U, 'C': C,
                         'zero_nozero': zero_nozero}

        print('Done.')

    # IMPORTANT NOTE:
    # TODO
    # Nuevo León have global zero cell problem for the constraint
    # P34HLI_NHE involving EDAD=3-4 and HLENGUA=Si/No español
    # We create an artifical set of households using neares neighbor
    # imputation as to fill the zero cells.
    # This process is note yet automatized for households and
    # specifically for HLENGUA we need to split the columns again into
    # HLENGUA and HESPANOL
    # We give priority to No especificado neighbors over other
    # neighbors.
    # To identify the global zero cells use the find_zero_cell_global
    # function.

    personas_full = pd.concat(personas_cat.values())
    viviendas_full = pd.concat(viviendas_cat.values())

    viv_imp_ids = personas_full.query(
        'EDAD == "3-4" & HLENGUA == "Sí/No especificado"'
    ).ID_VIV.unique()

    personas_imp = personas_full[personas_full.ID_VIV.isin(viv_imp_ids)].copy()
    personas_imp['MUN'] = 'IMPUTED'
    personas_imp['MUN'] = personas_imp.MUN.astype('category')
    personas_imp['HLENGUA'] = personas_imp.HLENGUA.replace(
        'Sí/No especificado', 'Sí/No español'
    ).astype(personas_full.HLENGUA.dtype)

    viviendas_imp = viviendas_full.loc[viv_imp_ids]

    viv_imp_ids_map = {
        vid: 500000000000 + i
        for i, vid in enumerate(viv_imp_ids)
    }
    personas_imp['ID_VIV'] = personas_imp.ID_VIV.map(viv_imp_ids_map)

    viviendas_imp.index = viviendas_imp.index.map(viv_imp_ids_map)

    X_imp, I_imp, W_imp, U_imp, Y_imp, C_imp = get_matrices(
                personas_imp, viviendas_imp,
                constraints_ind, constraints_viv,
                df_mun.sum()
            )

    XWC_dict['IMPUTED'] = {'X': X_imp, 'I': I_imp, 'W': W_imp,
                           'Y': Y_imp, 'U': U_imp, 'C': C_imp}

    # Second loop to fix zero cell problems
    print('Filling zero cell problems ... ')
    for mun in personas_cat.keys():
        if mun == 'IMPUTED':
            continue

        print(f'    {mun} ...', end='')
        consts = XWC_dict[mun]['zero_nozero'].index
        if len(consts) == 0:
            Y_ext = XWC_dict[mun]['Y']
            U_ext = XWC_dict[mun]['U']
            C_ext = XWC_dict[mun]['C']
        else:
            X_ext, I_ext, W_ext, U_ext, Y_ext, C_ext = fill_zero_h(
                mun,
                XWC_dict,
                constraints_ind, constraints_viv,
                personas_cat, viviendas_cat,
                df_mun)

        zero_nozero = find_zero_nozero_const(U_ext, C_ext)
        assert len(zero_nozero) == 0, zero_nozero

        XWC_dict[mun]['Y_ext'] = Y_ext
        XWC_dict[mun]['U_ext'] = U_ext
        XWC_dict[mun]['C_ext'] = C_ext

        Y = XWC_dict[mun]['Y']
        print(f'Added {len(Y_ext) - len(Y)} extra households.')

        conf_consts = find_conf_const(U_ext, C_ext)
        XWC_dict[mun]['conf_consts'] = conf_consts

    # Third loop to fix conflicts among constraints

        # if verbose:
            # print(f'    Solvable: {check_solvable(U_ext, C_ext)}')
            # print()
            # print('Non-zero-zero constraints: ')
            # print(find_nonzero_zero_const(U, C))
            # print()
            # C = df_mun.loc[mun]
            # assert C.POBHOG == C.OCUPVIVPAR
            # assert C.TOTHOG == C.TVIVPARHAB
            # print(f'Total people: {C.POBTOT}\n'
            #       f'people in particular dwelligns: {C.POBHOG}\n'
            #       f'people in collective dwellings: {C.POBTOT - C.POBHOG}')
            # print(f'Particular+Collective dwellings: {C.TVIVHAB}\n'
            #       f'Total collective dwellings: {C.TVIVHAB - C.TVIVPARHAB}\n'
            #       f'Total particular dwellings/households (1 household per dwelling): {C.TVIVPARHAB}\n'
            #       f'Particular with characteristics: {C.VIVPARH_CV}. Controlled by census constraints.\n'
            #       f'Particular without characteristics: {C.TVIVPARHAB - C.VIVPARH_CV}.'
            #       )

        # Fill zero cells with non-zero constraints in X
        # Identify zero cell problems as zero weight vectors
        # with non-zero constraints
        # W_zero = W.T.sum()[W.T.sum() == 0]
        # C_non_zero = C.loc[W_zero.index]
        # C_non_zero = C_non_zero[C_non_zero > 0]
        # if len(C_non_zero) > 0:
        #     print('    Filling zeroes ...')
        #     X = fill_zero_nn(X, C_non_zero, constraints)
        #     W = get_W(X, constraints)
        #     C = df_census.loc[mun][W.index].copy()
        #     print(f'    X has {len(X)} entries.')

        # # Find conflicting constraints
        # while not check_solvable(W, C):
        #     print('    Solving conflicts ...')
        #     conf_const = find_conf_const(W, C)
        #     C_conf = C[conf_const]
        #     X = fill_zero_nn(X, C_conf, constraints)
        #     W = get_W(X, constraints)
        #     C = df_census.loc[mun][W.index].copy()
        #     print(f'    X has {len(X)} entries.')

        # # Drop zero constrainst with all zeroes in W
        # W_zero = W.T.sum()[W.T.sum() == 0]
        # C_non_zero = C.loc[W_zero.index]
        # assert (C_non_zero > 0).sum() == 0, mun
        # C_zero = C_non_zero[C_non_zero == 0]
        # C_non_zero = C_non_zero[C_non_zero > 0]
        # C = C.drop(C_zero.index)
        # W = W.drop(C_zero.index)

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
        # C_zero = C[C == 0]
        # W_to_zero = W.loc[C_zero.index]
        # to_drop = (W_to_zero.values).sum(axis=0) > 0
        # X = X[~to_drop]
        # W = W.drop(index=C_zero.index, columns=list(np.nonzero(to_drop)[0]))
        # C = C.drop(C_zero.index)

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

        # assert check_solvable(W, C), mun

    return XWC_dict
