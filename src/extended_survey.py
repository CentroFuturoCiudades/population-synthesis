import numpy as np
import pandas as pd
from categories import defs, cats


def code_ent(value, curr_state=19):
    if value == curr_state:
        return 'EstaEnt'
    elif value <= 32 or value == 997:
        return 'OtraEnt'
    elif value <= 535 or value == 998:
        return 'OtroPais'
    elif value == 999:
        return 'No especificado'
    elif np.isnan(value):
        return 'Blanco por pase'
    else:
        assert False


def code_religion(val):
    if val == 1101:
        return 'Católica'
    elif int(val/100) == 13:
        return 'Protestante/cristiano evangélico'
    elif val == 1201 or int(val/1000) == 2:
        return 'Otros credos'
    elif int(val/1000) == 3:
        return 'Sin religión / Sin adscripción religiosa'
    elif val == 9999:
        return 'Religión no especificada'
    else:
        assert False


def code_hlengua(row):
    # HESPANOL specifies is person speaks spanish IN ADDITION
    # to a native tongue.
    # If HLENGUA is not 'Si' then HESPANOL is always NAN.
    # We modify the categories of HLENGUA to
    # Si/No español, Si/Si español, Si/No especificado
    val1 = row.HLENGUA
    val2 = row.HESPANOL
    if val1 == 1:
        if val2 == 1:
            return 'Sí/Sí Español'
        elif val2 == 3:
            return 'Sí/No español'
        elif val2 == 9:
            return 'Sí/No especificado'
        else:
            assert False
    elif val1 == 3:
        return 'No'
    elif val1 == 9:
        return 'No especificado'
    elif np.isnan(val1):
        return 'Blanco por pase'
    else:
        assert False


def code_MUN_ASI(row, mun_col='MUN_ASI', ent_col='ENT_PAIS_ASI'):
    asi_mun = row[mun_col]
    c_or_ent = row[ent_col]

    if c_or_ent == 'Blanco por pase':
        return 'Blanco por pase'
    elif c_or_ent == 'No especificado':
        return 'No especificado'
    elif c_or_ent == 'OtroPais':
        return 'OtroPais'
    elif c_or_ent == 'OtraEnt':
        return 'OtraEnt'
    elif c_or_ent == 'EstaEnt':
        if asi_mun == 999:
            return 'No especificado'
        else:
            return defs['muns'][asi_mun]
    else:
        print(row)
        assert False


def code_dhsersal(row):
    v1 = row.DHSERSAL1
    v2 = row.DHSERSAL2
    if np.isnan(v2):
        return defs['dhsersal'][v1]
    else:
        return defs['dhsersal'][v1] + ' - ' + defs['dhsersal'][v2]


def code_nivacad(row):
    escolari = row.ESCOLARI
    nivacad = defs['nivacad'][row.NIVACAD]
    if escolari == 0 or escolari == 'Blanco por pase':
        return nivacad
    elif nivacad == 'No especificado':
        return nivacad
    else:
        return f'{nivacad}_{int(escolari)}'


