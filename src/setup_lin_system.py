import numpy as np
import pandas as pd
# from scipy.spatial.distance import cdist
from scipy.optimize import nnls
from scipy.linalg import pinv, qr
import sparse
# from itertools import product
# import pickle
from collections import defaultdict


def check_solvable(W, C):
    WC = np.column_stack([W, C])

    # print(np.linalg.matrix_rank(W), np.linalg.matrix_rank(WC))
    solvable = np.linalg.matrix_rank(W) == np.linalg.matrix_rank(WC)

    return solvable


def make_init_system(personas, viviendas,
                     constraints_ind, constraints_viv,
                     df_mun):

    personas = personas.copy()
    viviendas = viviendas.copy()

    # Get X
    cat_cols = [
        col for col in personas.columns
        if personas[col].dtype == 'category'
    ]

    X = personas.reset_index().groupby(
        cat_cols,
        observed=True
    ).agg(
        {
            'FACTOR': 'sum',
            'ID_VIV': list,
            'index': list
        }
    ).sort_index().reset_index()

    # Get I and J matrices
    # Get map of viv ids to unique integers for indexing
    id_viv_l = np.sort(np.unique(personas.ID_VIV.values))
    id_viv_map = {id_viv: i for i, id_viv in enumerate(id_viv_l)}

    I = defaultdict(lambda: 0)
    J = defaultdict(lambda: 0)
    for i, row in X.iterrows():
        for id_viv in row.ID_VIV:
            I[(id_viv_map[id_viv], i)] += 1
        for id_per in row['index']:
            J[(i, id_per)] += 1
    I = sparse.COO(
        sparse.DOK(
            shape=(len(id_viv_l), len(X)),
            data=I,
            dtype=np.uint8)
    )
    J = sparse.COO(
        sparse.DOK(
            shape=(len(X), len(personas)),
            data=J,
            dtype=int)
    )

    coords = np.row_stack(
        [
            personas.ID_VIV.map(id_viv_map).values,
            personas.index.values
        ]
    )
    L = sparse.COO(coords, data=1, shape=(len(id_viv_l), len(personas)))

    assert np.all(I.sum(axis=1).todense() == viviendas.NUMPERS)
    assert J.sum(axis=0).min() == 1
    assert J.sum(axis=0).max() == 1
    assert L.sum(axis=0).min() == 1
    assert L.sum(axis=0).max() == 1
    assert np.all(L.sum(axis=1).todense() == viviendas.NUMPERS)

    W = get_W(X, constraints_ind)

    Up = pd.DataFrame(
        W.values @ I.T,
        columns=id_viv_l,
        index=W.index
    )
    Uh = get_W(viviendas.set_index('ID_VIV'), constraints_viv)

    assert np.all(Uh.columns == Up.columns)
    U = pd.concat([Uh, Up])

    C = df_mun[
        U.index.tolist()
        # + ['POBHOG', 'POBCOL', 'PHOGJEF_F', 'PHOGJEF_M']
    ]

    Y = viviendas.set_index('ID_VIV').loc[id_viv_l, ['MUN', 'FACTOR']].copy()
    Y = Y.rename(columns={'FACTOR': 'Survey'})
    mun_list = [m for m in Y.MUN.unique() if m != 'IMPUTED']
    for mun in mun_list:
        Y[mun] = Y.Survey * (Y.MUN == mun)

    X = X.drop(columns=['ID_VIV', 'index'])

    # We need to add collective people to the Gurobi model
    # Take information from X and W
    # X do not need modifications, but we need to create Y_people from it
    Yp = X[['MUN']].copy()
    Yp.index.name = 'ID_PER'
    Yp[Y.columns.drop('MUN')] = 0

    # Now, we need to modify W into Up
    # POBTOT constraints is OK, no need to modify it
    # We need to add POBCOL row of 1's
    # We need to add POBHOG row of 0's
    Up = W.copy()
    Up.index.name = 'ID_PER'
    Up.loc['POBCOL'] = 1
    Up.loc['POBHOG'] = 0

    # Now, we need to add constraints POBCOL, POBHOG to U
    # We are not controlling for TOTCOL, grouping all collective population
    # since we are ignorant of the appropriate household structure, and
    # do not expect to resemble those of private households.
    U.loc['POBCOL'] = 0
    U.loc['POBHOG'] = U.loc['POBTOT']

    # We need to add contraints to C, these constraints exist already in TAZ
    # Need to add POBCOL and POBHOG and remove POBTOT
    # since there is no need to constraint it if
    # contraining POBCOL and POGHOG
    C.loc[:, ['POBCOL', 'POBHOG']] = df_mun[['POBCOL', 'POBHOG']]
    C = C.drop(columns=['POBTOT'])

    # Assign proper variables to household mateices
    Uh = U
    Uh.columns.name = 'ID_VIV'
    Yh = Y

    Uh = Uh.drop(index='POBTOT')
    Up = Up.drop(index='POBTOT')

    # Now we need to join this up into a single Y and U
    Y = pd.concat([Yh, Yp])
    U = pd.concat([Uh, Up], axis=1).fillna(0).astype(int)

    return X, I, J, L, Up, Uh, U, Yp, Yh, Y, C

    pjoin = personas.drop(
        columns=['MUN', 'FACTOR']
    ).join(viviendas, on='ID_VIV')

    return pjoin, viviendas, W, X.drop(columns=['ID_VIV', 'index']), I, J, L, U, C, Y, Uh,Up


