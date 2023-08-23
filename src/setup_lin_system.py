import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
from scipy.optimize import nnls
from scipy.linalg import pinv, qr
import sparse
from itertools import product
import pickle
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

    # IMPORTANT NOTE / TODO:
    # Nuevo León has global zero cell problem for the constraint
    # P34HLI_NHE involving EDAD=3-4 and HLENGUA=Si/No español
    # We create an artifical set of households using nearest neighbor
    # imputation as to fill the zero cells.
    # This process is note yet automatized for households and
    # specifically for HLENGUA we need to split the columns again into
    # HLENGUA and HESPANOL
    # We give priority to No especificado neighbors over other
    # neighbors.
    # To identify the global zero cells use the find_zero_cell_global
    # function.
    viv_imp_ids = personas.query(
        'EDAD == "3-4" & HLENGUA == "Sí/No especificado"'
    ).ID_VIV.unique()

    personas_imp = personas[personas.ID_VIV.isin(viv_imp_ids)].copy()
    personas_imp['MUN'] = 'IMPUTED'
    personas_imp['MUN'] = personas_imp.MUN.astype('category')
    personas_imp['HLENGUA'] = personas_imp.HLENGUA.replace(
        'Sí/No especificado', 'Sí/No español'
    ).astype(personas.HLENGUA.dtype)

    viviendas_imp = viviendas.loc[viv_imp_ids]
    viviendas_imp['MUN'] = 'IMPUTED'

    # Create an artifitial id for created households
    viv_imp_ids_map = {
        vid: 500000000000 + i
        for i, vid in enumerate(viv_imp_ids)
    }
    personas_imp['ID_VIV'] = personas_imp.ID_VIV.map(viv_imp_ids_map)
    viviendas_imp.index = viviendas_imp.index.map(viv_imp_ids_map)

    personas = pd.concat([personas, personas_imp])
    personas['MUN'] = personas.MUN.astype('category')
    viviendas = pd.concat([viviendas, viviendas_imp])
    viviendas['MUN'] = viviendas.MUN.astype('category')

    # Get X
    # personas = personas.drop(columns=['MUN', 'MUN_RES_5A'])
    cat_cols = [
        col for col in personas.columns
        if personas[col].dtype == 'category'
    ]

    X = personas.groupby(
        cat_cols,
        observed=True
    ).agg({'FACTOR': np.sum, 'ID_VIV': list}).sort_index().reset_index()

    # Get I matrix
    # Get map of viv ids to unique integers for indexing
    id_viv_l = np.sort(np.unique(personas.ID_VIV.values))
    id_viv_map = {id_viv: i for i, id_viv in enumerate(id_viv_l)}

    I = defaultdict(lambda: 0)
    for i, row in X.iterrows():
        for id_viv in row.ID_VIV:
            I[(id_viv_map[id_viv], i)] += 1
    I = sparse.COO(
        sparse.DOK(
            shape=(len(id_viv_l), len(X)),
            data=I,
            dtype=np.uint8)
    )

    W = get_W(X, constraints_ind)

    Up = pd.DataFrame(
        W.values @ I.T,
        columns=id_viv_l,
        index=W.index
    )
    Uh = get_W(viviendas, constraints_viv)
    assert np.all(Uh.columns == Up.columns)
    U = pd.concat([Uh, Up])

    C = df_mun[U.index.tolist()]

    Y = viviendas.loc[id_viv_l, ['MUN', 'FACTOR']].copy()
    Y = Y.rename(columns={'FACTOR': 'Survey'})
    mun_list = [m for m in Y.MUN.unique() if m != 'IMPUTED']
    for mun in mun_list:
        Y[mun] = Y.Survey * (Y.MUN == mun)

    return viviendas, X.drop(columns='ID_VIV'), I, U, C, Y


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
