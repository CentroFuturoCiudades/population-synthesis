import numpy as np
import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from pathlib import Path


def relax_model(model, verbose=False):
    model_f = model.copy()
    orignumvars = model_f.NumVars
    constrs = [c for c in model.getConstrs() if c.Sense != '=']
    model_f.feasRelax(
        relaxobjtype=0,
        minrelax=False,
        vars=None,
        lbpen=None,
        ubpen=None,
        constrs=constrs,
        rhspen=[1.0]*len(constrs)
    )
    model_f.optimize()

    if verbose:
        print('\nSlack values:')

    slacks = model_f.getVars()[orignumvars:]
    slacks_2 = []
    for sv in slacks:
        if sv.X > 1e-9:
            # Check that the RHS decreases
            assert 'ArtP_' in sv.VarName
            slacks_2.append(
                (sv.VarName.replace('ArtP_', ''), sv.X)
            )
            if verbose:
                print('%s = %g' % (sv.VarName, sv.X))

    return slacks_2


def reduce_matrices(U, Y):
    # Reduce the number of variables by identifying equivalent households
    # These are equivalent from the perspective of the solver, since they
    # contribute equally to the constraints.
    # Other attributes may differ, but can be recovered in post-processing and
    # assigned accordingly to the sample proportions.
    gcols = U.index.to_list()
    H = U.T.copy()
    H = H.join(Y)
    H = H.reset_index().groupby(
        gcols + ['MUN'], observed=True
    ).agg(
        {'ID_VIV': list, 'Survey': list}
        | {c: 'sum' for c in Y.columns.drop(['MUN', 'Survey'])}
    ).reset_index().sort_values('MUN').reset_index()
    Uh = H[gcols].T
    Yh = H[Y.columns]
    h_to_y = H[['ID_VIV', 'Survey']].copy()
    h_to_y['rep'] = h_to_y.Survey.apply(len)
    # Yh = h_to_y.index
    print(f'{U.shape[1]} orignal households compressed '
          f'into {Uh.shape[1]} distinct prototypes.')

    return Uh, Yh, h_to_y


def setup_gb(mun, taz_dict, df_mun, C, Yh, Uh):
    taz_gdf = taz_dict[mun]

    # Total number of households
    N_mun = int(df_mun.loc[mun, 'TVIVHAB'])

    # Load the constraints as a dictionary
    C_mun = C.loc[mun].astype(int).to_dict()
    C_taz_all = taz_gdf.set_index('ZONA')[C_mun.keys()].fillna(0).astype(int)

    # Get the sample households ids and the contraint weight matrix
    Y_mun = Yh.loc[Yh[mun] > 0, mun]
    U_mun = Uh.loc[:, Y_mun.index]
    assert U_mun.T.duplicated().sum() == 0

    # Total number of survey entries
    N_S = len(Y_mun)
    # Total number of TAZ
    N_T = taz_gdf.shape[0]
    # Number of constraints
    N_C = len(C_mun)

    print(f'{mun} has {N_T} taz and {N_mun} households and {N_S} respondents and {N_C} constraints.')


