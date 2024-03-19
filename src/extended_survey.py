import numpy as np
import pandas as pd
from categories import defs, cats

BPP = 'Blanco por pase'
SI = 'Sí'
NO = 'No'


def code_ent(value, curr_state=19):
    if value == curr_state:
        return 'EstaEnt'
    elif value <= 32 or value == 997:
        return 'OtraEnt'
    elif value <= 535 or value == 998:
        return 'OtroPais'
    elif value == 999:
        return np.nan
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
        return np.nan
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

    if c_or_ent == BPP:
        return BPP
    elif c_or_ent == 'OtroPais':
        return 'OtroPais'
    elif c_or_ent == 'OtraEnt':
        return 'OtraEnt'
    elif c_or_ent == 'EstaEnt':
        if asi_mun == 999:
            return np.nan
        else:
            return defs['muns'][asi_mun]
    elif np.isnan(c_or_ent):
        return np.nan
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
    # nivacad = defs['nivacad'][row.NIVACAD]
    nivacad = row.NIVACAD
    if escolari == 0 or escolari == 'Blanco por pase':
        return nivacad
    elif nivacad == 'No especificado':
        return nivacad
    else:
        return f'{nivacad}_{int(escolari)}'


nivacad_posmap = {
    'Ninguno_0': 'Sin Educación',
    'Preescolar_1': 'Sin Educación',
    'Preescolar_2': 'Sin Educación',
    'Preescolar_3': 'Sin Educación',
    'Preescolar_nan': 'Sin Educación',

    'Primaria_1': 'Primaria_incom',
    'Primaria_2': 'Primaria_incom',
    'Primaria_3': 'Primaria_incom',
    'Primaria_4': 'Primaria_incom',
    'Primaria_5': 'Primaria_incom',
    'Primaria_6': 'Primaria_com',
    'Primaria_nan': 'Primaria_incom',

    'Estudios técnicos o comerciales con primaria terminada_1': 'Primaria_com',
    'Estudios técnicos o comerciales con primaria terminada_2': 'Primaria_com',
    'Estudios técnicos o comerciales con primaria terminada_3': 'Primaria_com',
    'Estudios técnicos o comerciales con primaria terminada_4': 'Primaria_com',
    'Estudios técnicos o comerciales con primaria terminada_nan': 'Primaria_com',

    'Secundaria_1': 'Secundaria_incom',
    'Secundaria_2': 'Secundaria_incom',
    'Secundaria_3': 'Secundaria_com',
    'Secundaria_nan': 'Secundaria_incom',

    'Preparatoria o bachillerato general_1': 'Posbásica',
    'Preparatoria o bachillerato general_2': 'Posbásica',
    'Preparatoria o bachillerato general_3': 'Posbásica',
    'Preparatoria o bachillerato general_4': 'Posbásica',
    'Preparatoria o bachillerato general_nan': 'Posbásica',

    'Bachillerato tecnológico_1': 'Posbásica',
    'Bachillerato tecnológico_2': 'Posbásica',
    'Bachillerato tecnológico_3': 'Posbásica',
    'Bachillerato tecnológico_4': 'Posbásica',
    'Bachillerato tecnológico_nan': 'Posbásica',

    'Estudios técnicos o comerciales con secundaria terminada_1': 'Posbásica',
    'Estudios técnicos o comerciales con secundaria terminada_2': 'Posbásica',
    'Estudios técnicos o comerciales con secundaria terminada_3': 'Posbásica',
    'Estudios técnicos o comerciales con secundaria terminada_4': 'Posbásica',
    'Estudios técnicos o comerciales con secundaria terminada_5': 'Posbásica',
    'Estudios técnicos o comerciales con secundaria terminada_nan': 'Posbásica',

    'Estudios técnicos o comerciales con preparatoria terminada_1': 'Posbásica',
    'Estudios técnicos o comerciales con preparatoria terminada_2': 'Posbásica',
    'Estudios técnicos o comerciales con preparatoria terminada_3': 'Posbásica',
    'Estudios técnicos o comerciales con preparatoria terminada_4': 'Posbásica',
    'Estudios técnicos o comerciales con preparatoria terminada_nan': 'Posbásica',

    'Normal con primaria o secundaria terminada_1': 'Posbásica',
    'Normal con primaria o secundaria terminada_2': 'Posbásica',
    'Normal con primaria o secundaria terminada_3': 'Posbásica',
    'Normal con primaria o secundaria terminada_4': 'Posbásica',
    'Normal con primaria o secundaria terminada_nan': 'Posbásica',

    'Normal de licenciatura_1': 'Posbásica',
    'Normal de licenciatura_2': 'Posbásica',
    'Normal de licenciatura_3': 'Posbásica',
    'Normal de licenciatura_4': 'Posbásica',
    'Normal de licenciatura_5': 'Posbásica',
    'Normal de licenciatura_6': 'Posbásica',
    'Normal de licenciatura_nan': 'Posbásica',

    'Licenciatura_1': 'Posbásica',
    'Licenciatura_2': 'Posbásica',
    'Licenciatura_3': 'Posbásica',
    'Licenciatura_4': 'Posbásica',
    'Licenciatura_5': 'Posbásica',
    'Licenciatura_6': 'Posbásica',
    'Licenciatura_7': 'Posbásica',
    'Licenciatura_8': 'Posbásica',
    'Licenciatura_nan': 'Posbásica',

    'Especialidad_1': 'Posbásica',
    'Especialidad_2': 'Posbásica',
    'Especialidad_nan': 'Posbásica',

    'Maestría_1': 'Posbásica',
    'Maestría_2': 'Posbásica',
    'Maestría_3': 'Posbásica',
    'Maestría_4': 'Posbásica',
    'Maestría_5': 'Posbásica',
    'Maestría_6': 'Posbásica',
    'Maestría_nan': 'Posbásica',

    'Doctorado_1': 'Posbásica',
    'Doctorado_2': 'Posbásica',
    'Doctorado_3': 'Posbásica',
    'Doctorado_4': 'Posbásica',
    'Doctorado_5': 'Posbásica',
    'Doctorado_6': 'Posbásica',
    'Doctorado_nan': 'Posbásica',

    # 'No especificado': 'No especificado',
    BPP: BPP
}

