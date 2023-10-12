import numpy as np
import pandas as pd
import gurobipy as gp
from gurobipy import GRB


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


def solve_gurobi_taz(U_mun, Y_mun, C_taz, obj_type, jitter=False, save=False):

    # Some useful quantities
    N_S = Y_mun.shape[0]  # Total number of survey entries
    N_t = C_taz.TVIVHAB  # Total number of households in taz
    N_C = C_taz.shape[0]  # Number of constraints
    N_s = Y_mun.sum()  # Sum of survey weights

    model = gp.Model(f'MUN_{Y_mun.name}_TAZ_{C_taz.name}')

    # Create vector of household variables
    yT = model.addMVar(shape=N_S, vtype=GRB.INTEGER, name='yT', lb=0, ub=N_t)

    # The constraints can be easily added in matrix form
    # Treat total people and household as =, other constraints as >=
    sense = np.array(['>']*N_C)
    sense[C_taz.index.isin(['TVIVHAB', 'POBTOT'])] = '='

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

    if obj_type == 'L1':
        ydiff = model.addMVar(
            shape=N_S,
            vtype=GRB.CONTINUOUS,
            name='ydiff',
            lb=-1, ub=1)
        model.addConstr(yT/N_t - Y_mun.values/N_s == ydiff)
        norm = model.addVar(name='norm', ub=N_S)
        model.addGenConstrNorm(norm, ydiff, 1, name='norm')
        model.setObjective(norm, GRB.MINIMIZE)
    elif obj_type == 'L2':
        model.setObjective(
            # (yT/N_t - Y_mun.values/N_s) @ (yT/N_t - Y_mun.values/N_s),
            # (yT - Y) @ (yT - Y),
            0,
            GRB.MINIMIZE
        )

    model.Params.LogToConsole = 0
    model.Params.PoolSolutions = 100
    # model.Params.SolutionLimit = 100
    model.Params.TimeLimit = 120
    model.Params.LogFile = f'MUN_{Y_mun.name}_TAZ_{C_taz.name}.log'
    model.optimize()

    if model.SolCount < 1:
        print(f'MUN_{Y_mun.name}_TAZ_{C_taz.name}')
    return model

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

    return sol_df


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