def solve_gurobi_taz(U_mun, Y_mun, C_taz, obj_type,
                     jitter=False, save=False):

    assert np.all(U_mun.index == C_taz.index)
    assert np.all(U_mun.columns == Y_mun.index)
    # Some useful quantities
    N_S = Y_mun.shape[0]  # Total number of survey entries
    N_t = C_taz.TOTHOG  # Total number of households in taz
    N_p = C_taz.POBCOL  # Total number collective people
    N_C = C_taz.shape[0]  # Number of constraints
    N_s = Y_mun.sum()  # Sum of survey weights

    model = gp.Model(f'MUN_{Y_mun.name}_TAZ_{C_taz.name}')

    # Create vector of household variables
    yT = model.addMVar(
        shape=N_S,
        vtype=GRB.INTEGER,
        name='yT',
        lb=0,
        ub=(Y_mun.values > 0) * N_t + (Y_mun.values == 0) * N_p
    )

    # The constraints can be easily added in matrix form
    # Treat total people and household as =, other constraints as >=
    sense = np.array(['>']*N_C)
    sense[C_taz.index.isin(['TVIVHAB', 'TOTHOG', 'POBCOL', 'POBHOG'])] = '='

    model.addMConstr(
        A=U_mun.values,
        x=yT,
        sense=sense,
        b=C_taz.values,
        name=C_taz.index.to_list()
    )

    # Y = Y_mun.values*N_t/N_s
    if jitter:
        Y_mun = Y_mun + np.random.uniform(0.1, 0.5, len(Y_mun))

    # if obj_type == 'L1':
    #     ydiff = model.addMVar(
    #         shape=N_S,
    #         vtype=GRB.CONTINUOUS,
    #         name='ydiff',
    #         lb=-1, ub=1)
    #     model.addConstr(yT/N_t - Y_mun.values/N_s == ydiff)
    #     norm = model.addVar(name='norm', ub=N_S)
    #     model.addGenConstrNorm(norm, ydiff, 1, name='norm')
    #     model.setObjective(norm, GRB.MINIMIZE)
    if obj_type == 'L2':
        model.setObjective(
            (yT/N_t - Y_mun.values/N_s) @ (yT/N_t - Y_mun.values/N_s),
            GRB.MINIMIZE
        )
    elif obj_type == 0:
        model.setObjective(
            # (yT/N_t - Y_mun.values/N_s) @ (yT/N_t - Y_mun.values/N_s),
            # (yT - Y) @ (yT - Y),
            0,
            GRB.MINIMIZE
        )
    else:
        assert False, 'Incorrect value.'

    model.Params.LogToConsole = 0
    model.Params.PoolSolutions = 100
    # model.Params.SolutionLimit = 100
    model.Params.TimeLimit = 120
    # model.Params.LogFile = f'MUN_{Y_mun.name}_TAZ_{C_taz.name}.log'
    model.Params.JSONSolDetail = 1
    model.optimize()

    if model.Status == GRB.INFEASIBLE:
        # print(f'MUN_{Y_mun.name}_TAZ_{C_taz.name} INFEASIBLE')
        return False, None, model
    elif (
            model.Status == GRB.OPTIMAL
            or model.Status == GRB.TIME_LIMIT
            or model.Status == GRB.SOLUTION_LIMIT
    ):
        pass
    else:
        assert False, 'Unexpected behaviour.'

    # Extract all solutions, save to disk
    sol_arr = np.zeros((model.SolCount, Y_mun.size), dtype=int)
    obj_arr = np.zeros(model.SolCount, dtype=float)
    for sol_n in range(model.SolCount):
        model.params.SolutionNumber = sol_n
        sol_arr[sol_n, :] = np.round(yT.Xn).astype(int)
        obj_arr[sol_n] = model.PoolObjVal

    sol_df = pd.concat(
        [
            pd.DataFrame({'obj_val': obj_arr}),
            pd.DataFrame(sol_arr, columns=Y_mun.index.tolist())
        ],
        axis=1
    )

    if save:
        sol_df.to_pickle(f'MUN_{Y_mun.name}_TAZ_{C_taz.name}_gsols.pkl')
        model.write(f'MUN_{Y_mun.name}_TAZ_{C_taz.name}_gsols.json')

    return True, sol_df, model