nivacad_posmap_fine = {
    'Ninguno_0': 'Sin Educación',
    'Preescolar_1': 'Sin Educación',
    'Preescolar_2': 'Sin Educación',
    'Preescolar_3': 'Sin Educación',
    'Preescolar_nan': 'Sin Educación',

    'Primaria_1': 'Básica',
    'Primaria_2': 'Básica',
    'Primaria_3': 'Básica',
    'Primaria_4': 'Básica',
    'Primaria_5': 'Básica',
    'Primaria_6': 'Básica',
    'Primaria_nan': 'Básica',

    'Estudios técnicos o comerciales con primaria terminada_1': 'Básica',
    'Estudios técnicos o comerciales con primaria terminada_2': 'Básica',
    'Estudios técnicos o comerciales con primaria terminada_3': 'Básica',
    'Estudios técnicos o comerciales con primaria terminada_4': 'Básica',
    'Estudios técnicos o comerciales con primaria terminada_nan': 'Básica',

    'Secundaria_1': 'Básica',
    'Secundaria_2': 'Básica',
    'Secundaria_3': 'Básica',
    'Secundaria_nan': 'Básica',

    'Preparatoria o bachillerato general_1': 'MediaSup',
    'Preparatoria o bachillerato general_2': 'MediaSup',
    'Preparatoria o bachillerato general_3': 'MediaSup',
    'Preparatoria o bachillerato general_4': 'MediaSup',
    'Preparatoria o bachillerato general_nan': 'MediaSup',

    'Bachillerato tecnológico_1': 'MediaSup',
    'Bachillerato tecnológico_2': 'MediaSup',
    'Bachillerato tecnológico_3': 'MediaSup',
    'Bachillerato tecnológico_4': 'MediaSup',
    'Bachillerato tecnológico_nan': 'MediaSup',

    'Estudios técnicos o comerciales con secundaria terminada_1': 'MediaSup',
    'Estudios técnicos o comerciales con secundaria terminada_2': 'MediaSup',
    'Estudios técnicos o comerciales con secundaria terminada_3': 'MediaSup',
    'Estudios técnicos o comerciales con secundaria terminada_4': 'MediaSup',
    'Estudios técnicos o comerciales con secundaria terminada_5': 'MediaSup',
    'Estudios técnicos o comerciales con secundaria terminada_nan': 'MediaSup',

    'Estudios técnicos o comerciales con preparatoria terminada_1': 'Superior',
    'Estudios técnicos o comerciales con preparatoria terminada_2': 'Superior',
    'Estudios técnicos o comerciales con preparatoria terminada_3': 'Superior',
    'Estudios técnicos o comerciales con preparatoria terminada_4': 'Superior',
    'Estudios técnicos o comerciales con preparatoria terminada_nan': 'Superior',

    'Normal con primaria o secundaria terminada_1': 'MediaSup',
    'Normal con primaria o secundaria terminada_2': 'MediaSup',
    'Normal con primaria o secundaria terminada_3': 'MediaSup',
    'Normal con primaria o secundaria terminada_4': 'MediaSup',
    'Normal con primaria o secundaria terminada_nan': 'MediaSup',

    'Normal de licenciatura_1': 'Superior',
    'Normal de licenciatura_2': 'Superior',
    'Normal de licenciatura_3': 'Superior',
    'Normal de licenciatura_4': 'Superior',
    'Normal de licenciatura_5': 'Superior',
    'Normal de licenciatura_6': 'Superior',
    'Normal de licenciatura_nan': 'Superior',

    'Licenciatura_1': 'Superior',
    'Licenciatura_2': 'Superior',
    'Licenciatura_3': 'Superior',
    'Licenciatura_4': 'Superior',
    'Licenciatura_5': 'Superior',
    'Licenciatura_6': 'Superior',
    'Licenciatura_7': 'Superior',
    'Licenciatura_8': 'Superior',
    'Licenciatura_nan': 'Superior',

    'Especialidad_1': 'Superior',
    'Especialidad_2': 'Superior',
    'Especialidad_nan': 'Superior',

    'Maestría_1': 'Superior',
    'Maestría_2': 'Superior',
    'Maestría_3': 'Superior',
    'Maestría_4': 'Superior',
    'Maestría_5': 'Superior',
    'Maestría_6': 'Superior',
    'Maestría_nan': 'Superior',

    'Doctorado_1': 'Superior',
    'Doctorado_2': 'Superior',
    'Doctorado_3': 'Superior',
    'Doctorado_4': 'Superior',
    'Doctorado_5': 'Superior',
    'Doctorado_6': 'Superior',
    'Doctorado_nan': 'Superior',

    # 'No especificado': 'No especificado',
    BPP: BPP
}


