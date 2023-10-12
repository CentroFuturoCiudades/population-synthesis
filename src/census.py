import numpy as np
import pandas as pd

mun_d = {
    1: 'Abasolo',
    2: 'Agualeguas',
    3: 'Los Aldamas',
    4: 'Allende',
    5: 'Anáhuac',
    6: 'Apodaca',
    7: 'Aramberri',
    8: 'Bustamante',
    9: 'Cadereyta Jiménez',
    10: 'El Carmen',
    11: 'Cerralvo',
    12: 'Ciénega de Flores',
    13: 'China',
    14: 'Doctor Arroyo',
    15: 'Doctor Coss',
    16: 'Doctor González',
    17: 'Galeana',
    18: 'García',
    19: 'San Pedro Garza García',
    20: 'General Bravo',
    21: 'General Escobedo',
    22: 'General Terán',
    23: 'General Treviño',
    24: 'General Zaragoza',
    25: 'General Zuazua',
    26: 'Guadalupe',
    27: 'Los Herreras',
    28: 'Higueras',
    29: 'Hualahuises',
    30: 'Iturbide',
    31: 'Juárez',
    32: 'Lampazos de Naranjo',
    33: 'Linares',
    34: 'Marín',
    35: 'Melchor Ocampo',
    36: 'Mier y Noriega',
    37: 'Mina',
    38: 'Montemorelos',
    39: 'Monterrey',
    40: 'Parás',
    41: 'Pesquería',
    42: 'Los Ramones',
    43: 'Rayones',
    44: 'Sabinas Hidalgo',
    45: 'Salinas Victoria',
    46: 'San Nicolás de los Garza',
    47: 'Hidalgo',
    48: 'Santa Catarina',
    49: 'Santiago',
    50: 'Vallecillo',
    51: 'Villaldama'
}


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
    # Return lower bounds for counts

    df_min = df_censo.replace(-1, 0)
    df_max = df_censo.replace(-1, 2)

    # Create columns
    # This needed to identify zero cell of true values
    # Substration of lb - up
    df_min['P34HLI'] = df_min.P3YM_HLI - df_max.P5_HLI
    df_min['P34HLI_HE'] = df_min.P3HLI_HE - df_max.P5_HLI_HE
    df_min['P34HLI_NHE'] = df_min.P3HLINHE - df_max.P5_HLI_NHE

    df_min['PAFIL_PUB'] = (
        df_min.PDER_IMSS + df_min.PDER_ISTE + df_min.PDER_ISTEE
        + df_min.PAFIL_PDOM + df_min.PDER_SEGP + df_min.PDER_IMSSB
    )

    df_min['PNOCUPA'] = df_min.PDESOCUP + df_min.PE_INAC
    df_min['PNOCUPA_M'] = df_min.PDESOCUP_M + df_min.PE_INAC_M
    df_min['PNOCUPA_F'] = df_min.PDESOCUP_F + df_min.PE_INAC_F

    df_min['P8YM_AN'] = df_min.P8A14AN + df_min.P15YM_AN
    df_min['P8YM_AN_M'] = df_min.P8A14AN_M + df_min.P15YM_AN_M
    df_min['P8YM_AN_F'] = df_min.P8A14AN_F + df_min.P15YM_AN_F

    df_min['P6A14NOA'] = df_min.P6A11_NOA + df_min.P12A14NOA
    df_min['P6A14NOAF'] = df_min.P6A11_NOAF + df_min.P12A14NOAF
    df_min['P6A14NOAM'] = df_min.P6A11_NOAM + df_min.P12A14NOAM

    # COLLECTIVE
    df_min['POBCOL'] = df_min.POBTOT - df_max.POBHOG
    df_min['TOTCOL'] = df_min.TVIVHAB - df_max.TVIVPARHAB

    # new_cols = [
    #     'P34HLI', 'P34HLI_HE', 'P34HLI_NHE',
    #     'PAFIL_PUB',
    #     'PNOCUPA', 'PNOCUPA_M', 'PNOCUPA_F',
    #     'P8YM_AN', 'P8YM_AN_M', 'P8YM_AN_F',
    #     'POBCOL', 'TOTCOL',
    #     'P6A14NOA', 'P6A14NOAM', 'P6A14NOAF'
    # ]

    # Mark uncertain values with -1 again
    # for col in new_cols:
    #     df_censo[col] = df_censo[col].where(
    #         np.logical_or(
    #             df_min[col] == df_max[col],
    #             df_censo[col].isna()
    #         ),
    #         -1
    #     )

    return df_min