def solve_gurobi_mun(U_mun, Y_mun, C_mun, C_taz_all):

    vtype = GRB.INTEGER
    U_mun = U_mun.values

    # Some useful quantities
    N_S = Y_mun.shape[0]  # Total number of survey entries
    N_mun = C_mun['TVIVHAB']  # Total number of households in mun
    N_T, N_C = C_taz_all.shape  # Number of TAZ, Number of constratins
    N_s = Y_mun.sum()  # Sum of survey weights

    model = gp.Model('mun')

    # Create matrix of household variables N_S X N_TAZ
    YT = model.addMVar(
        shape=(N_S, N_T),
        vtype=vtype,
        name='YT',
        lb=0,
        ub=C_taz_all.TVIVHAB.values
    )

    # The constraints can be easily added in matrix form
    # Treat total people and household as =, other constraints as >=
    sense = np.array(['>']*N_C)
    sense[C_taz_all.columns.isin(['TVIVHAB', 'POBTOT'])] = '='
    # Need to loop over taz, columns of YT
    for yT, (taz, C_taz) in zip(YT.T, C_taz_all.iterrows()):
        model.addMConstr(
            A=U_mun,
            x=yT,
            sense=sense,
            b=C_taz.values,
            name=[f'TAZ_{taz}_' + c for c in C_taz.index.to_list()]
        )

    # Add constraints without intermediate variables
    cm = np.array(list(C_mun.values()))
    for i in range(N_C):
        if sense[i] == '=':
            model.addConstr(
                sum(
                    U_mun[i, :] @ YT[:, t]
                    # for j in range(N_S)
                    for t in range(N_T)
                ) == cm[i]
            )
        else:
            model.addConstr(
                sum(
                    U_mun[i, :] @ YT[:, t]
                    # for j in range(N_S)
                    for t in range(N_T)
                ) >= cm[i]
            )

    # Add constraints to avoid sparsity
    for s in range(N_S):
        model.addConstr(YT[s, :].sum() >= 1)

    # # Add municipality level auxiliary variables
    # ym = model.addMVar(
    #     shape=N_S,
    #     vtype=vtype,
    #     name='ym',
    #     lb=1,
    #     ub=N_mun
    # )
    # # Add constraints for sum of taz variables
    # model.addConstr(ym == YT.sum(axis=1), name='hier')

    # # Add municipality level constraint
    # model.addMConstr(
    #     A=U_mun,
    #     x=ym,
    #     sense=sense,
    #     b=np.array(list(C_mun.values())),
    #     name='mun'
    # )

    Y = Y_mun.values*N_mun/N_s

    model.setObjective(
        0,
        # (ym - Y) @ (ym - Y),
        # (YT.T @ YT).sum() - 2*(YT * Y[:, None]).sum(),
        GRB.MINIMIZE
    )

    return model, YT, Y


def solve_gb(mun, taz, taz_dict, Y, U, C, obj_type, save, force=False):

    sol_file = Path(f'MUN_{mun}_TAZ_{taz}_gsols.json')
    if sol_file.exists() and not force:
        return None, None

    # Load the constraints as a dictionary
    C_mun = C.loc[mun].astype(int).to_dict()
    C_taz = (
        taz_dict[mun]
        .set_index('ZONA')[C_mun.keys()]
        .fillna(0)
        .astype(int)
        .loc[taz]
        .copy()
    )
    if C_taz.TOTHOG < 1:
        return None, None

    # Get the sample households ids and the contraint weight matrix
    Y_mun = Y.loc[Y['MUN'] == mun, mun]
    U_mun = U.loc[:, Y_mun.index]
    assert Y_mun.sum() > 0

    status, sol_df, model = solve_gurobi_taz(
        U_mun, Y_mun, C_taz, obj_type=obj_type,
        jitter=False, save=save
    )

    if not status:
        # Relax the model
        print(f'Relaxing {mun} {taz} ... ')
        slacks = relax_model(model, verbose=True)

        # Adjust constraints
        for cname, c_adj in slacks:
            C_taz[cname] = C_taz[cname] - c_adj
            assert C_taz[cname] >= 0, C_taz[cname]

        # Run model again
        status, sol_df, model = solve_gurobi_taz(
            U_mun, Y_mun, C_taz, obj_type=obj_type,
            jitter=False, save=save
        )
    assert status, (mun, taz)

    return sol_df, model