def process_people_df(file_path):

    personas = pd.read_csv(file_path)

    # Household type is always Particular to use same categories as census
    personas_cat = personas[['ID_PERSONA', 'ID_VIV', 'FACTOR']].copy()

    personas_cat['MUN'] = personas.MUN.map(defs['muns']).astype(cats['muns'])

    personas_cat['CLAVIVP'] = personas.CLAVIVP.map(
        defs['clavivp']
    ).astype(cats['clavivp'])

    personas_cat['NUMPER'] = personas.NUMPER

    personas_cat['SEXO'] = personas.SEXO.map(defs['sexo']).astype(cats['sexo'])

    personas_cat['EDAD'] = personas.EDAD.replace(999, np.nan)

    personas_cat['PARENTESCO'] = personas.PARENTESCO.map(
        defs['parentesco']
    ).astype(cats['parentesco'])

    personas_cat['IDENT_MADRE'] = personas.IDENT_MADRE.replace(
        {
            96: 'Otra vivienda',
            97: 'Falleció',
            98: np.nan,
            99: np.nan
        }
    )

    personas_cat['IDENT_PADRE'] = personas.IDENT_PADRE.replace(
        {
            96: 'Otra vivienda',
            97: 'Falleció',
            98: np.nan,
            99: np.nan
        }
    )

    personas_cat['ENT_PAIS_NAC'] = personas.ENT_PAIS_NAC.apply(
        code_ent
    ).astype(cats['ent'])

    personas_cat['NACIONALIDAD'] = personas.NACIONALIDAD.map(
        defs['sino_139']
    ).astype(cats['sino_139'])

    personas_cat['SERSALUD'] = personas.SERSALUD.map(
        defs['sersalud']
    ).astype(cats['sersalud'])

    personas_cat['AFRODES'] = personas.AFRODES.map(
        defs['sino_139']
    ).astype(cats['sino_139'])

    personas_cat['REGIS_NAC'] = personas.REGIS_NAC.map(
        {
            1: 'México',
            2: 'Otro país',
            3: 'No tiene'
        }
    ).astype('category')

    personas_cat['DHSERSAL1'] = personas.DHSERSAL1.map(
        {
            1: 'IMSS',
            2: 'ISSSTE',
            3: 'ISSSTE_E',
            4: 'P_D_M',
            5: 'Popular_NGenración_SBienestar',
            6: 'IMSS_Prospera/Bienestar',
            7: 'Privado',
            8: 'Otro',
            9: 'No afiliado'
        }
    )

    personas_cat['DHSERSAL2'] = personas.DHSERSAL2.fillna(BPP).map(
        {
            2: 'ISSSTE',
            3: 'ISSSTE_E',
            4: 'P_D_M',
            5: 'Popular_NGenración_SBienestar',
            6: 'IMSS_Prospera/Bienestar',
            7: 'Privado',
            8: 'Otro',
            BPP: BPP
        }
    )

    personas_cat['RELIGION'] = personas.RELIGION.apply(
        code_religion
    ).astype('category')

    personas_cat['DIS_VER'] = personas.DIS_VER.map(
        defs['dis']).astype('category')
    personas_cat['DIS_OIR'] = personas.DIS_OIR.map(
        defs['dis']).astype('category')
    personas_cat['DIS_CAMINAR'] = personas.DIS_CAMINAR.map(
        defs['dis']).astype('category')
    personas_cat['DIS_RECORDAR'] = personas.DIS_RECORDAR.map(
        defs['dis']).astype('category')
    personas_cat['DIS_BANARSE'] = personas.DIS_BANARSE.map(
        defs['dis']).astype('category')
    personas_cat['DIS_HABLAR'] = personas.DIS_HABLAR.map(
        defs['dis']).astype('category')
    personas_cat['DIS_MENTAL'] = personas.DIS_MENTAL.map(
        defs['dis_mental']).astype('category')
    personas_cat['DIS'] = (
        personas.DIS_VER.astype(str)
        + personas.DIS_OIR.astype(str)
        + personas.DIS_CAMINAR.astype(str)
        + personas.DIS_RECORDAR.astype(str)
        + personas.DIS_BANARSE.astype(str)
        + personas.DIS_HABLAR.astype(str)
        + personas.DIS_MENTAL.astype(str)
    ).astype(cats['dis'])

    personas_cat['HLENGUA'] = personas['HLENGUA'].fillna(BPP).map(
        {
            1: SI,
            3: NO,
            BPP: BPP
        }
    ).astype('category')
    personas_cat['HESPANOL'] = personas['HESPANOL'].fillna(BPP).map(
        {
            1: SI,
            3: NO,
            BPP: BPP
        }
    ).astype('category')

    personas_cat['ELENGUA'] = personas.ELENGUA.fillna(BPP).map(
        {
            5: SI,
            7: NO,
            BPP: BPP
        }
    ).astype('category')

    personas_cat['PERTE_INDIGENA'] = personas.PERTE_INDIGENA.fillna(
        BPP
    ).map(
        {
            1: SI,
            3: NO,
            BPP: BPP
        }
    ).astype('category')

    personas_cat['ASISTEN'] = personas.ASISTEN.fillna(BPP).map(
        {
            1: SI,
            3: NO,
            BPP: BPP
        }
    ).astype('category')

    personas_cat['ENT_PAIS_ASI'] = personas.ENT_PAIS_ASI.apply(
        code_ent).astype(cats['ent'])
    personas_cat['MUN_ASI'] = pd.concat(
        [
            personas[['MUN_ASI']],
            personas_cat[['ENT_PAIS_ASI']]
        ],
        axis=1).apply(code_MUN_ASI, axis=1).astype('category')

    personas_cat['TIE_TRASLADO_ESCU'] = personas.TIE_TRASLADO_ESCU.fillna(
        BPP).map(
            defs['tie_traslado']).astype('category')

    med_traslado_esc1_dummies = pd.get_dummies(
        personas.MED_TRASLADO_ESC1.fillna(BPP).map(
            defs['med_traslado']), prefix='MED_TRASLADO_ESC')
    med_traslado_esc2_dummies = pd.get_dummies(
        personas.MED_TRASLADO_ESC2.fillna(BPP).map(
            defs['med_traslado']), prefix='MED_TRASLADO_ESC')
    med_traslado_esc3_dummies = pd.get_dummies(
        personas.MED_TRASLADO_ESC3.fillna(BPP).map(
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

    personas_cat['NIVACAD'] = personas['NIVACAD'].fillna(BPP).map(
        {
            0: 'Ninguno',
            1: 'Preescolar',
            2: 'Primaria',
            3: 'Secundaria',
            4: 'Preparatoria o bachillerato general',
            5: 'Bachillerato tecnológico',
            6: 'Estudios técnicos o comerciales con primaria terminada',
            7: 'Estudios técnicos o comerciales con secundaria terminada',
            8: 'Estudios técnicos o comerciales con preparatoria terminada',
            9: 'Normal con primaria o secundaria terminada',
            10: 'Normal de licenciatura',
            11: 'Licenciatura',
            12: 'Especialidad',
            13: 'Maestría',
            14: 'Doctorado',
            BPP: BPP,
        }
    ).astype('category')
    personas_cat['ESCOLARI'] = personas.ESCOLARI.fillna(
        BPP).astype(
            pd.CategoricalDtype(
                [0, 1, 2, 3, 4, 5, 6, 7, 8, BPP])
        )

    personas_cat['NOMCAR_C'] = personas.NOMCAR_C.fillna(BPP).replace(9999, np.nan)

    personas_cat['ALFABET'] = personas.ALFABET.fillna(BPP).map(
        {
            1: SI,
            3: NO,
            BPP: BPP
        }
    ).astype('category')

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
    ).astype('category')

    personas_cat['SITUA_CONYUGAL'] = personas.SITUA_CONYUGAL.fillna(
        BPP).map(
            {
                1: 'unión libre',
                2: 'separada(o)',
                3: 'divorciada(o)',
                4: 'viuda(o)',
                5: 'casada(o) sólo por el civil',
                6: 'casada(o) sólo religiosamente',
                7: 'casada(o) civil y religiosamente',
                8: 'soltera(o)',
                # 9: 'No especificado',
                BPP: BPP,
            }
        ).astype('category')

    personas_cat['IDENT_PAREJA'] = personas.IDENT_PAREJA.fillna(BPP).replace(
        {
            96: NO,
            99: np.nan
        }
    )

    personas_cat['CONACT'] = personas.CONACT.fillna(BPP).map(
        {
            10: 'Trabajó',
            13: 'Declara que busca trabajo /  se rescata que trabaja',
            14: 'Declara jubilado o pensionado / se rescata que trabaja',
            15: 'Declara estudiante / se rescata que trabaja',
            16: 'Se dedica a los quehaceres del hogar / se rescata que trabaja',
            17: 'Declara que tiene limitaciónes / se rescata que trabaja',
            18: 'Declara otra situación de actividad / se rescata que trabaja',
            19: 'No se tiene información / se rescata que trabaja',
            20: 'Tenía trabajo pero no trabajó',
            30: 'Buscó trabajo',
            40: 'Es pensionada(o) o jubilada(o)',
            50: 'Es estudiante',
            60: 'Se dedica a los quehaceres del hogar',
            70: 'Está incapacitado permanentemente para trabajar',
            80: 'No trabaja',
            # 99: 'No especificado',
            BPP: BPP,
        }
    ).astype('category')

    personas_cat['OCUPACION_C'] = np.floor(personas.OCUPACION_C/10).fillna(
        BPP).map(
            {
                11: 'Funcionarios y altas autoridades de los sectores público,'
                ' privado y social',
                12: 'Directores y gerentes en servicios financieros, legales,'
                ' administrativos y sociales',
                13: 'Directores y gerentes en producción, tecnología y transporte',
                14: 'Directores y gerentes de ventas, restaurantes, hoteles y'
                ' otros establecimientos',
                15: 'Coordinadores y jefes de área en servicios financieros,'
                ' administrativos y sociales',
                16: 'Coordinadores y jefes de área en producción y tecnología',
                17: 'Coordinadores y jefes de área de ventas, restaurantes, hoteles'
                ' y otros establecimientos',
                19: 'Otros directores, funcionarios, gerentes, coordinadores y'
                ' jefes de área, no clasificados anteriormente',
                21: 'Profesionistas en ciencias económico-administrativas,'
                ' ciencias sociales, humanistas y en artes',
                22: 'Investigadores y profesionistas en ciencias exactas,'
                ' biológicas, ingeniería, informática y en telecomunicaciones',
                23: 'Profesores y especialistas en docencia',
                24: 'Médicos, enfermeras y otros especialistas en salud',
                25: 'Auxiliares y técnicos en ciencias económico-administrativas,'
                ' ciencias sociales, humanistas y en artes',
                26: 'Auxiliares y técnicos en ciencias exactas, biológicas,'
                ' ingeniería, informática y en telecomunicaciones',
                27: 'Auxiliares y técnicos en educación, instructores y capacitadores',
                28: 'Enfermeras, técnicos en medicina y trabajadores de apoyo'
                ' en salud',
                29: 'Otros profesionistas y técnicos no clasificados anteriormente',
                31: 'Supervisores de personal de apoyo administrativo, secretarias,'
                ' capturistas, cajeros y trabajadores de control de archivo'
                ' y transporte',
                32: 'Supervisores y trabajadores que brindan y manejan información',
                39: 'Otros trabajadores auxiliares en actividades administrativas,'
                ' no clasificados anteriormente',
                41: 'Comerciantes en establecimientos',
                42: 'Empleados de ventas en establecimientos',
                43: 'Trabajadores en servicios de alquiler',
                49: 'Otros comerciantes, empleados en ventas y agentes de ventas'
                ' en establecimientos, no clasificados anteriormente',
                51: 'Trabajadores en la preparación y servicio de alimentos y'
                ' bebidas, así como en servicios de esparcimiento y de hotelería',
                52: 'Trabajadores en cuidados personales y del hogar',
                53: 'Trabajadores en servicios de protección y vigilancia',
                54: 'Trabajadores de la Armada, Ejército y Fuerza Aérea',
                61: 'Trabajadores en actividades agrícolas y ganaderas',
                62: 'Trabajadores en actividades pesqueras, forestales, caza y'
                ' similares',
                63: 'Operadores de maquinaria agropecuaria y forestal',
                69: 'Otros trabajadores en actividades agrícolas, ganaderas,'
                ' forestales, caza y pesca, no clasificados anteriormente',
                71: 'Trabajadores en la extracción y la edificación de construcciones',
                72: 'Artesanos y trabajadores en el tratamiento y elaboración de'
                ' productos de metal',
                73: 'Artesanos y trabajadores en la elaboración de productos de'
                ' madera, papel, textiles y de cuero y piel',
                74: 'Artesanos y trabajadores en la elaboración de productos de'
                ' hule, caucho, plásticos y de sustancias químicas',
                75: 'Trabajadores en la elaboración y procesamiento de alimentos,'
                ' bebidas y productos de tabaco',
                76: 'Artesanos y trabajadores en la elaboración de productos de'
                ' cerámica, vidrio, azulejo y similares',
                79: 'Otros trabajadores artesanales no clasificados anteriormente',
                81: 'Operadores de instalaciones y maquinaria industrial',
                82: 'Ensambladores y montadores de herramientas, maquinaria,'
                ' productos metálicos y electrónicos',
                83: 'Conductores de transporte y de maquinaria móvil',
                89: 'Otros operadores de maquinaria industrial, ensambladores y'
                ' conductores de transporte, no clasificados anteriormente',
                91: 'Trabajadores de apoyo en actividades agropecuarias, forestales,'
                ' pesca y caza',
                92: 'Trabajadores de apoyo en la minería, construcción e industria',
                93: 'Ayudantes de conductores de transporte, conductores de'
                ' transporte de tracción humana y animal y cargadores',
                94: 'Ayudantes en la preparación de alimentos',
                95: 'Vendedores ambulantes',
                96: 'Trabajadores domésticos, de limpieza, planchadores y otros'
                ' trabajadores de limpieza',
                97: 'Trabajadores de paquetería, de apoyo para espectáculos,'
                ' mensajeros y repartidores de mercancías',
                98: 'Otros trabajadores en actividades elementales y de apoyo,'
                ' no clasificados anteriormente',
                # 99: 'Ocupaciones no especificadas ',
                BPP: BPP
            }
        ).astype('category')

    personas_cat['SITTRA'] = personas.SITTRA.fillna(BPP).map(
        {
            1: 'empleada(o) u obrera(o)',
            2: 'jornalera(o) o peón(a)',
            3: 'ayudante con pago',
            4: 'patrón(a) o empleador(a)',
            5: 'trabajador(a) por cuenta propia',
            6: 'trabajador(a) sin pago',
            # 9: 'No especificado',
            BPP: BPP,
        }
    ).astype('category')

    personas_cat['AGUINALDO'] = personas.AGUINALDO.fillna(BPP).map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['VACACIONES'] = personas.VACACIONES.fillna(BPP).map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['SERVICIO_MEDICO'] = personas.SERVICIO_MEDICO.fillna(BPP).map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['UTILIDADES'] = personas.UTILIDADES.fillna(BPP).map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['INCAP_SUELDO'] = personas.INCAP_SUELDO.fillna(BPP).map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['SAR_AFORE'] = personas.SAR_AFORE.fillna(BPP).map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['CREDITO_VIVIENDA'] = personas.CREDITO_VIVIENDA.fillna(BPP).map(
            defs['prestaciones']).astype(cats['prestaciones'])

    personas_cat['INGTRMEN'] = personas.INGTRMEN.fillna(BPP).replace(
        999999, np.nan)

    personas_cat['HORTRA'] = personas.HORTRA.fillna(BPP).replace(
        999, np.nan)

    personas_cat['ACTIVIDADES_C'] = np.floor(
        personas.ACTIVIDADES_C/100).fillna(
            BPP).map(
                defs['actividades']).astype('category')

    personas_cat['ENT_PAIS_TRAB'] = personas.ENT_PAIS_TRAB.apply(
        code_ent).astype('category')

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
        axis=1).astype('category')

    personas_cat['TIE_TRASLADO_TRAB'] = personas.TIE_TRASLADO_TRAB.fillna(
        BPP).map(
            defs['tie_traslado_trab']).astype('category')

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

    return personas_cat


