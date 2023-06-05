import numpy as np
import pandas as pd


def create_implicit_consts(df_censo):
    df_min = df_censo.replace(-1, 0)
    df_max = df_censo.replace(-1, 2)

    new_cols = ['P_UNK', 'PNA_OP_BPP_NE', 'POB_AFRO_NO_NE',
                'PDER_NE', 'PRELIG_NE', 'PRES15_OP_BPP_NE',
                'P3_LI_NO_BPP_NE', 'P5_LI_NO_BPP_NE',
                'P3A14_A_NE_BPP', 'P15A24_NOA_NE_BPP',
                'P8A14AS', 'P15YM_AS', 'P12YM_BPP_NE',
                'PE_BPP_NE',
                'P15_POSBAS_BPP_NE', 'P18_BAS_BPP_NE']

    # Create columns
    for df in [df_censo, df_min, df_max]:
        df['P_UNK'] = df.POBTOT - (df.POB0_14 + df.P_15YMAS)
        df['PNA_OP_BPP_NE'] = df.POBTOT - (df.PNACENT + df.PNACOE)
        df['POB_AFRO_NO_NE'] = df.POBTOT - df.POB_AFRO
        df['PDER_NE'] = df.POBTOT - (df.PSINDER + df.PDER_SS)
        df['PRELIG_NE'] = df.POBTOT - (
            df.PCATOLICA + df.PRO_CRIEVA + df.POTRAS_REL + df.PSIN_RELIG
        )
        df['PRES15_OP_BPP_NE'] = df.P_5YMAS - (df.PRES2015 + df.PRESOE15)
        df['P3_LI_NO_BPP_NE'] = df.P_3YMAS - df.P3YM_HLI
        df['P5_LI_NO_BPP_NE'] = df.P_5YMAS - df.P5_HLI
        df['P3A14_A_NE_BPP'] = (df.P_3YMAS - df.P_15YMAS) - (
            df.P3A5_NOA + df.P6A11_NOA + df.P12A14NOA)
        df['P15A24_NOA_NE_BPP'] = (df.P_15A17 + df.P_18A24) - (
            df.P15A17A + df.P18A24A)
        df['P8A14AS'] = df.P_8A14 - df.P8A14AN
        df['P15YM_AS'] = df.P_15YMAS - df.P15YM_AN
        df['P12YM_BPP_NE'] = df.P_12YMAS - (
            df.P12YM_SOLT + df.P12YM_CASA + df.P12YM_SEPA)
        df['PE_BPP_NE'] = df.P_12YMAS - (df.PEA + df.PE_INAC)
        df['P15_POSBAS_BPP_NE'] = df.P_15YMAS - (
            df.P15YM_SE + df.P15PRI_IN + df.P15PRI_CO +
            df.P15SEC_IN + df.P15SEC_CO)
        df['P18_BAS_BPP_NE'] = df.P_18YMAS - df.P18YM_PB

    # Mark uncertain values with -1 again
    for col in new_cols:
        # assert df_min[col].min() >= 0, col
        # assert df_max[col].min() >= 0, col
        df_censo[col] = df_censo[col].where(
            np.logical_or(
                df_min[col] == df_max[col],
                df_censo[col].isna()
            ),
            -1
        )
        # assert df_censo[col].min() >= -1, col

    return df_censo, df_min, df_max