def process_people_df(file_path):

    personas = pd.read_csv(file_path)

    # Household type is always Particular to use same categories as census
    personas_cat = personas[['ID_PERSONA', 'ID_VIV', 'FACTOR']].copy()

    personas_cat['MUN'] = personas.MUN.map(defs['muns']).astype(cats['muns'])

    personas_cat['CLAVIVP'] = personas.CLAVIVP.map(
        defs['clavivp']
    ).astype(cats['clavivp'])

    personas_cat['SEXO'] = personas.SEXO.map(defs['sexo']).astype(cats['sexo'])

    personas_cat['EDAD'] = pd.cut(
        personas.EDAD,
        (0, 3, 5, 6, 8, 12, 15, 18, 25, 50, 60, 65, 131, 1000),
        right=False,
        labels=cats['edad']
    )

    personas_cat['ENT_PAIS_NAC'] = personas.ENT_PAIS_NAC.apply(
        code_ent
    ).astype(cats['ent'])

    personas_cat['PARENTESCO'] = personas.PARENTESCO.map(
        defs['parentesco']
    ).astype(cats['parentesco'])

    personas_cat['NACIONALIDAD'] = personas.NACIONALIDAD.map(
        defs['sino_139']
    ).astype(cats['sino_139'])

    personas_cat['SERSALUD'] = personas.SERSALUD.map(
        defs['sersalud']
    ).astype(cats['sersalud'])

    personas_cat['AFRODES'] = personas.AFRODES.map(
        defs['sino_139']
    ).astype(cats['sino_139'])

    # Since the categories for health services are not mutually exclusive,
    # we use a binary column per service.
    # dhsersal1_dummies = pd.get_dummies(
    #     personas.DHSERSAL1.map(defs['dhsersal']),
    #     prefix='DHSERSAL'
    # )
    # dhsersal2_dummies = pd.get_dummies(
    #     personas.DHSERSAL2.map(
    #         defs['dhsersal']),
    #     prefix='DHSERSAL'
    # )
    # personas_cat = pd.concat(
    #     [
    #         personas_cat,
    #         dhsersal1_dummies.add(
    #             dhsersal2_dummies, fill_value=0
    #         ).astype(int).astype('category')
    #     ],
    #     axis=1
    # )

    dhsersal1_dummies = pd.get_dummies(
            personas.DHSERSAL1.map(defs['dhsersal']),
        )
    dhsersal2_dummies = pd.get_dummies(
            personas.DHSERSAL2.map(defs['dhsersal']),
        )
    dhsercal_or_cats = list(defs['dhsersal'].values())
    dhsersar_df = dhsersal1_dummies.add(
                    dhsersal2_dummies, fill_value=0
                )[dhsercal_or_cats].astype(int).astype(str)
    dhsersal_series = dhsersar_df[dhsercal_or_cats[0]]
    for c in dhsercal_or_cats[1:]:
        dhsersal_series += dhsersar_df[c]
    personas_cat['DHSERSAL'] = dhsersal_series.astype(cats['dhsersal'])

    personas_cat['RELIGION'] = personas.RELIGION.apply(
        code_religion
    ).astype(cats['religion'])

    # personas_cat['DIS_VER'] = personas.DIS_VER.map(
    #     defs['dis']).astype(cats['dis'])
    # personas_cat['DIS_OIR'] = personas.DIS_OIR.map(
    #     defs['dis']).astype(cats['dis'])
    # personas_cat['DIS_CAMINAR'] = personas.DIS_CAMINAR.map(
    #     defs['dis']).astype(cats['dis'])
    # personas_cat['DIS_RECORDAR'] = personas.DIS_RECORDAR.map(
    #     defs['dis']).astype(cats['dis'])
    # personas_cat['DIS_BANARSE'] = personas.DIS_BANARSE.map(
    #     defs['dis']).astype(cats['dis'])
    # personas_cat['DIS_HABLAR'] = personas.DIS_HABLAR.map(
    #     defs['dis']).astype(cats['dis'])

    # personas_cat['DIS_MENTAL'] = personas.DIS_MENTAL.map(
    #     defs['dis_mental']).astype(cats['dis_mental'])
    personas_cat['DIS'] = (
        personas.DIS_VER.astype(str)
        + personas.DIS_OIR.astype(str)
        + personas.DIS_CAMINAR.astype(str)
        + personas.DIS_RECORDAR.astype(str)
        + personas.DIS_BANARSE.astype(str)
        + personas.DIS_HABLAR.astype(str)
        + personas.DIS_MENTAL.astype(str)
    ).astype(cats['dis'])

    personas_cat['HLENGUA'] = personas[['HLENGUA', 'HESPANOL']].apply(
        code_hlengua, axis=1).astype(cats['hlengua'])

    personas_cat['ELENGUA'] = personas.ELENGUA.map(defs['elengua'])
    personas_cat.loc[personas.HLENGUA == 1, 'ELENGUA'] = 'Sí'
    personas_cat['ELENGUA'] = personas_cat['ELENGUA'].fillna(
        'Blanco por pase').astype(cats['elengua'])

    personas_cat['PERTE_INDIGENA'] = personas.PERTE_INDIGENA.fillna(
        'Blanco por pase').map(defs['asisten']).astype(cats['asisten'])

    personas_cat['ASISTEN'] = personas.ASISTEN.fillna('Blanco por pase').map(
        defs['asisten']).astype(cats['asisten'])

    personas_cat['ENT_PAIS_ASI'] = personas.ENT_PAIS_ASI.apply(
        code_ent).astype(cats['ent'])
    personas_cat['MUN_ASI'] = pd.concat(
        [
            personas[['MUN_ASI']],
            personas_cat[['ENT_PAIS_ASI']]
        ],
        axis=1).apply(code_MUN_ASI, axis=1).astype(cats['mun_asi'])

    personas_cat['TIE_TRASLADO_ESCU'] = personas.TIE_TRASLADO_ESCU.fillna(
        'Blanco por pase').map(
            defs['tie_traslado']).astype(cats['tie_traslado'])

    med_traslado_esc1_dummies = pd.get_dummies(
        personas.MED_TRASLADO_ESC1.fillna('Blanco por pase').map(
            defs['med_traslado']), prefix='MED_TRASLADO_ESC')
    med_traslado_esc2_dummies = pd.get_dummies(
        personas.MED_TRASLADO_ESC2.fillna('Blanco por pase').map(
            defs['med_traslado']), prefix='MED_TRASLADO_ESC')
    med_traslado_esc3_dummies = pd.get_dummies(
        personas.MED_TRASLADO_ESC3.fillna('Blanco por pase').map(
            defs['med_traslado']), prefix='MED_TRASLADO_ESC')
    personas_cat = pd.concat(
        [
            personas_cat,
            med_traslado_esc1_dummies.add(
                med_traslado_esc2_dummies,
                fill_value=0).add(
                    med_traslado_esc3_dummies,
                    fill_value=0).astype(int).replace(
                        {2: 1, 3: 1}).astype('category'),
        ],
        axis=1
    )

    personas_cat['NIVACAD'] = personas[['NIVACAD', 'ESCOLARI']].fillna(
        'Blanco por pase').apply(
            code_nivacad, axis=1).astype(cats['nivacad'])

    # personas_cat['ESCOLARI'] = personas.ESCOLARI.fillna(
    #     'Blanco por pase').astype(
    #         pd.CategoricalDtype(
    #             [0, 1, 2, 3, 4, 5, 6, 7, 8, 99, 'Blanco por pase'])
    #     )

    personas_cat['ALFABET'] = personas.ALFABET.fillna('Blanco por pase').map(
        defs['alfabet']).astype(cats['alfabet'])

    personas_cat['ENT_PAIS_RES_5A'] = personas.ENT_PAIS_RES_5A.apply(
        code_ent).astype(cats['ent'])

    personas_cat['MUN_RES_5A'] = pd.concat(
        [
            personas[['MUN_RES_5A']],
            personas_cat[['ENT_PAIS_RES_5A']]],
        axis=1
    ).apply(
        code_MUN_ASI,
        axis=1,
        mun_col='MUN_RES_5A',
        ent_col='ENT_PAIS_RES_5A'
    ).astype(cats['mun_asi'])

    personas_cat['SITUA_CONYUGAL'] = personas.SITUA_CONYUGAL.fillna(
        'Blanco por pase').map(
            defs['situa_conyugal']).astype(
                cats['situa_conyugal'])

    personas_cat['CONACT'] = personas.CONACT.fillna('Blanco por pase').map(
        defs['conact']).astype(cats['conact'])

    personas_cat['OCUPACION_C'] = np.floor(personas.OCUPACION_C/10).fillna(
        'Blanco por pase').map(
            defs['ocupacion_compact']).astype(cats['ocupacion_compact'])

    personas_cat['SITTRA'] = personas.SITTRA.fillna('Blanco por pase').map(
        defs['sittra']).astype(cats['sittra'])

    personas_cat['AGUINALDO'] = personas.AGUINALDO.fillna(
        'Blanco por pase').map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['VACACIONES'] = personas.VACACIONES.fillna(
        'Blanco por pase').map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['SERVICIO_MEDICO'] = personas.SERVICIO_MEDICO.fillna(
        'Blanco por pase').map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['UTILIDADES'] = personas.UTILIDADES.fillna(
        'Blanco por pase').map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['INCAP_SUELDO'] = personas.INCAP_SUELDO.fillna(
        'Blanco por pase').map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['SAR_AFORE'] = personas.SAR_AFORE.fillna(
        'Blanco por pase').map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['CREDITO_VIVIENDA'] = personas.CREDITO_VIVIENDA.fillna(
        'Blanco por pase').map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['INGTRMEN'] = pd.cut(
        personas.INGTRMEN.fillna(2e6),
        (0, 1000, 5000, 10000, 20000, 40000, 80000, 150000, 999999, 1e6, 3e6),
        right=False,
        labels=[
            '0-999', '1,000-4,999', '5,000-9,999', '10,000-19,999',
            '20,000-39,999', '40,000-79,999', '80,000-149,999',
            '150,000yMas', 'No especificado', 'Blanco por pase'
        ]
    )

    personas_cat['HORTRA'] = pd.cut(
        personas.HORTRA.fillna(2e6),
        [-1, 5, 10, 20, 40, 48, 56, 60, 80, 1e6, 3e6],
        right=True,
        labels=[
            '0-5', '6-10', '11-20', '21-40', '41-48', '49-56',
            '57-60', '61-80', '80YMAS', 'Blanco por pase'
        ]
    )

    personas_cat['ACTIVIDADES_C'] = np.floor(
        personas.ACTIVIDADES_C/100).fillna(
            'Blanco por pase').map(
                defs['actividades']).astype(cats['actividades'])

    personas_cat['ENT_PAIS_TRAB'] = personas.ENT_PAIS_TRAB.apply(
        code_ent).astype(cats['ent'])

    personas_cat['MUN_TRAB'] = pd.concat(
        [
            personas[['MUN_TRAB']],
            personas_cat[['ENT_PAIS_TRAB']]
        ],
        axis=1
    ).apply(
        code_MUN_ASI,
        mun_col='MUN_TRAB',
        ent_col='ENT_PAIS_TRAB',
        axis=1).astype(cats['mun_asi'])

    personas_cat['TIE_TRASLADO_TRAB'] = personas.TIE_TRASLADO_TRAB.fillna(
        'Blanco por pase').map(
            defs['tie_traslado_trab']).astype(cats['tie_traslado_trab'])

    med_traslado_trab1_dummies = pd.get_dummies(
        personas.MED_TRASLADO_TRAB1.fillna(
            'Blanco por pase').map(
                defs['med_traslado']), prefix='MED_TRASLADO_TRAB')
    med_traslado_trab2_dummies = pd.get_dummies(
        personas.MED_TRASLADO_TRAB2.fillna(
            'Blanco por pase').map(
                defs['med_traslado']), prefix='MED_TRASLADO_TRAB')
    med_traslado_trab3_dummies = pd.get_dummies(
        personas.MED_TRASLADO_TRAB3.fillna(
            'Blanco por pase').map(
                defs['med_traslado']), prefix='MED_TRASLADO_TRAB')
    personas_cat = pd.concat([
        personas_cat,
        med_traslado_trab1_dummies.add(
            med_traslado_trab2_dummies, fill_value=0).add(
                med_traslado_trab3_dummies, fill_value=0).astype(
                    int).replace({2: 1, 3: 1}).astype('category'),
    ], axis=1)

    assert personas_cat.isna().sum().sum() == 0

    cols_to_drop = [
        'NACIONALIDAD', 'SERSALUD', 'ELENGUA', 'PERTE_INDIGENA',
        'ENT_PAIS_ASI', 'ENT_PAIS_RES_5A', 'AGUINALDO', 'VACACIONES',
        'SERVICIO_MEDICO', 'UTILIDADES', 'INCAP_SUELDO', 'SAR_AFORE',
        'CREDITO_VIVIENDA', 'ENT_PAIS_TRAB'
    ]

    # personas_cat = personas_cat.drop(columns=cols_to_drop)

    # Split by municipality, the finer aggregation level
    # statistically representative in the survey.
    groups = personas_cat.groupby('MUN')
    group_dict = {mun: df for mun, df in groups}

    return group_dict
