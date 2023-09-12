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


def fill_zero_h(
        mun_dest, XWC_dict, consts,
        constraints_ind, constraints_viv,
        personas_cat, viviendas_cat,
        df_mun
):
    # consts = XWC_dict[mun_dest]['zero_nozero'].index
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


def make_init_dict(personas_cat, viviendas_cat,
                   df_mun,
                   constraints_ind, constraints_viv,
                   out_path,
                   force=False):

    fpath = out_path / 'XWC_init.pickle'
    if fpath.exists() and not force:
        print('Loading initial dict.')
        with open(fpath, 'rb') as f:
            XWC_dict = pickle.load(f)
        return XWC_dict

    XWC_dict = {}
    print('Building initial dict ... ')
    for mun in personas_cat.keys():
        print(f'    {mun} ... ', end='')
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

    # IMPORTANT NOTE / TODO:
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

    # Save initial dict to disk
    with open(fpath, 'wb') as f:
        pickle.dump(XWC_dict, f)

    return XWC_dict


def fix_zero_cell(XWC_dict,
                  personas_cat, viviendas_cat,
                  df_mun,
                  constraints_ind, constraints_viv,
                  out_path,
                  force=False):

    fpath = out_path / 'XWC_fill.pickle'
    if fpath.exists() and not force:
        print('Loading zero filled dict.')
        with open(fpath, 'rb') as f:
            XWC_ext = pickle.load(f)
        return XWC_ext

    print('Filling zero cell problems ... ')
    XWC_ext = {}
    for mun in XWC_dict.keys():
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
                consts,
                constraints_ind, constraints_viv,
                personas_cat, viviendas_cat,
                df_mun)

        zero_nozero = find_zero_nozero_const(U_ext, C_ext)
        assert len(zero_nozero) == 0, zero_nozero

        XWC_ext[mun] = {}
        XWC_ext[mun]['X'] = X_ext
        XWC_ext[mun]['Y'] = Y_ext
        XWC_ext[mun]['U'] = U_ext
        XWC_ext[mun]['C'] = C_ext

        Y = XWC_dict[mun]['Y']
        print(f'Added {len(Y_ext) - len(Y)} extra households.')

        conf_consts = find_conf_const(U_ext, C_ext)
        XWC_ext[mun]['conf_consts'] = conf_consts

    # Save initial dict to disk
    with open(fpath, 'wb') as f:
        pickle.dump(XWC_ext, f)

    return XWC_ext


def are_people(cols, X):
    col_test = [c in X.columns for c in cols]
    all_people = np.all([c in X.columns for c in cols])
    all_viv = np.all([c not in X.columns for c in cols])
    if all_people:
        return True
    elif all_viv:
        return False
    else:
        raise NotImplementedError


def get_cat_dicts(X, viviendas):
    # Get a dictionary with all possible columns categories.
    cat_personas = {}
    for col in X.columns:
        if col == 'FACTOR':
            continue
        cat_personas[col] = X[col].cat.categories.tolist()

    cat_viviendas = {}
    for col in viviendas.columns:
        if viviendas[col].dtype != 'category':
            continue
        cat_viviendas[col] = viviendas[col].cat.categories.tolist()
    cat_personas.update(cat_viviendas)
    return cat_personas