def fix_zero_cell_all(Y, U, C):
    Y = Y.copy()
    mun_list = [m for m in Y.MUN.unique() if m != 'IMPUTED']
    for mun in mun_list:
        Y[mun] = Y[mun].astype(float)

        # Get only vivs for current mun
        mask = Y.MUN == mun
        # Find C for the restricted nnls problem
        Cr = find_zero_nozero_const(U.loc[:, mask], C.loc[mun])
        consts = Cr.index
        if len(consts) == 0:
            # print(mun, 0)
            continue

        print(mun)
        print(Cr)
        print('###############')
        # Find the ids invovled in zeroed constraints
        query = ' | '.join([f'{const} > 0' for const in consts])
        viv_ids = U.T.query(query).index

        # Find U for the restricted nnls problem
        Ur = U.loc[consts, viv_ids]

        # Solve the nnls problem
        factors_new, err = nnls(Ur.values.astype(float), Cr)
        assert err < 1e-10, mun
        factors_new[factors_new < 1e-10] = 0
        # nnew = (factors_new > 1e-10).sum()
        # print(mun, nnew)

        # Assign new weights in Y
        Y.loc[viv_ids, mun] = factors_new
        mask = Y.loc[:, mun] > 0
        assert len(
            find_zero_nozero_const(U.loc[:, mask], C.loc[mun])) == 0, mun

    return Y


def get_conf_cols(consts, const_dict):
    cols = []
    for const in consts:
        cols.extend(list(const_dict[const].keys()))
    cols = tuple(set(cols))
    return cols


def get_conf_consts(mun, Y, U, C):
    mask = Y.loc[:, mun] > 0
    Ur = U.loc[:, mask]
    conf_consts = find_conf_const(Ur, C.loc[mun])

    return conf_consts