def process_census(census_iter_path, census_resageburb_path):
    non_count_cols = [
        'REL_H_M', 'PROM_HNV', 'GRAPROES',
        'GRAPROES_F', 'GRAPROES_M', 'PROM_OCUP', 'PRO_OCUP_C'
    ]

    # Load census data
    df_censo = pd.read_csv(
        census_resageburb_path,
        low_memory=False,
        na_values=['N/D'],
    )

    obj_cols = ['NOM_ENT', 'NOM_MUN', 'NOM_LOC', 'AGEB']
    int_cols = ['ENTIDAD', 'MUN', 'LOC', 'MZA', 'POBTOT', 'VIVTOT']

    # For manzanas, asterisc means ommited values where VIVTOT <= 2
    mask = np.logical_and(
        df_censo.values == '*',
        np.broadcast_to(
            (df_censo.VIVTOT.values <= 2)[:, None],
            df_censo.shape
        )
    )
    df_censo = df_censo.mask(mask, np.nan)

    # Otherwise * measn values of 0,1,2, replace by -1 for identification
    df_censo = df_censo.mask(df_censo == '*', -1)

    for col in df_censo.columns.drop(obj_cols + int_cols):
        df_censo[col] = df_censo[col].astype(float)

    # Create ind dataframes
    df_entidad = df_censo.query(
        'ENTIDAD != 0 & MUN == 0 & LOC == 0 & AGEB == "0000" & MZA == 0'
    ).drop(
        columns=[
            'ENTIDAD', 'NOM_ENT', 'NOM_MUN', 'MUN',
            'AGEB', 'MZA', 'NOM_LOC', 'LOC'
        ] + non_count_cols
    ).reset_index(drop=True)

    df_mun = df_censo.query(
        'ENTIDAD != 0 & MUN != 0 & LOC == 0 & AGEB == "0000" & MZA == 0'
    ).drop(columns=[
        'ENTIDAD', 'NOM_ENT', 'NOM_MUN',
        'AGEB', 'MZA', 'NOM_LOC', 'LOC'
    ] + non_count_cols).reset_index(drop=True).set_index('MUN')

    df_loc = df_censo.query(
        'ENTIDAD != 0 & MUN != 0 & LOC != 0 & AGEB == "0000" & MZA == 0'
    ).drop(columns=[
        'ENTIDAD', 'NOM_ENT', 'NOM_MUN', 'NOM_LOC',
        'AGEB', 'MZA'] + non_count_cols
           ).reset_index(drop=True).set_index(['MUN', 'LOC'])

    df_agebs = df_censo.query(
        'ENTIDAD != 0 & MUN != 0 & LOC != 0 & AGEB != "0000" & MZA == 0'
    ).drop(columns=[
        'ENTIDAD', 'NOM_ENT', 'NOM_MUN',
        'NOM_LOC', 'MZA'] + non_count_cols
           ).reset_index(drop=True).set_index(['MUN', 'LOC', 'AGEB'])

    # Load results buy locality
    df_iter = pd.read_csv(census_iter_path,
                          low_memory=False,
                          na_values=['*', 'N/D'])

    df_iter_ent = (
        df_iter.head(1)
        .reset_index(drop=True)[df_entidad.columns]
        .copy()
    )

    df_iter_mun = (
        df_iter[df_iter.NOM_LOC == 'Total del Municipio']
        .reset_index(drop=True)
        .set_index('MUN')[df_mun.columns]
        .copy()
    )

    df_iter_loc = (
        df_iter[
            (df_iter.LOC != 0) & (df_iter.MUN != 0) & (df_iter.LOC < 9998)
        ]
        .reset_index(drop=True)
        .set_index(['MUN', 'LOC'])[df_loc.columns]
        .copy())

    # Sanity checks

    # Perfect match at entity level
    assert np.all(df_entidad == df_iter_ent)

    # Both census match for municipalities when exlcuding
    # ommited values in RESAGEBURB
    assert np.all(
        df_mun.values == df_iter_mun.values,
        where=~np.logical_or(df_mun.isna(), df_mun == -1)
    )

    # Aggregate matches from mun -> ent when non-count columns removed
    assert np.all(df_iter_mun.sum() == df_iter_ent)

    # REAGEBURB only incudes localities with
    # POBTOT > 2500 or municipality heads
    # Check if mutual localities match
    assert np.all(
        (df_loc == df_iter_loc[df_iter_loc.index.isin(df_loc.index)]).values,
        where=~np.logical_or(df_loc.isna(), df_loc == -1)
    )

    # For iter check if aggregation locality -> mun holds
    # Must take into account nan values
    num_missing_iter_loc = df_iter_loc.isna().groupby('MUN').sum()
    sum_iter_loc = df_iter_loc.groupby('MUN').sum()
    # Check cells without missing values
    assert np.all(
        (df_iter_mun == sum_iter_loc).values,
        where=num_missing_iter_loc == 0
    )
    # Check cells with missing values
    assert np.all((df_iter_mun >= sum_iter_loc).values)

    # For RESARGEBUB check if aggregation from AGEB -> Locality holds
    num_missing_agebs = (
        df_agebs.replace(-1, np.nan)
        .isna()
        .groupby(['MUN', 'LOC'])
        .sum()
    )
    sum_agebs = df_agebs.replace(-1, np.nan).groupby(['MUN', 'LOC']).sum()
    # Check cells without missing values
    assert np.all(
        (df_loc == sum_agebs).values,
        where=num_missing_agebs == 0
    )
    # Check cells with missing values
    assert np.all((df_loc >= sum_agebs).values,
                  where=~df_loc.replace(-1, np.nan).isna())

    # Eliminar AGEBS sin población
    df_agebs = df_agebs[df_agebs.POBTOT > 0].copy()

    # Create implicit constraints to identify
    # zero cell problems
    (
        df_iter_mun,
        df_iter_mun_min,
        df_iter_mun_max
    ) = create_implicit_consts(df_iter_mun)

    (
        df_iter_loc,
        df_iter_loc_min,
        df_iter_loc_max
    ) = create_implicit_consts(df_iter_loc)

    (
        df_agebs,
        df_agebs_min,
        df_agebs_max
    ) = create_implicit_consts(df_agebs)

    return (df_iter_mun, df_iter_mun_min, df_iter_mun_max,
            df_iter_loc, df_iter_loc_min, df_iter_loc_max,
            df_agebs, df_agebs_min, df_agebs_max)