def locate_collective(df_mun, df_loc):
    cols = ['POBTOT', 'POBHOG',
            'TVIVHAB', 'TVIVPARHAB']

    df_mun = df_mun.copy()[cols]
    df_loc = df_loc.copy()[cols]

    df_mun['TVIVCOLHAB'] = df_mun.TVIVHAB - df_mun.TVIVPARHAB
    df_mun['POBCOL'] = df_mun.POBTOT - df_mun.POBHOG

    df_loc['TVIVCOLHAB'] = df_loc.TVIVHAB - df_loc.TVIVPARHAB
    df_loc['POBCOL'] = df_loc.POBTOT - df_loc.POBHOG

    df_loc_agg = df_loc.groupby('MUN').sum()
    df_mun['MUN'] = np.arange(1, 52)
    df_mun = df_mun.set_index('MUN')

    # This data frame locates collective dwellings into municipalities
    df_mun_loc = df_mun.merge(df_loc_agg, on='MUN', suffixes=('_mun', '_loc'))
    # Some collective dwellings may fall in localoties with nan counts
    # Identify them
    df_mun_loc['TVIVCOLHAB_diff'] = df_mun_loc.TVIVCOLHAB_mun - df_mun_loc.TVIVCOLHAB_loc
    df_mun_loc['POBCOL_diff'] = df_mun_loc.POBCOL_mun - df_mun_loc.POBCOL_loc
    mask1 = df_mun_loc.POBCOL_mun != df_mun_loc.POBCOL_loc
    mask2 = df_mun_loc.TVIVCOLHAB_mun != df_mun_loc.TVIVCOLHAB_loc
    assert np.all(mask1 == mask2)

    # We can handle a single missing dwelling per municipality
    # which is the case for Nuevo Leon
    assert df_mun_loc['TVIVCOLHAB_diff'].max() <= 1

    def filt_loc(row, pobcol):
        if row.POBTOT == pobcol and row.TVIVHAB > 1:
            return False
        if row.TVIVHAB == 1 and row.POBTOT != pobcol:
            return False
        return True

    df_mun_missing = df_mun_loc[mask1]
    # Get list of possible localities
    loc_list = []
    for mun, row in df_mun_missing.iterrows():
        # print(mun, row.POBCOL_diff, row.TVIVCOLHAB_diff)
        df_loc_m = df_loc.loc[mun]
        df_loc_m = df_loc_m[
            (df_loc_m.POBTOT >= row.POBCOL_diff)
            & (df_loc_m.TVIVCOLHAB.isna())
            & (df_loc_m.apply(filt_loc, args=(row.POBCOL_diff,), axis=1))
        ]
        loc_list.append((mun, row.POBCOL_diff, row.TVIVCOLHAB_diff, df_loc_m))

    return loc_list
    return df_mun_missing
    # return muns_with_missing


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

    # For agebs the same happens when TVIVHAB <=2
    mask = np.logical_and(
        df_censo.values == '*',
        np.broadcast_to(
            (df_censo.TVIVHAB.isin(['0', '1', '2'])).values[:, None],
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

    # Create implicit constraints and return lower bounds
    df_iter_mun = create_implicit_consts(df_iter_mun)

    df_iter_loc = create_implicit_consts(df_iter_loc)

    df_agebs = create_implicit_consts(df_agebs)

    return df_iter_mun, df_iter_loc, df_agebs


def merge_loc_agebs(df_mun, df_loc, df_agebs, impute=False):
    df_mun = df_mun.copy().sort_index()
    df_agebs = df_agebs.copy()
    df_loc = df_loc.copy()

    idx_to_drop = df_agebs.index.droplevel('AGEB').unique()
    df_loc_agebs = pd.concat(
        [
            (
                df_loc
                .drop(idx_to_drop)
                .assign(AGEB='0000')
                .set_index('AGEB', append=True)
            ),
            df_agebs]
    ).sort_index().reset_index()
    df_loc_agebs['MUN'] = df_loc_agebs.MUN.map(mun_d)
    df_loc_agebs = df_loc_agebs.set_index(['MUN', 'LOC', 'AGEB']).sort_index()

    if not impute:
        return df_loc_agebs

    tot_cols = ['POBTOT', 'POBHOG', 'POBCOL', 'TVIVHAB', 'TOTHOG', 'TOTCOL']

    df_diff = df_mun[tot_cols] - df_loc_agebs.groupby('MUN').sum()[tot_cols]

    # If pobcol and tothog match municipality levels,
    # we can impute at ageb level
    for mun in df_mun.index:
        if np.isclose(df_diff.loc[mun, 'POBCOL'], 0):
            df_loc_agebs.loc[mun, 'POBHOG'] = (
                df_loc_agebs
                .loc[mun, 'POBHOG']
                .mask(
                    df_loc_agebs.loc[mun, 'POBHOG'].isna(),
                    df_loc_agebs.loc[mun, 'POBTOT']
                ).values
            )
        if np.isclose(df_diff.loc[mun, 'TOTCOL'], 0):
            df_loc_agebs.loc[mun, 'TOTHOG'] = (
                df_loc_agebs.loc[mun, 'TOTHOG']
                .mask(
                    df_loc_agebs.loc[mun, 'TOTHOG'].isna(),
                    df_loc_agebs.loc[mun, 'TVIVHAB']
                ).values
            )

    df_diff = df_mun[tot_cols] - df_loc_agebs.groupby('MUN').sum()[tot_cols]

    # Set lower bounds to 0
    df_loc_agebs = df_loc_agebs.fillna(0)

    # Add capacity columns
    df_loc_agebs['capacity_P'] = df_loc_agebs.POBTOT - (
        df_loc_agebs.POBHOG + df_loc_agebs.POBCOL)
    df_loc_agebs['capacity_H'] = df_loc_agebs.TVIVHAB - (
        df_loc_agebs.TOTHOG + df_loc_agebs.TOTCOL
    )

    # Add p/h ratio
    df_loc_agebs['ph_ratio'] = df_loc_agebs.POBTOT / df_loc_agebs.TVIVHAB

    # Assign pop and h
    for mun in df_mun.index:
        h_sup = df_diff.loc[mun, 'TOTCOL']
        p_sup = df_diff.loc[mun, 'POBCOL']
        if p_sup == 0:
            continue
        # So far we can handle a single household
        assert h_sup == 1

        # Find candidate with max ph_ratio and available capacity
        loc_idx, ageb_idx = (
            df_loc_agebs
            .loc[mun]
            .query(
                'capacity_P > 0 & capacity_P >= @p_sup & capacity_H > 0'
            ).ph_ratio.idxmax()
        )

        df_loc_agebs.loc[
            (mun, loc_idx, ageb_idx),
            ['POBCOL', 'TOTCOL']
        ] = p_sup, h_sup

    df_diff = df_mun[tot_cols] - df_loc_agebs.groupby('MUN').sum()[tot_cols]
    assert df_diff.POBCOL.sum() == 0
    assert df_diff.TOTCOL.sum() == 0

    # Now that collective population is assigned, make hogares equalities
    df_loc_agebs['POBHOG'] = df_loc_agebs.POBTOT - df_loc_agebs.POBCOL
    df_loc_agebs['TOTHOG'] = df_loc_agebs.TVIVHAB - df_loc_agebs.TOTCOL

    df_diff = df_mun[tot_cols] - df_loc_agebs.groupby('MUN').sum()[tot_cols]
    assert df_diff.sum().sum() == 0

    return df_loc_agebs.drop(columns=[
        'capacity_P', 'capacity_H', 'ph_ratio'
    ])