def fix_confs_mun(mun, Y_ext, personas, viviendas, U, C, L, const_dict,
                  fill_factor=1e-3):
    conf_consts = get_conf_consts(mun, Y_ext, U, C)

    n_ext = 0
    while len(conf_consts) > 0:
        # Find all combinations of conflicting constraints sets
        combs = []
        for consts in conf_consts:
            # Find columns involved in the constraints
            cols = get_conf_cols(consts, const_dict)

            # Find all combinations of cols, ignore Blanco por pase
            ccombs = list(zip(*[personas[c] for c in cols]))
            ccombs = set([c for c in ccombs if 'Blanco por pase' not in c])
            combs.extend([(cols, ccomb) for ccomb in ccombs])

        combs = set(combs)
        combs_dict = defaultdict(list)
        for cols, comb in combs:
            combs_dict[cols].append(comb)
        # Get full list of constraints
        consts = list(set(sum(conf_consts, [])))

        # Find all combinations already present in mun
        # as well as missing combinations
        mask_in = Y_ext[mun] > 0
        # viviendas_in = viviendas.loc[mask_in]
        maskP_in = L[mask_in].sum(axis=0).astype(bool).todense()
        personas_in = personas.loc[maskP_in]

        combs_in_dict = defaultdict(list)
        combs_miss_dict = defaultdict(list)
        for cols, combs in combs_dict.items():
            combs_in_dict[cols] = set(zip(*[personas_in[c] for c in cols]))
            combs_miss_dict[cols] = set(combs_dict[cols]) - combs_in_dict[cols]

        # Build query to search for them

        def s_or_i(c):
            if isinstance(c, str):
                return f'"{c}"'
            else:
                return c

        query_l = []
        for cols, combs in combs_miss_dict.items():
            ss = []
            for comb in combs:
                s = ' & '.join(
                    f'{col}=={s_or_i(c)}'for col, c in zip(cols, comb)
                )
                ss.append(f'({s})')
            ss = ' | '.join(ss)
            query_l.append(f'({ss})')
        query = ' | '.join(query_l)
        # Get viv ids
        maskP_miss = personas.eval(query)
        mask_miss = L.T[maskP_miss].sum(axis=0).astype(bool).todense()
        assert mask_miss.sum() > 0

        # Solve restrictred nnls problem
        mask = mask_in | mask_miss
        Cr = C.loc[mun, consts]
        Ur = U.loc[consts, mask]
        Yr, err = nnls(Ur, Cr)
        assert err < 1e-10, (mun, err)
        # print(mun, err)
        mask0 = np.zeros_like(mask, dtype=bool)
        mask0[mask] = Yr.astype(bool)

        # Find nnls solutions belonging to missing set
        mask_ext = mask0 & mask_miss
        n_ext += mask_ext.sum()
        assert 100 > n_ext > 0

        # Add them to seed with small weight
        # reflecting they are missing from original seed (How small?)
        Y_ext.loc[mask_ext, mun] = fill_factor

        conf_consts = get_conf_consts(mun, Y_ext, U, C)
        # break
    print(mun, n_ext)

    # return mask


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
    if np.linalg.matrix_rank(W_ind) != rank:
        r, P = qr(W.T.values, mode='r', pivoting=True)
        assert (abs(np.diag(r)) > 1e-10).sum() == rank
        W_ind = W.iloc[P[:rank]].copy()
        W_dep = W.iloc[P[rank:]].copy()
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
            conf_consts.append([cname])
            conf_consts[-1].extend(W_ind.index[c_w.astype(bool)])
    # conf_consts = set(conf_consts)

    return list(conf_consts)  # , rank, A, C_ind, W_ind, W_dep


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


def setup_ls(personas_cat, viviendas_cat,
             df_mun,
             constraints_ind, constraints_viv,
             out_path,
             ignore_cols_p=[],
             ignore_cols_v=[],
             verbose=True):

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
    XWC_init = make_init_dict(
        personas_cat, viviendas_cat,
        df_mun,
        constraints_ind, constraints_viv,
        out_path)

    # Seconf loop, fix zero cell problmes
    XWC_ext = fix_zero_cell(
        XWC_init,
        personas_cat, viviendas_cat,
        df_mun,
        constraints_ind, constraints_viv,
        out_path)

    # Third loop to fix conflicts among constraints
    print('Fixing conflicting constraints ... ')
    for mun in personas_cat.keys():
        if mun == 'IMPUTED':
            continue

        print(f'    {mun} ...', end='')
        conf_consts = XWC_dict[mun]['conf_consts']
        zero_consts = XWC_dict[mun]['zero_nozero'].index.tolist()
        consts = set(zero_consts + conf_consts)
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

        XWC_dict[mun]['Y_ext'] = Y_ext
        XWC_dict[mun]['U_ext'] = U_ext
        XWC_dict[mun]['C_ext'] = C_ext

        Y = XWC_dict[mun]['Y']
        print(f'Added {len(Y_ext) - len(Y)} extra households.')

        conf_consts = find_conf_const(U_ext, C_ext)
        XWC_dict[mun]['conf_consts'] = conf_consts

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