def categorize_p(personas):
    personas_cat = personas.copy()

    personas_cat['EDAD'] = pd.cut(
        personas.EDAD,
        (0, 3, 5, 6, 8, 12, 15, 18, 25, 50, 60, 65, 131),
        right=False,
        labels=cats['edad']
    )

    dhsersal_or_cats = [
        'DHSERSAL_IMSS',
        'DHSERSAL_ISSSTE',
        'DHSERSAL_ISSSTE_E',
        'DHSERSAL_P_D_M',
        'DHSERSAL_Popular_NGenración_SBienestar',
        'DHSERSAL_IMSS_Prospera/Bienestar',
        'DHSERSAL_Privado',
        'DHSERSAL_Otro',
        'DHSERSAL_No afiliado'
    ]
    dhsersal1_dummies = pd.get_dummies(personas.DHSERSAL1, prefix='DHSERSAL')
    dhsersal2_dummies = pd.get_dummies(
        personas.DHSERSAL2.replace(BPP, np.nan), prefix='DHSERSAL')
    dhsersal_df = dhsersal1_dummies.add(
        dhsersal2_dummies, fill_value=0
    )[dhsersal_or_cats].astype(int)
    dhsersal_df['DHSERSAL_PUB'] = (
        dhsersal_df[dhsersal_or_cats[:6]].T.sum() > 0).astype(int)
    dhsersal_df['DHSERSAL_AFIL'] = (
        dhsersal_df[dhsersal_or_cats[:8]].T.sum() > 0).astype(int)
    dhsersal_df = dhsersal_df.astype('category')

    personas_cat = pd.concat([personas_cat, dhsersal_df], axis=1)
    # dhsersal_or_cats = [
    #     'IMSS', 'ISSSTE', 'ISSSTE_E', 'P_D_M', 'Popular_NGenración_SBienestar',
    #     'IMSS_Prospera/Bienestar', 'Privado', 'Otro', 'No afiliado'
    # ]
    # dhsersal1_dummies = pd.get_dummies(personas.DHSERSAL1)
    # dhsersal2_dummies = pd.get_dummies(personas.DHSERSAL2)
    # dhsersar_df = dhsersal1_dummies.add(
    #                 dhsersal2_dummies, fill_value=0
    #             )[dhsersal_or_cats].astype(int).astype(str)
    # dhsersal_series = dhsersar_df[dhsersal_or_cats[0]]
    # for c in dhsersal_or_cats[1:]:
    #     dhsersal_series += dhsersar_df[c]
    # personas_cat['DHSERSAL'] = dhsersal_series.replace(
    #     '000000000', np.nan).astype('category')

    # personas_cat['DHSERSAL_pub'] = [
    #     1
    #     if (
    #             (not np.isnan(float(v))) and ('1' in v[:6])
    #     ) else 0
    #     for v in personas_cat.DHSERSAL.values
    # ]
    # personas_cat['DHSERSAL_priv'] = [
    #     1
    #     if (
    #             (not np.isnan(float(v))) and ('1' in v[6])
    #     ) else 0
    #     for v in personas_cat.DHSERSAL.values
    # ]
    # personas_cat['DHSERSAL_otro'] = [
    #     1
    #     if (
    #             (not np.isnan(float(v))) and ('1' in v[7])
    #     ) else 0
    #     for v in personas_cat.DHSERSAL.values
    # ]
    # personas_cat['DHSERSAL_no'] = [
    #     1
    #     if (
    #             (not np.isnan(float(v))) and ('1' in v[8])
    #     ) else 0
    #     for v in personas_cat.DHSERSAL.values
    # ]

    personas_cat['EDUC'] = (
        personas.NIVACAD.astype(str)
        + '_'
        + personas.ESCOLARI.astype(str)
    ).replace(
        {
            'nan_nan': np.nan,
            'Blanco por pase_Blanco por pase':
            'Blanco por pase'
        }
    ).map(nivacad_posmap).astype('category')

    personas_cat['SITUA_CONYUGAL'] = personas.SITUA_CONYUGAL.map(
            {
                'unión libre': 'casado',
                'separada(o)': 'separado',
                'divorciada(o)': 'separado',
                'viuda(o)': 'separado',
                'casada(o) sólo por el civil': 'casado',
                'casada(o) sólo religiosamente': 'casado',
                'casada(o) civil y religiosamente': 'casado',
                'soltera(o)': 'soltero',
                # 9: 'No especificado',
                BPP: BPP,
            }
        ).astype('category')

    personas_cat['CONACT'] = personas.CONACT.map(
        {
            'Trabajó': 'Trabaja',
            'Declara que busca trabajo /  se rescata que trabaja': 'Trabaja',
            'Declara jubilado o pensionado / se rescata que trabaja': 'Trabaja',
            'Declara estudiante / se rescata que trabaja': 'Trabaja',
            'Se dedica a los quehaceres del hogar / se rescata que trabaja': 'Trabaja',
            'Declara que tiene limitaciónes / se rescata que trabaja': 'Trabaja',
            'Declara otra situación de actividad / se rescata que trabaja': 'Trabaja',
            'No se tiene información / se rescata que trabaja': 'Trabaja',
            'Tenía trabajo pero no trabajó': 'Trabaja',
            'Buscó trabajo': 'No trabaja',
            'Es pensionada(o) o jubilada(o)': 'No trabaja',
            'Es estudiante': 'No trabaja',
            'Se dedica a los quehaceres del hogar': 'No trabaja',
            'Está incapacitado permanentemente para trabajar': 'No trabaja',
            'No trabaja': 'No trabaja',
            BPP: BPP,
        }
    ).astype('category')

    personas_cat['INGTRMEN'] = pd.cut(
        personas.INGTRMEN.replace(BPP, 2e6),
        (0, 1000, 5000, 10000, 20000, 40000, 80000, 150000, 999999, 1e6, 3e6),
        right=False,
        labels=[
            '0-999', '1,000-4,999', '5,000-9,999', '10,000-19,999',
            '20,000-39,999', '40,000-79,999', '80,000-149,999',
            '150,000yMas', 'No especificado', BPP
        ]
    ).replace('No especificado', np.nan)

    personas_cat['HORTRA'] = pd.cut(
        personas.HORTRA.replace(BPP, 2e6),
        [-1, 5, 10, 20, 40, 48, 56, 60, 80, 998, 1e6, 3e6],
        right=True,
        labels=[
            '0-5', '6-10', '11-20', '21-40', '41-48', '49-56',
            '57-60', '61-80', '81YMAS', 'No especificado', BPP
        ]
    ).replace('No especificado', np.nan)

    # personas_cat['DIS_VER'] = personas.DIS_VER.replace(
    #         'Se desconoce el grado de la discapacidad', np.nan)
    # personas_cat['DIS_OIR'] = personas.DIS_OIR.replace(
    #         'Se desconoce el grado de la discapacidad', np.nan)
    # personas_cat['DIS_CAMINAR'] = personas.DIS_CAMINAR.replace(
    #         'Se desconoce el grado de la discapacidad', np.nan)
    # personas_cat['DIS_RECORDAR'] = personas.DIS_RECORDAR.replace(
    #         'Se desconoce el grado de la discapacidad', np.nan)
    # personas_cat['DIS_BANARSE'] = personas.DIS_BANARSE.replace(
    #         'Se desconoce el grado de la discapacidad', np.nan)
    # personas_cat['DIS_HABLAR'] = personas.DIS_HABLAR.replace(
    #         'Se desconoce el grado de la discapacidad', np.nan)

    # personas_cat['DIS_CON'] = [
    #     'Sí' if ('3' in c) or ('4' in c) else 'No'
    #     for c in personas.DIS
    # ]
    # personas_cat['DIS_CON'] = personas_cat['DIS_CON'].astype('category')

    # personas_cat['DIS_LIMI'] = [
    #     'Sí' if '2' in c else 'No'
    #     for c in personas.DIS
    # ]
    # personas_cat['DIS_LIMI'] = personas_cat['DIS_LIMI'].astype('category')

    return personas_cat


