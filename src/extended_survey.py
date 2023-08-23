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


nivacad_posmap = {
    'Ninguno': 'Sin Educación',
    'Preescolar_1': 'Sin Educación',
    'Preescolar_2': 'Sin Educación',
    'Preescolar_3': 'Sin Educación',
    'Preescolar_99': 'Sin Educación',

    'Primaria_1': 'Primaria_incom',
    'Primaria_2': 'Primaria_incom',
    'Primaria_3': 'Primaria_incom',
    'Primaria_4': 'Primaria_incom',
    'Primaria_5': 'Primaria_incom',
    'Primaria_6': 'Primaria_com',
    'Primaria_99': 'Primaria_incom',

    'Estudios técnicos o comerciales con primaria terminada_1': 'EToC_prim',
    'Estudios técnicos o comerciales con primaria terminada_2': 'EToC_prim',
    'Estudios técnicos o comerciales con primaria terminada_3': 'EToC_prim',
    'Estudios técnicos o comerciales con primaria terminada_4': 'EToC_prim',
    'Estudios técnicos o comerciales con primaria terminada_99': 'EToC_prim',

    'Secundaria_1': 'Secundaria_incom',
    'Secundaria_2': 'Secundaria_incom',
    'Secundaria_3': 'Secundaria_com',
    'Secundaria_99': 'Secundaria_incom',

    'Preparatoria o bachillerato general_1': 'Preparatoria',
    'Preparatoria o bachillerato general_2': 'Preparatoria',
    'Preparatoria o bachillerato general_3': 'Preparatoria',
    'Preparatoria o bachillerato general_4': 'Preparatoria',
    'Preparatoria o bachillerato general_99': 'Preparatoria',

    'Bachillerato tecnológico_1': 'Bachillerato tecnológico',
    'Bachillerato tecnológico_2': 'Bachillerato tecnológico',
    'Bachillerato tecnológico_3': 'Bachillerato tecnológico',
    'Bachillerato tecnológico_4': 'Bachillerato tecnológico',
    'Bachillerato tecnológico_99': 'Bachillerato tecnológico',

    'Estudios técnicos o comerciales con secundaria terminada_1': 'EToC_sec',
    'Estudios técnicos o comerciales con secundaria terminada_2': 'EToC_sec',
    'Estudios técnicos o comerciales con secundaria terminada_3': 'EToC_sec',
    'Estudios técnicos o comerciales con secundaria terminada_4': 'EToC_sec',
    'Estudios técnicos o comerciales con secundaria terminada_5': 'EToC_sec',
    'Estudios técnicos o comerciales con secundaria terminada_99': 'EToC_sec',

    'Estudios técnicos o comerciales con preparatoria terminada_1': 'EToC_prep',
    'Estudios técnicos o comerciales con preparatoria terminada_2': 'EToC_prep',
    'Estudios técnicos o comerciales con preparatoria terminada_3': 'EToC_prep',
    'Estudios técnicos o comerciales con preparatoria terminada_4': 'EToC_prep',
    'Estudios técnicos o comerciales con preparatoria terminada_99': 'EToC_prep',

    'Normal con primaria o secundaria terminada_1': 'Normal prim/sec term',
    'Normal con primaria o secundaria terminada_2': 'Normal prim/sec term',
    'Normal con primaria o secundaria terminada_3': 'Normal prim/sec term',
    'Normal con primaria o secundaria terminada_4': 'Normal prim/sec term',
    'Normal con primaria o secundaria terminada_99': 'Normal prim/sec term',

    'Normal de licenciatura_1': 'Normal de licenciatura',
    'Normal de licenciatura_2': 'Normal de licenciatura',
    'Normal de licenciatura_3': 'Normal de licenciatura',
    'Normal de licenciatura_4': 'Normal de licenciatura',
    'Normal de licenciatura_5': 'Normal de licenciatura',
    'Normal de licenciatura_6': 'Normal de licenciatura',
    'Normal de licenciatura_99': 'Normal de licenciatura',

    'Licenciatura_1': 'Licenciatura',
    'Licenciatura_2': 'Licenciatura',
    'Licenciatura_3': 'Licenciatura',
    'Licenciatura_4': 'Licenciatura',
    'Licenciatura_5': 'Licenciatura',
    'Licenciatura_6': 'Licenciatura',
    'Licenciatura_7': 'Licenciatura',
    'Licenciatura_8': 'Licenciatura',
    'Licenciatura_99': 'Licenciatura',

    'Especialidad_1': 'Especialidad',
    'Especialidad_2': 'Especialidad',
    'Especialidad_99': 'Especialidad',

    'Maestría_1': 'Maestría',
    'Maestría_2': 'Maestría',
    'Maestría_3': 'Maestría',
    'Maestría_4': 'Maestría',
    'Maestría_5': 'Maestría',
    'Maestría_6': 'Maestría',
    'Maestría_99': 'Maestría',

    'Doctorado_1': 'Doctorado',
    'Doctorado_2': 'Doctorado',
    'Doctorado_3': 'Doctorado',
    'Doctorado_4': 'Doctorado',
    'Doctorado_5': 'Doctorado',
    'Doctorado_6': 'Doctorado',
    'Doctorado_99': 'Doctorado',

    'No especificado': 'No especificado',
    'Blanco por pase': 'Blanco por pase'
}


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
        code_nivacad, axis=1).map(nivacad_posmap).astype(
            pd.CategoricalDtype(list(set(nivacad_posmap.values()))))

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


