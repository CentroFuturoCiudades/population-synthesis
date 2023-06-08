import numpy as np
import pandas as pd


def get_mun_codes():
    df_mun_codes = pd.read_csv(
        '../data/cuestionario_ampliado/'
        'Censo2020_clasificaciones_CPV_csv/MUN.csv',
        encoding='ISO-8859-1'
    )
    mun_codes = {i: {} for i in df_mun_codes.CVE_ENT.unique()}
    for idx, row in df_mun_codes.iterrows():
        ent = row.CVE_ENT
        mun = row.CVE_MUN
        nom = row.NOM_MUN
        mun_codes[ent][mun] = nom
    return mun_codes


def create_implicit_consts(df_censo):
    df_min = df_censo.replace(-1, 0)
    df_max = df_censo.replace(-1, 2)

    new_cols = [
        'P_UNK',

        'PNA_OP_BPP_NE_F', 'PNA_OP_BPP_NE_M',
        'PRES15_OP_BPP_NE_F', 'PRES15_OP_BPP_NE_M',

        'POB_AFRO_NO_NE_F', 'POB_AFRO_NO_NE_M',
        'P3_LI_NO_BPP_NE_F', 'P3_LI_NO_BPP_NE_M',
        'P5_LI_NO_BPP_NE',

        'P3A5_A_NE_BPP_F', 'P3A5_A_NE_BPP_M',
        'P6A11_A_NE_BPP_F', 'P6A11_A_NE_BPP_M',
        'P12A14_A_NE_BPP_F', 'P12A14_A_NE_BPP_M',
        'P15A17_NOA_NE_BPP_F', 'P15A17_NOA_NE_BPP_M',
        'P18A24_NOA_NE_BPP_F', 'P18A24_NOA_NE_BPP_M',

        'P8A14AS_F', 'P8A14AS_M',
        'P15YM_AS_F', 'P15YM_AS_M',

        'P15_POSBAS_BPP_NE_F', 'P15_POSBAS_BPP_NE_M',
        'P18_BAS_BPP_NE_F', 'P18_BAS_BPP_NE_M',

        'PE_BPP_NE_F', 'PE_BPP_NE_M',

        'PDER_NE',

        'P12YM_BPP_NE',

        'PRELIG_NE',
    ]

    # Create columns
    for df in [df_censo, df_min, df_max]:
        df['P_UNK'] = df.POBTOT - (df.POB0_14 + df.P_15YMAS)

        df['PNA_OP_BPP_NE_F'] = df.POBFEM - (df.PNACENT_F + df.PNACOE_F)
        df['PNA_OP_BPP_NE_M'] = df.POBMAS - (df.PNACENT_M + df.PNACOE_M)
        df['PRES15_OP_BPP_NE_F'] = df.P_5YMAS_F - (
            df.PRES2015_F + df.PRESOE15_F)
        df['PRES15_OP_BPP_NE_M'] = df.P_5YMAS_M - (
            df.PRES2015_M + df.PRESOE15_M)

        df['POB_AFRO_NO_NE_F'] = df.POBFEM - df.POB_AFRO_F
        df['POB_AFRO_NO_NE_M'] = df.POBMAS - df.POB_AFRO_M
        df['P3_LI_NO_BPP_NE_F'] = df.P_3YMAS_F - df.P3YM_HLI_F
        df['P3_LI_NO_BPP_NE_M'] = df.P_3YMAS_M - df.P3YM_HLI_M
        df['P5_LI_NO_BPP_NE'] = df.P_5YMAS - df.P5_HLI

        df['P3A5_A_NE_BPP_F'] = df.P_3A5_F - df.P3A5_NOA_F
        df['P3A5_A_NE_BPP_M'] = df.P_3A5_M - df.P3A5_NOA_M
        df['P6A11_A_NE_BPP_F'] = df.P_6A11_F - df.P6A11_NOAF
        df['P6A11_A_NE_BPP_M'] = df.P_6A11_M - df.P6A11_NOAM
        df['P12A14_A_NE_BPP_F'] = df.P_12A14_F - df.P12A14NOAF
        df['P12A14_A_NE_BPP_M'] = df.P_12A14_M - df.P12A14NOAM
        df['P15A17_NOA_NE_BPP_F'] = df.P_15A17_F - df.P15A17A_F
        df['P15A17_NOA_NE_BPP_M'] = df.P_15A17_M - df.P15A17A_M
        df['P18A24_NOA_NE_BPP_F'] = df.P_18A24_F - df.P18A24A_F
        df['P18A24_NOA_NE_BPP_M'] = df.P_18A24_M - df.P18A24A_M

        df['P8A14AS_F'] = df.P_8A14_F - df.P8A14AN_F
        df['P8A14AS_M'] = df.P_8A14_M - df.P8A14AN_M
        df['P15YM_AS_F'] = df.P_15YMAS_F - df.P15YM_AN_F
        df['P15YM_AS_M'] = df.P_15YMAS_M - df.P15YM_AN_M

        df['P15_POSBAS_BPP_NE_F'] = df.P_15YMAS_F - (
            df.P15YM_SE_F + df.P15PRI_INF + df.P15PRI_COF +
            df.P15SEC_INF + df.P15SEC_COF)
        df['P15_POSBAS_BPP_NE_M'] = df.P_15YMAS_M - (
            df.P15YM_SE_M + df.P15PRI_INM + df.P15PRI_COM +
            df.P15SEC_INM + df.P15SEC_COM)
        df['P18_BAS_BPP_NE_F'] = df.P_18YMAS_F - df.P18YM_PB_F
        df['P18_BAS_BPP_NE_M'] = df.P_18YMAS_M - df.P18YM_PB_M

        df['PE_BPP_NE_F'] = df.P_12YMAS_F - (df.PEA_F + df.PE_INAC_F)
        df['PE_BPP_NE_M'] = df.P_12YMAS_M - (df.PEA_M + df.PE_INAC_M)

        df['PDER_NE'] = df.POBTOT - (df.PSINDER + df.PDER_SS)

        df['P12YM_BPP_NE'] = df.P_12YMAS - (
            df.P12YM_SOLT + df.P12YM_CASA + df.P12YM_SEPA)

        df['PRELIG_NE'] = df.POBTOT - (
            df.PCATOLICA + df.PRO_CRIEVA + df.POTRAS_REL + df.PSIN_RELIG
        )

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

    mun_codes = get_mun_codes()
    df_iter_mun.index = [mun_codes[19][i] for i in df_iter_mun.index]

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