def process_places_df(file_path):

    viviendas = pd.read_csv(file_path)

    viviendas_cat = viviendas[['ID_VIV', 'FACTOR']].copy()

    viviendas_cat['MUN'] = viviendas.MUN.map(defs['muns']).astype(cats['muns'])

    viviendas_cat['CLAVIVP'] = viviendas.CLAVIVP.map(
        defs['clavivp']
    ).astype('category')

    viviendas_cat['PAREDES'] = viviendas.PAREDES.fillna(
        'Blanco por pase').map(defs['paredes']).astype(cats['paredes'])

    viviendas_cat['TECHOS'] = viviendas.TECHOS.fillna(
        'Blanco por pase').map(defs['techos']).astype(cats['techos'])

    viviendas_cat['PISOS'] = viviendas.PISOS.fillna(
        BPP).map(
            {
                1: 'Tierra',
                2: 'Cemento o firme',
                3: 'Madera, mosaico u otro recubrimiento',
                # 9: 'No especificado',
                BPP: BPP
            }
        ).astype('category')

    viviendas_cat['COCINA'] = viviendas.COCINA.fillna(
        'Blanco por pase').map(defs['cocina']).astype(cats['cocina'])

    viviendas_cat['CUADORM'] = viviendas.CUADORM.fillna(
        BPP).replace(99, np.nan).astype('category')

    viviendas_cat['TOTCUART'] = viviendas.TOTCUART.fillna(BPP).replace(
        99, np.nan).astype('category')

    viviendas_cat['LUG_COC'] = viviendas.LUG_COC.fillna(
        'Blanco por pase').map(defs['lug_coc']).astype(cats['lug_coc'])

    viviendas_cat['COMBUSTIBLE'] = viviendas.COMBUSTIBLE.fillna(
        'Blanco por pase').map(defs['combustible']).astype(cats['combustible'])

    viviendas_cat['ESTUFA'] = viviendas.ESTUFA.fillna(
        'Blanco por pase').map(defs['estufa']).astype(cats['estufa'])

    viviendas_cat['ELECTRICIDAD'] = viviendas.ELECTRICIDAD.fillna(
        BPP).map(
            {
                1: SI,
                3: NO,
                BPP: BPP
            }
        ).astype('category')

    viviendas_cat['FOCOS'] = viviendas.FOCOS.fillna(
        'Blanco por pase').map(
            defs['focos']).astype(cats['focos'])

    viviendas_cat['FOCOS_AHORRA'] = viviendas.FOCOS_AHORRA.fillna(
        'Blanco por pase').map(
            defs['focos_ahorra']).astype(cats['focos_ahorra'])

    viviendas_cat['AGUA_ENTUBADA'] = viviendas.AGUA_ENTUBADA.fillna(
        BPP).map(
            {
                1: 'Dentro de la vivienda',
                2: 'Sólo en el patio o terreno',
                3: 'No tiene',
                BPP: BPP
            }
        ).astype('category')

    viviendas_cat['ABA_AGUA_ENTU'] = viviendas.ABA_AGUA_ENTU.fillna(BPP).map(
            {
                1: 'Del servicio público de agua.',
                2: 'De un pozo comunitario.',
                3: 'De un pozo particular.',
                4: 'De una pipa.',
                5: 'De otra vivienda.',
                6: 'De la lluvia.',
                7: 'De otro lugar.',
                BPP: BPP
            }
    ).astype('category')

    viviendas_cat['ABA_AGUA_NO_ENTU'] = viviendas.ABA_AGUA_NO_ENTU.fillna(
        'Blanco por pase').map(
            defs['aba_agua_no_entu']).astype(cats['aba_agua_no_entu'])

    viviendas_cat['TINACO'] = viviendas.TINACO.fillna(
        BPP).map(
            defs['tinaco']).astype(cats['tinaco'])

    viviendas_cat['CISTERNA'] = viviendas.CISTERNA.fillna(
        BPP).map(
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
        BPP).map(defs['sersan']).astype('category')

    viviendas_cat['CONAGUA'] = viviendas.CONAGUA.fillna(
        BPP).map(
            {
                1: 'Tiene descarga directa de agua.',
                2: 'Le echan agua con cubeta.',
                3: 'No se le puede echar agua.',
                BPP: BPP
            }
        ).astype('category')

    viviendas_cat['USOEXC'] = viviendas.USOEXC.fillna(
        'Blanco por pase').map(
            defs['usoexc']).astype(cats['usoexc'])

    viviendas_cat['DRENAJE'] = viviendas.DRENAJE.fillna(
        BPP).map(
            {
                1: 'La red pública.',
                2: 'Una fosa séptica o tanque séptico (biodigestor).',
                3: 'Una tubería que va a dar a una barranca o grieta.',
                4: 'Una tubería que va a dar a un río, lago o mar.',
                5: 'No tiene drenaje.',
                BPP: BPP
            }
    ).astype('category')

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
        BPP).map(
            defs['refrigerador']).astype(cats['refrigerador'])

    viviendas_cat['LAVADORA'] = viviendas.LAVADORA.fillna(
        BPP).map(
            defs['lavadora']).astype(cats['lavadora'])

    viviendas_cat['HORNO'] = viviendas.HORNO.fillna(
        BPP).map(
            defs['horno']).astype(cats['horno'])

    viviendas_cat['AUTOPROP'] = viviendas.AUTOPROP.fillna(
        BPP).map(
            defs['autoprop']).astype(cats['autoprop'])

    viviendas_cat['MOTOCICLETA'] = viviendas.MOTOCICLETA.fillna(
        BPP).map(
            defs['motocicleta']).astype(cats['motocicleta'])

    viviendas_cat['BICICLETA'] = viviendas.BICICLETA.fillna(
        BPP).map(
            defs['bicicleta']).astype(cats['bicicleta'])

    viviendas_cat['RADIO'] = viviendas.RADIO.fillna(
        BPP).map(
            defs['radio']).astype(cats['radio'])

    viviendas_cat['TELEVISOR'] = viviendas.TELEVISOR.fillna(
        BPP).map(
            defs['televisor']).astype(cats['televisor'])

    viviendas_cat['COMPUTADORA'] = viviendas.COMPUTADORA.fillna(
        BPP).map(
            defs['computadora']).astype(cats['computadora'])

    viviendas_cat['TELEFONO'] = viviendas.TELEFONO.fillna(
        BPP).map(
            defs['telefono']).astype(cats['telefono'])

    viviendas_cat['CELULAR'] = viviendas.CELULAR.fillna(
        BPP).map(
            defs['celular']).astype(cats['celular'])

    viviendas_cat['INTERNET'] = viviendas.INTERNET.fillna(
        BPP).map(
            defs['internet']).astype(cats['internet'])

    viviendas_cat['SERV_TV_PAGA'] = viviendas.SERV_TV_PAGA.fillna(
        BPP).map(
            defs['serv_tv_paga']).astype(cats['serv_tv_paga'])

    viviendas_cat['SERV_PEL_PAGA'] = viviendas.SERV_PEL_PAGA.fillna(
        BPP).map(
            defs['serv_pel_paga']).astype(cats['serv_pel_paga'])

    viviendas_cat['CON_VJUEGOS'] = viviendas.CON_VJUEGOS.fillna(
        BPP).map(
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
        BPP).map(
            defs['tipohog']).astype(cats['tipohog'])

    viviendas_cat['INGTRHOG'] = viviendas.INGTRHOG.fillna(BPP).replace(
        999999, np.nan)

    viviendas_cat['JEFE_SEXO'] = viviendas.JEFE_SEXO.map(
        defs['sexo']).astype(cats['sexo'])

    viviendas_cat['JEFE_EDAD'] = viviendas.JEFE_EDAD.replace(999, np.nan)

    return viviendas_cat