def process_places_df(file_path, to_drop=[]):

    viviendas = pd.read_csv(file_path)

    viviendas_cat = viviendas[['ID_VIV', 'FACTOR']].copy()

    viviendas_cat['MUN'] = viviendas.MUN.map(defs['muns']).astype(cats['muns'])

    viviendas_cat['CLAVIVP'] = viviendas.CLAVIVP.map(
        defs['clavivp']
    ).astype(cats['clavivp'])

    viviendas_cat['PAREDES'] = viviendas.PAREDES.fillna(
        'Blanco por pase').map(defs['paredes']).astype(cats['paredes'])

    viviendas_cat['TECHOS'] = viviendas.TECHOS.fillna(
        'Blanco por pase').map(defs['techos']).astype(cats['techos'])

    viviendas_cat['PISOS'] = viviendas.PISOS.fillna(
        'Blanco por pase').map(defs['pisos']).astype(cats['pisos'])

    viviendas_cat['COCINA'] = viviendas.COCINA.fillna(
        'Blanco por pase').map(defs['cocina']).astype(cats['cocina'])

    viviendas_cat['CUADORM'] = viviendas.CUADORM.fillna(
        'Blanco por pase').map(defs['cuadorm']).astype(cats['cuadorm'])

    viviendas_cat['TOTCUART'] = viviendas.TOTCUART.fillna(
        'Blanco por pase').map(defs['totcuart']).astype(cats['totcuart'])

    viviendas_cat['LUG_COC'] = viviendas.LUG_COC.fillna(
        'Blanco por pase').map(defs['lug_coc']).astype(cats['lug_coc'])

    viviendas_cat['COMBUSTIBLE'] = viviendas.COMBUSTIBLE.fillna(
        'Blanco por pase').map(defs['combustible']).astype(cats['combustible'])

    viviendas_cat['ESTUFA'] = viviendas.ESTUFA.fillna(
        'Blanco por pase').map(defs['estufa']).astype(cats['estufa'])

    viviendas_cat['ELECTRICIDAD'] = viviendas.ELECTRICIDAD.fillna(
        'Blanco por pase').map(
            defs['electricidad']).astype(cats['electricidad'])

    viviendas_cat['FOCOS'] = viviendas.FOCOS.fillna(
        'Blanco por pase').map(
            defs['focos']).astype(cats['focos'])

    viviendas_cat['FOCOS_AHORRA'] = viviendas.FOCOS_AHORRA.fillna(
        'Blanco por pase').map(
            defs['focos_ahorra']).astype(cats['focos_ahorra'])

    viviendas_cat['AGUA_ENTUBADA'] = viviendas.AGUA_ENTUBADA.fillna(
        'Blanco por pase').map(
            defs['agua_entubada']).astype(cats['agua_entubada'])

    viviendas_cat['ABA_AGUA_ENTU'] = viviendas.ABA_AGUA_ENTU.fillna(
        'Blanco por pase').map(
            defs['aba_agua_entu']).astype(cats['aba_agua_entu'])

    viviendas_cat['ABA_AGUA_NO_ENTU'] = viviendas.ABA_AGUA_NO_ENTU.fillna(
        'Blanco por pase').map(
            defs['aba_agua_no_entu']).astype(cats['aba_agua_no_entu'])

    viviendas_cat['TINACO'] = viviendas.TINACO.fillna(
        'Blanco por pase').map(
            defs['tinaco']).astype(cats['tinaco'])

    viviendas_cat['CISTERNA'] = viviendas.CISTERNA.fillna(
        'Blanco por pase').map(
            defs['cisterna']).astype(cats['cisterna'])

    viviendas_cat['BOMBA_AGUA'] = viviendas.BOMBA_AGUA.fillna(
        'Blanco por pase').map(
            defs['bomba_agua']).astype(cats['bomba_agua'])

    viviendas_cat['REGADERA'] = viviendas.REGADERA.fillna(
        'Blanco por pase').map(
            defs['regadera']).astype(cats['regadera'])

    viviendas_cat['BOILER'] = viviendas.BOILER.fillna(
        'Blanco por pase').map(
            defs['boiler']).astype(cats['boiler'])

    viviendas_cat['CALENTADOR_SOLAR'] = viviendas.CALENTADOR_SOLAR.fillna(
        'Blanco por pase').map(
            defs['calentador_solar']).astype(cats['calentador_solar'])

    viviendas_cat['AIRE_ACON'] = viviendas.AIRE_ACON.fillna(
        'Blanco por pase').map(
            defs['aire_acon']).astype(cats['aire_acon'])

    viviendas_cat['PANEL_SOLAR'] = viviendas.PANEL_SOLAR.fillna(
        'Blanco por pase').map(
            defs['panel_solar']).astype(cats['panel_solar'])

    viviendas_cat['SERSAN'] = viviendas.SERSAN.fillna(
        'Blanco por pase').map(
            defs['sersan']).astype(cats['sersan'])

    viviendas_cat['CONAGUA'] = viviendas.CONAGUA.fillna(
        'Blanco por pase').map(
            defs['conagua']).astype(cats['conagua'])

    viviendas_cat['USOEXC'] = viviendas.USOEXC.fillna(
        'Blanco por pase').map(
            defs['usoexc']).astype(cats['usoexc'])

    viviendas_cat['DRENAJE'] = viviendas.DRENAJE.fillna(
        'Blanco por pase').map(
            defs['drenaje']).astype(cats['drenaje'])

    viviendas_cat['SEPARACION1'] = viviendas.SEPARACION1.fillna(
        'Blanco por pase').map(
            defs['separacion1']).astype(cats['separacion1'])

    viviendas_cat['SEPARACION2'] = viviendas.SEPARACION2.fillna(
        'Blanco por pase').map(
            defs['separacion2']).astype(cats['separacion2'])

    viviendas_cat['SEPARACION3'] = viviendas.SEPARACION3.fillna(
        'Blanco por pase').map(
            defs['separacion3']).astype(cats['separacion3'])

    viviendas_cat['SEPARACION4'] = viviendas.SEPARACION4.fillna(
        'Blanco por pase').map(
            defs['separacion4']).astype(cats['separacion4'])

    viviendas_cat['DESTINO_BAS'] = viviendas.DESTINO_BAS.fillna(
        'Blanco por pase').map(
            defs['destino_bas']).astype(cats['destino_bas'])

    viviendas_cat['REFRIGERADOR'] = viviendas.REFRIGERADOR.fillna(
        'Blanco por pase').map(
            defs['refrigerador']).astype(cats['refrigerador'])

    viviendas_cat['LAVADORA'] = viviendas.LAVADORA.fillna(
        'Blanco por pase').map(
            defs['lavadora']).astype(cats['lavadora'])

    viviendas_cat['HORNO'] = viviendas.HORNO.fillna(
        'Blanco por pase').map(
            defs['horno']).astype(cats['horno'])

    viviendas_cat['AUTOPROP'] = viviendas.AUTOPROP.fillna(
        'Blanco por pase').map(
            defs['autoprop']).astype(cats['autoprop'])

    viviendas_cat['MOTOCICLETA'] = viviendas.MOTOCICLETA.fillna(
        'Blanco por pase').map(
            defs['motocicleta']).astype(cats['motocicleta'])

    viviendas_cat['BICICLETA'] = viviendas.BICICLETA.fillna(
        'Blanco por pase').map(
            defs['bicicleta']).astype(cats['bicicleta'])

    viviendas_cat['RADIO'] = viviendas.RADIO.fillna(
        'Blanco por pase').map(
            defs['radio']).astype(cats['radio'])

    viviendas_cat['TELEVISOR'] = viviendas.TELEVISOR.fillna(
        'Blanco por pase').map(
            defs['televisor']).astype(cats['televisor'])

    viviendas_cat['COMPUTADORA'] = viviendas.COMPUTADORA.fillna(
        'Blanco por pase').map(
            defs['computadora']).astype(cats['computadora'])

    viviendas_cat['TELEFONO'] = viviendas.TELEFONO.fillna(
        'Blanco por pase').map(
            defs['telefono']).astype(cats['telefono'])

    viviendas_cat['CELULAR'] = viviendas.CELULAR.fillna(
        'Blanco por pase').map(
            defs['celular']).astype(cats['celular'])

    viviendas_cat['INTERNET'] = viviendas.INTERNET.fillna(
        'Blanco por pase').map(
            defs['internet']).astype(cats['internet'])

    viviendas_cat['SERV_TV_PAGA'] = viviendas.SERV_TV_PAGA.fillna(
        'Blanco por pase').map(
            defs['serv_tv_paga']).astype(cats['serv_tv_paga'])

    viviendas_cat['SERV_PEL_PAGA'] = viviendas.SERV_PEL_PAGA.fillna(
        'Blanco por pase').map(
            defs['serv_pel_paga']).astype(cats['serv_pel_paga'])

    viviendas_cat['CON_VJUEGOS'] = viviendas.CON_VJUEGOS.fillna(
        'Blanco por pase').map(
            defs['con_vjuegos']).astype(cats['con_vjuegos'])

    viviendas_cat['TENENCIA'] = viviendas.TENENCIA.fillna(
        'Blanco por pase').map(
            defs['tenencia']).astype(cats['tenencia'])

    viviendas_cat['ESCRITURAS'] = viviendas.ESCRITURAS.fillna(
        'Blanco por pase').map(
            defs['escrituras']).astype(cats['escrituras'])

    viviendas_cat['FORMA_ADQUI'] = viviendas.FORMA_ADQUI.fillna(
        'Blanco por pase').map(
            defs['forma_adqui']).astype(cats['forma_adqui'])

    viviendas_cat['FINANCIAMIENTO1'] = viviendas.FINANCIAMIENTO1.fillna(
        'Blanco por pase').map(
            defs['financiamiento1']).astype(cats['financiamiento1'])

    viviendas_cat['FINANCIAMIENTO2'] = viviendas.FINANCIAMIENTO2.fillna(
        'Blanco por pase').map(
            defs['financiamiento2']).astype(cats['financiamiento2'])

    viviendas_cat['FINANCIAMIENTO3'] = viviendas.FINANCIAMIENTO3.fillna(
        'Blanco por pase').map(
            defs['financiamiento3']).astype(cats['financiamiento3'])

    viviendas_cat['DEUDA'] = viviendas.DEUDA.fillna(
        'Blanco por pase').map(
            defs['deuda']).astype(cats['deuda'])

    viviendas_cat['NUMPERS'] = viviendas.NUMPERS.astype('category')

    viviendas_cat['MCONMIG'] = viviendas.MCONMIG.fillna(
        'Blanco por pase').map(
            defs['mconmig']).astype(cats['mconmig'])

    viviendas_cat['MNUMPERS'] = viviendas.MNUMPERS.fillna(
        'Blanco por pase').astype('category')

    viviendas_cat['INGR_PEROTROPAIS'] = viviendas.INGR_PEROTROPAIS.fillna(
        'Blanco por pase').map(
            defs['ingr_perotropais']).astype(cats['ingr_perotropais'])

    viviendas_cat['INGR_PERDENTPAIS'] = viviendas.INGR_PERDENTPAIS.fillna(
        'Blanco por pase').map(
            defs['ingr_perdentpais']).astype(cats['ingr_perdentpais'])

    viviendas_cat['INGR_AYUGOB'] = viviendas.INGR_AYUGOB.fillna(
        'Blanco por pase').map(
            defs['ingr_ayugob']).astype(cats['ingr_ayugob'])

    viviendas_cat['INGR_JUBPEN'] = viviendas.INGR_JUBPEN.fillna(
        'Blanco por pase').map(
            defs['ingr_jubpen']).astype(cats['ingr_jubpen'])

    viviendas_cat['ALIMENTACION'] = viviendas.ALIMENTACION.fillna(
        'Blanco por pase').map(
            defs['alimentacion']).astype(cats['alimentacion'])

    viviendas_cat['ALIM_ADL1'] = viviendas.ALIM_ADL1.fillna(
        'Blanco por pase').map(
            defs['alim_adl1']).astype(cats['alim_adl1'])

    viviendas_cat['ALIM_ADL2'] = viviendas.ALIM_ADL2.fillna(
        'Blanco por pase').map(
            defs['alim_adl2']).astype(cats['alim_adl2'])

    viviendas_cat['ING_ALIM_ADL1'] = viviendas.ING_ALIM_ADL1.fillna(
        'Blanco por pase').map(
            defs['ing_alim_adl1']).astype(cats['ing_alim_adl1'])

    viviendas_cat['ING_ALIM_ADL2'] = viviendas.ING_ALIM_ADL2.fillna(
        'Blanco por pase').map(
            defs['ing_alim_adl2']).astype(cats['ing_alim_adl2'])

    viviendas_cat['ING_ALIM_ADL3'] = viviendas.ING_ALIM_ADL3.fillna(
        'Blanco por pase').map(
            defs['ing_alim_adl3']).astype(cats['ing_alim_adl3'])

    viviendas_cat['TIPOHOG'] = viviendas.TIPOHOG.fillna(
        'Blanco por pase').map(
            defs['tipohog']).astype(cats['tipohog'])

    viviendas_cat['INGTRHOG'] = pd.cut(
        viviendas.INGTRHOG.fillna(2e6),
        (0, 1000, 5000, 10000, 20000, 40000, 80000, 150000, 999999, 1e6, 3e6),
        right=False,
        labels=[
            '0-999', '1,000-4,999', '5,000-9,999', '10,000-19,999',
            '20,000-39,999', '40,000-79,999', '80,000-149,999',
            '150,000yMas', 'No especificado', 'Blanco por pase'
        ]
    )

    viviendas_cat['JEFE_SEXO'] = viviendas.JEFE_SEXO.map(
        defs['sexo']).astype(cats['sexo'])

    viviendas_cat['JEFE_EDAD'] = pd.cut(
        viviendas.JEFE_EDAD,
        (0, 3, 5, 6, 8, 12, 15, 18, 25, 50, 60, 65, 131, 1000),
        right=False,
        labels=cats['edad']
    )

    assert viviendas_cat.isna().sum().sum() == 0

    # cols_to_drop = [
    #     'NACIONALIDAD', 'SERSALUD', 'ELENGUA', 'PERTE_INDIGENA',
    #     'ENT_PAIS_ASI', 'ENT_PAIS_RES_5A', 'AGUINALDO', 'VACACIONES',
    #     'SERVICIO_MEDICO', 'UTILIDADES', 'INCAP_SUELDO', 'SAR_AFORE',
    #     'CREDITO_VIVIENDA', 'ENT_PAIS_TRAB'
    # ]

    # viviendas_cat = viviendas_cat.drop(columns=cols_to_drop)

    # Split by municipality, the finer aggregation level
    # statistically representative in the survey.
    viviendas_cat = viviendas_cat.drop(columns=to_drop)

    groups = viviendas_cat.groupby('MUN')
    group_dict = {mun: df.set_index('ID_VIV') for mun, df in groups}

    return group_dict