def categorize_v(viviendas):
    viviendas_cat = viviendas.copy()

    # viviendas_cat['PISOS'] = viviendas.PISOS.map(
    #         {
    #             'Tierra': 'Tierra',
    #             'Cemento o firme': 'No tierra',
    #             'Madera, mosaico u otro recubrimiento': 'No tierra',
    #             BPP: BPP
    #         }
    #     ).astype('category')

    viviendas_cat['CUADORM'] = viviendas.CUADORM.map(
        {1: 1} | {i: '2+' for i in range(2, 26)} | {BPP: BPP}
    ).astype('category')

    viviendas_cat['TOTCUART'] = viviendas.TOTCUART.map(
        {1: 1, 2: 2} | {i: '3+' for i in range(3, 26)} | {BPP: BPP}
    ).astype('category')

    # viviendas_cat['AGUA_ENTUBADA'] = viviendas.AGUA_ENTUBADA.map(
    #         {
    #             'Dentro de la vivienda': 'Tiene',
    #             'Sólo en el patio o terreno': 'Tiene',
    #             'No tiene': 'No tiene',
    #             BPP: BPP
    #         }
    # ).astype('category')

    # viviendas_cat['ABA_AGUA_ENTU'] = viviendas.ABA_AGUA_ENTU.map(
    #         {
    #             'Del servicio público de agua.': 'Del servicio público de agua.',
    #             'De un pozo comunitario.': 'De otro lugar.',
    #             'De un pozo particular.': 'De otro lugar.',
    #             'De una pipa.': 'De otro lugar.',
    #             'De otra vivienda.': 'De otro lugar.',
    #             'De la lluvia.': 'De otro lugar.',
    #             'De otro lugar.': 'De otro lugar.',
    #             BPP: BPP
    #         }
    # ).astype('category')

    # viviendas_cat['CONAGUA'] = viviendas.CONAGUA.map(
    #         {
    #             'Tiene descarga directa de agua.': SI,
    #             'Le echan agua con cubeta.': SI,
    #             'No se le puede echar agua.': NO,
    #             BPP: BPP
    #         }
    # ).astype('category')

    # viviendas_cat['DRENAJE'] = viviendas.DRENAJE.map(
    #         {
    #             'La red pública.': SI,
    #             'Una fosa séptica o tanque séptico (biodigestor).': SI,
    #             'Una tubería que va a dar a una barranca o grieta.': SI,
    #             'Una tubería que va a dar a un río, lago o mar.': SI,
    #             'No tiene drenaje.': NO,
    #             BPP: BPP
    #         }
    # ).astype('category')

    viviendas_cat['INGTRHOG'] = pd.cut(
        viviendas.INGTRHOG.replace(BPP, 2e6),
        (0, 1000, 5000, 10000, 20000, 40000, 80000, 150000, 999999, 1e6, 3e6),
        right=False,
        labels=[
            '0-999', '1,000-4,999', '5,000-9,999', '10,000-19,999',
            '20,000-39,999', '40,000-79,999', '80,000-149,999',
            '150,000yMas', 'No especificado', BPP
        ]
    ).replace('No especificado', np.nan)

    viviendas_cat['JEFE_EDAD'] = pd.cut(
        viviendas.JEFE_EDAD,
        (0, 3, 5, 6, 8, 12, 15, 18, 25, 50, 60, 65, 131),
        right=False,
        labels=cats['edad']
    )

    viviendas_cat['CLAVIVP'] = viviendas.CLAVIVP.map(
        {
            'Casa única en el terreno': 'Vivienda',
            'Casa que comparte terreno con otra(s)': 'Vivienda',
            'Casa dúplex': 'Vivienda',
            'Departamento en edificio': 'Vivienda',
            'Vivienda en vecindad o cuartería': 'Vivienda',
            'Vivienda en cuarto de azotea de un edificio': 'Vivienda',
            'Local no construido para habitación': 'Otro',
            'Vivienda móvil': 'Otro',
            'Refugio': 'Otro',
        }
    ).astype('category')

    return viviendas_cat