def places_postproc(df):

    # ID columns
    id_cols = [
        'FACTOR',
        'MUN'
    ]

    # Columns controlled by census
    census_cols = [
        'ABA_AGUA_ENTU',
        'AGUA_ENTUBADA',
        'AUTOPROP',
        'BICICLETA',
        'CELULAR',
        'CISTERNA',
        'COMPUTADORA',
        'CONAGUA',
        'CON_VJUEGOS',
        'CUADORM',  # ISNUM
        'DRENAJE',
        'ELECTRICIDAD',
        'HORNO',
        'INTERNET',
        'JEFE_SEXO',
        'LAVADORA',
        'MOTOCICLETA',
        'PISOS',
        'RADIO',
        'REFRIGERADOR',
        'SERSAN',
        'SERV_PEL_PAGA',
        'SERV_TV_PAGA',
        'TELEFONO',
        'TELEVISOR',
        'TINACO',
        'TOTCUART'  # ISNUM
    ]

    # Columns only in extended survey
    extended_cols = [
        'ABA_AGUA_NO_ENTU',
        'AIRE_ACON',
        'ALIMENTACION',
        'ALIM_ADL1',
        'ALIM_ADL2',
        'BOILER',
        'BOMBA_AGUA',
        'CALENTADOR_SOLAR',
        'COCINA',
        'COMBUSTIBLE',
        'DESTINO_BAS',
        'DEUDA',
        'ESCRITURAS',
        'ESTUFA',
        'FINANCIAMIENTO1',  # Needs encoding
        'FINANCIAMIENTO2',  # Needs encoding
        'FINANCIAMIENTO3',  # Needs encoding
        'FOCOS',  # ISNUM
        'FOCOS_AHORRA',  #ISNUM
        'FORMA_ADQUI',
        'INGR_AYUGOB',
        'INGR_JUBPEN',
        'INGR_PERDENTPAIS',
        'INGR_PEROTROPAIS',
        'ING_ALIM_ADL1',
        'ING_ALIM_ADL2',
        'ING_ALIM_ADL3',
        'LUG_COC',
        'MCONMIG',
        'MNUMPERS',  #ISNUM
        'PANEL_SOLAR',
        'PAREDES',
        'REGADERA',
        'SEPARACION1',
        'SEPARACION2',
        'SEPARACION3',
        'SEPARACION4',
        'TECHOS',
        'TENENCIA',
        'USOEXC'
    ]

    # Columns related to household structure and form
    household_cols = [
        'CLAVIVP', 'NUMPERS', 'INGTRHOG', 'JEFE_EDAD', 'TIPOHOG',
    ]


def people_postproc(df):
    pass