def has_dis(s):
    for c in s:
        if 1 < int(c) < 6 or int(c) == 8:
            return 1
    if '9' in s:
        return np.nan
    return 0


def get_modo_agr(r):
    if r['MED_TRASLADO_ESC_TPUB'] == 1:
        return 'TPUB'
    elif r['MED_TRASLADO_ESC_Automóvil o camioneta'] == 1:
        return 'Automóvil o camioneta'
    elif r['MED_TRASLADO_ESC_Motocicleta o motoneta'] == 1:
        return 'Motocicleta o motoneta'
    elif r['MED_TRASLADO_ESC_Transporte escolar'] == 1:
        return 'Transporte escolar'
    elif r['MED_TRASLADO_ESC_Taxi (App Internet)'] == 1:
        return 'Taxi (App Internet)'
    elif r['MED_TRASLADO_ESC_Taxi (sitio, calle, otro)'] == 1:
        return 'Taxi (sitio, calle, otro)'
    elif r['MED_TRASLADO_ESC_Bicicleta'] == 1:
        return 'Bicicleta'
    elif r['MED_TRASLADO_ESC_Caminando'] == 1:
        return 'Caminando'
    elif r['MED_TRASLADO_ESC_Otro'] == 1:
        return 'Otro'
    elif r['MED_TRASLADO_ESC_No especificado'] == 1:
        return 'No especificado'
    elif r['MED_TRASLADO_ESC_Blanco por pase'] == 1:
        return 'Blanco por pase'
    else:
        raise NotImplementedError
