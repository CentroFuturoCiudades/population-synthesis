import numpy as np
import pandas as pd
from constraints import constraints_ind
from itertools import product

# Codes for the metropolitan zone of Monterrey
met_area_codes = [1, 6, 9, 10, 12, 18, 19, 21, 25, 26,
                  31, 39, 41, 45, 46, 47, 48, 49]

DIS_CATS = [f'{i}{j}{k}{l}{m}{n}{o}'
            for (i, j, k, l, m, n), o
            in product(product([1, 2, 3, 4, 8, 9], repeat=6), [5, 6, 9])]

DHSERSAL_CATS = sorted(
    ['0000000001', '0000000010']
    + [
        f'{i}{j}{k}{l}{m}{n}{o}{p}00'
        for i, j, k, l, m, n, o, p in product([0, 1], repeat=8)
        if 0 < sum([i, j, k, l, m, n, o, p]) < 3
    ]
)

nivacad_cats = []
nivacad_cats += ['Ninguno']
nivacad_cats += [f'Preescolar_{i}' for i in [1, 2, 3, 99]]
nivacad_cats += [f'Primaria_{i}' for i in [1, 2, 3, 4, 5, 6, 99]]
nivacad_cats += [f'Secundaria_{i}' for i in [1, 2, 3, 99]]
nivacad_cats += [f'Preparatoria o bachillerato general_{i}'
                 for i in [1, 2, 3, 4, 99]]
nivacad_cats += [f'Bachillerato tecnológico_{i}' for i in [1, 2, 3, 4, 99]]
nivacad_cats += [f'Estudios técnicos o comerciales con primaria terminada_{i}'
                 for i in [1, 2, 3, 4, 99]]
nivacad_cats += [
    f'Estudios técnicos o comerciales con secundaria terminada_{i}'
    for i in [1, 2, 3, 4, 5, 99]
]
nivacad_cats += [
    f'Estudios técnicos o comerciales con preparatoria terminada_{i}'
    for i in [1, 2, 3, 4, 99]
]
nivacad_cats += [f'Normal con primaria o secundaria terminada_{i}'
                 for i in [1, 2, 3, 4, 99]]
nivacad_cats += [f'Normal de licenciatura_{i}' for i in [1, 2, 3, 4, 5, 6, 99]]
nivacad_cats += [f'Licenciatura_{i}' for i in [1, 2, 3, 4, 5, 6, 7, 8, 99]]
nivacad_cats += [f'Especialidad_{i}' for i in [1, 2, 99]]
nivacad_cats += [f'Maestría_{i}' for i in [1, 2, 3, 4, 5, 6, 99]]
nivacad_cats += [f'Doctorado_{i}' for i in [1, 2, 3, 4, 5, 6, 99]]
nivacad_cats += ['No especificado']
nivacad_cats += ['Blanco por pase']


def load_mun_defs():
    # Categories for municipalities in Nuevo Leon
    mun_defs = pd.read_csv(
        '../data/cuestionario_ampliado/'
        'Censo2020_clasificaciones_CPV_csv/MUN.csv',
        encoding='ISO-8859-1'
    )
    mun_defs = (
        mun_defs[mun_defs.CVE_ENT == 19][['CVE_MUN', 'NOM_MUN']]
        .set_index('CVE_MUN')
        .drop(999)
        .to_dict()['NOM_MUN']
    )
    return mun_defs


def load_paren_defs():
    parentesco_defs = pd.read_csv(
        '../data/cuestionario_ampliado/'
        'Censo2020_clasificaciones_CPV_csv/PARENTESCO.csv',
        encoding='ISO-8859-1',
        index_col='CLAVE'
    ).to_dict()['DESCRIPCION']
    return parentesco_defs


def load_ocupacion_defs():
    ddefs = pd.read_csv(
        '../data/cuestionario_ampliado/'
        'Censo2020_clasificaciones_CPV_csv/OCUPACION.csv',
        encoding='ISO-8859-1',
        index_col='CLAVE'
    ).to_dict()['DESCRIPCION']

    ddefs[999] = 'No especificado'
    ddefs['Blanco por pase'] = 'Blanco por pase'

    return ddefs


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


defs = {
    'muns': load_mun_defs(),

    'clavivp': {
        1: 'Casa única en el terreno',
        2: 'Casa que comparte terreno con otra(s)',
        3: 'Casa dúplex',
        4: 'Departamento en edificio',
        5: 'Vivienda en vecindad o cuartería',
        6: 'Vivienda en cuarto de azotea de un edificio',
        7: 'Local no construido para habitación',
        8: 'Vivienda móvil',
        9: 'Refugio',
        99: 'No especificado de vivienda particular'
    },

    'sexo': {
        1: 'M',
        3: 'F'
    },

    'ent': code_ent,

    'parentesco': load_paren_defs(),

    'sersalud': {
        1: 'IMSS',
        2: 'ISSSTE',
        3: 'ISSSTE Estatal',
        4: 'PEMEX, Defensa o Marina',
        5: 'SSA/Seguro Popular/Bienestar',
        6: 'IMSS-PROSPERA o IMSS-BIENESTAR',
        7: 'Consultorio, clínica u hospital privado',
        8: 'Consultorio de farmacia',
        9: 'Otro lugar',
        10: 'No se atiende',
        99: 'No especificado'
    },

    'dhsersal': {
        1: 'IMSS',
        2: 'ISSSTE',
        3: 'ISSSTE estatal',
        4: 'PEMEX, Defensa o Marina',
        5: 'Seguro Popular/Nueva Generación/Bienestar',
        6: 'IMSS-PROSPERA o IMSS-BIENESTAR',
        7: 'seguro privado',
        8: 'otra institución',
        9: 'no afiliada(o)',
        99: 'No especificado'},

    'sino_139': {
        1: 'Sí',
        3: 'No',
        9: 'No especificado'
    },

    'dis': {
        1: 'No tiene dificultad',
        2: 'Lo hace con poca dificultad',
        3: 'Lo hace con mucha dificultad',
        4: 'No puede hacerlo',
        8: 'Se desconoce el grado de la discapacidad',
        9: 'No especificado'
    },

    'dis_mental': {
        5: 'Sí',
        6: 'No',
        9: 'No especificado'
    },

    'hlengua': {
        1: 'Sí',
        3: 'No',
        9: 'No especificado',
        99: 'Blanco por pase'  # Also NAN, means person's age is less than 3
    },

    'elengua': {
        5: 'Sí',
        7: 'No',
        9: 'No especificado',
        99: 'Blanco por pase'
        # If NAN, means person's age is less than 3
        # OR that person speaks native, in which case we replace nans with 'Si'
    },

    'asisten': {
        1: 'Sí',
        3: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
        # NAN means the person's age is less than 3, set 'Blanco por pase'
    },

    'tie_traslado': {
        1: 'Hasta 15 minutos',
        2: '16 a 30 minutos',
        3: '31 minutos a 1 hora',
        4: 'Más de 1 hora y hasta 2 horas',
        5: 'Más de 2 horas',
        6: 'No se traslada',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'med_traslado': {
        1: 'Caminando',
        2: 'Bicicleta',
        3: 'Metro, tren ligero, tren suburbano',
        4: 'Trolebús',
        5: 'Metrobús (autobús en carril confinado)',
        6: 'Camión, autobús, combi, colectivo',
        7: 'Transporte escolar',
        8: 'Taxi (sitio, calle, otro)',
        9: 'Taxi (App Internet)',
        10: 'Motocicleta o motoneta',
        11: 'Automóvil o camioneta',
        12: 'Otro',
        99: 'No especificado',
        'Blanco por pase': 'Blanco por pase',
    },

    'nivacad': {
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
        99: 'No especificado',
        'Blanco por pase': 'Blanco por pase',
    },

    'alfabet': {
        1: 'Sí',
        3: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'situa_conyugal': {
        1: 'unión libre',
        2: 'separada(o)',
        3: 'divorciada(o)',
        4: 'viuda(o)',
        5: 'casada(o) sólo por el civil',
        6: 'casada(o) sólo religiosamente',
        7: 'casada(o) civil y religiosamente',
        8: 'soltera(o)',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase',
    },

    'conact': {
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
        99: 'No especificado',
        'Blanco por pase': 'Blanco por pase',
    },

    'ocupacion': load_ocupacion_defs(),
    'ocupacion_compact': {
        11: 'Funcionarios y altas autoridades de los sectores público, privado y social',
        12: 'Directores y gerentes en servicios financieros, legales, administrativos y sociales',
        13: 'Directores y gerentes en producción, tecnología y transporte',
        14: 'Directores y gerentes de ventas, restaurantes, hoteles y otros establecimientos',
        15: 'Coordinadores y jefes de área en servicios financieros, administrativos y sociales',
        16: 'Coordinadores y jefes de área en producción y tecnología',
        17: 'Coordinadores y jefes de área de ventas, restaurantes, hoteles y otros establecimientos',
        19: 'Otros directores, funcionarios, gerentes, coordinadores y jefes de área, no clasificados anteriormente',
        21: 'Profesionistas en ciencias económico-administrativas, ciencias sociales, humanistas y en artes',
        22: 'Investigadores y profesionistas en ciencias exactas, biológicas, ingeniería, informática y en telecomunicaciones',
        23: 'Profesores y especialistas en docencia',
        24: 'Médicos, enfermeras y otros especialistas en salud',
        25: 'Auxiliares y técnicos en ciencias económico-administrativas, ciencias sociales, humanistas y en artes',
        26: 'Auxiliares y técnicos en ciencias exactas, biológicas, ingeniería, informática y en telecomunicaciones',
        27: 'Auxiliares y técnicos en educación, instructores y capacitadores',
        28: 'Enfermeras, técnicos en medicina y trabajadores de apoyo en salud',
        29: 'Otros profesionistas y técnicos no clasificados anteriormente',
        31: 'Supervisores de personal de apoyo administrativo, secretarias, capturistas, cajeros y trabajadores de control de archivo y transporte',
        32: 'Supervisores y trabajadores que brindan y manejan información',
        39: 'Otros trabajadores auxiliares en actividades administrativas, no clasificados anteriormente',
        41: 'Comerciantes en establecimientos',
        42: 'Empleados de ventas en establecimientos',
        43: 'Trabajadores en servicios de alquiler',
        49: 'Otros comerciantes, empleados en ventas y agentes de ventas en establecimientos, no clasificados anteriormente',
        51: 'Trabajadores en la preparación y servicio de alimentos y bebidas, así como en servicios de esparcimiento y de hotelería',
        52: 'Trabajadores en cuidados personales y del hogar',
        53: 'Trabajadores en servicios de protección y vigilancia',
        54: 'Trabajadores de la Armada, Ejército y Fuerza Aérea',
        61: 'Trabajadores en actividades agrícolas y ganaderas',
        62: 'Trabajadores en actividades pesqueras, forestales, caza y similares',
        63: 'Operadores de maquinaria agropecuaria y forestal',
        69: 'Otros trabajadores en actividades agrícolas, ganaderas, forestales, caza y pesca, no clasificados anteriormente',
        71: 'Trabajadores en la extracción y la edificación de construcciones',
        72: 'Artesanos y trabajadores en el tratamiento y elaboración de productos de metal',
        73: 'Artesanos y trabajadores en la elaboración de productos de madera, papel, textiles y de cuero y piel',
        74: 'Artesanos y trabajadores en la elaboración de productos de hule, caucho, plásticos y de sustancias químicas',
        75: 'Trabajadores en la elaboración y procesamiento de alimentos, bebidas y productos de tabaco',
        76: 'Artesanos y trabajadores en la elaboración de productos de cerámica, vidrio, azulejo y similares',
        79: 'Otros trabajadores artesanales no clasificados anteriormente',
        81: 'Operadores de instalaciones y maquinaria industrial',
        82: 'Ensambladores y montadores de herramientas, maquinaria, productos metálicos y electrónicos',
        83: 'Conductores de transporte y de maquinaria móvil',
        89: 'Otros operadores de maquinaria industrial, ensambladores y conductores de transporte, no clasificados anteriormente',
        91: 'Trabajadores de apoyo en actividades agropecuarias, forestales, pesca y caza',
        92: 'Trabajadores de apoyo en la minería, construcción e industria',
        93: 'Ayudantes de conductores de transporte, conductores de transporte de tracción humana y animal y cargadores',
        94: 'Ayudantes en la preparación de alimentos',
        95: 'Vendedores ambulantes',
        96: 'Trabajadores domésticos, de limpieza, planchadores y otros trabajadores de limpieza',
        97: 'Trabajadores de paquetería, de apoyo para espectáculos, mensajeros y repartidores de mercancías',
        98: 'Otros trabajadores en actividades elementales y de apoyo, no clasificados anteriormente',
        99: 'Ocupaciones no especificadas ',
        'Blanco por pase': 'Blanco por pase'
    },

    'sittra': {
        1: 'empleada(o) u obrera(o)',
        2: 'jornalera(o) o peón(a)',
        3: 'ayudante con pago',
        4: 'patrón(a) o empleador(a)',
        5: 'trabajador(a) por cuenta propia',
        6: 'trabajador(a) sin pago',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase',
    },

    'prestaciones': {
        1: 'Sí',
        2: 'No',
        3: 'Sí',
        4: 'No',
        5: 'Sí',
        6: 'No',
        7: 'Sí',
        8: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase',
    },

    'actividades': {
        11: 'Agricultura, cría y explotación de animales, aprovechamiento forestal, pesca y caza',
        21: 'Minería',
        22: 'Generación, transmisión, distribución y comercialización de energía eléctrica, suministro de agua y de gas natural por ductos al consumidor final',
        23: 'Construcción',
        31: 'Industrias manufactureras',
        32: 'Industrias manufactureras',
        33: 'Industrias manufactureras',
        43: 'Comercio al por mayor',
        46: 'Comercio al por menor',
        48: 'Transportes, correos y almacenamiento',
        49: 'Transportes, correos y almacenamiento',
        51: 'Información en medios masivos',
        52: 'Servicios financieros y de seguros',
        53: 'Servicios inmobiliarios y de alquiler de bienes muebles e intangibles',
        54: 'Servicios profesionales, científicos y técnicos',
        55: 'Corporativos',
        56: 'Servicios de apoyo a los negocios y manejo de residuos, y servicios de remediación',
        61: 'Servicios educativos',
        62: 'Servicios de salud y de asistencia social',
        71: 'Servicios de esparcimiento, culturales y deportivos, y otros servicios recreativos',
        72: 'Servicios de alojamiento temporal y de preparación de alimentos y bebidas',
        81: 'Otros servicios excepto actividades gubernamentales',
        93: 'Actividades legislativas, gubernamentales, de impartición de justicia y de organismos internacionales y extraterritoriales',
        99: 'Descripciones insuficientemente especificadas general de sector de actividad',
        'Blanco por pase': 'Blanco por pase',
    },

    'tie_traslado_trab': {
        1: 'Hasta 15 minutos',
        2: '16 a 30 minutos',
        3: '31 minutos a 1 hora',
        4: 'Más de 1 hora y hasta 2 horas',
        5: 'Más de 2 horas',
        6: 'No es posible determinarlo',
        7: 'No se traslada',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },
}

cats = {
    'muns': pd.CategoricalDtype(defs['muns'].values()),
    'clavivp': pd.CategoricalDtype(defs['clavivp'].values()),
    'sexo': pd.CategoricalDtype(defs['sexo'].values()),
    'edad': [
        '0-2', '3-4', '5', '6-7', '8-11', '12-14', '15-17', '18-24',
        '25-49', '50-59', '60-64', '65-130', 'Unknown'
    ],
    'ent': pd.CategoricalDtype(
        [
            'EstaEnt', 'OtraEnt', 'OtroPais',
            'No especificado', 'Blanco por pase'
        ]
    ),
    'parentesco': pd.CategoricalDtype(defs['parentesco'].values()),
    'sersalud': pd.CategoricalDtype(defs['sersalud'].values()),
    'sino_139': pd.CategoricalDtype(defs['sino_139'].values()),
    'religion': pd.CategoricalDtype([
        'Católica', 'Protestante/cristiano evangélico', 'Otros credos',
        'Sin religión / Sin adscripción religiosa',
        'Religión no especificada'
    ]),
    'dis': pd.CategoricalDtype(DIS_CATS),
    # 'dis_mental': pd.CategoricalDtype(defs['dis_mental'].values()),
    'hlengua': pd.CategoricalDtype([
        'Sí/Sí Español', 'Sí/No español', 'Sí/No especificado',
        'No', 'No especificado', 'Blanco por pase'
    ]),
    'elengua': pd.CategoricalDtype(defs['elengua'].values()),
    'asisten': pd.CategoricalDtype(defs['asisten'].values()),
    'mun_asi': pd.CategoricalDtype(
        list(defs['muns'].values())
        + ['Blanco por pase', 'No especificado', 'OtroPais', 'OtraEnt']),
    'tie_traslado': pd.CategoricalDtype(defs['tie_traslado'].values()),
    'nivacad': pd.CategoricalDtype(nivacad_cats),
    'alfabet': pd.CategoricalDtype(defs['alfabet'].values()),
    'situa_conyugal': pd.CategoricalDtype(defs['situa_conyugal'].values()),
    'conact': pd.CategoricalDtype(defs['conact'].values()),
    'ocupacion': pd.CategoricalDtype(defs['ocupacion'].values()),
    'ocupacion_compact': pd.CategoricalDtype(defs['ocupacion_compact'].values()),
    'sittra': pd.CategoricalDtype(defs['sittra'].values()),
    'prestaciones': pd.CategoricalDtype(set(defs['prestaciones'].values())),
    'actividades': pd.CategoricalDtype(set(defs['actividades'].values())),
    'tie_traslado_trab': pd.CategoricalDtype(defs['tie_traslado_trab'].values()),
    'dhsersal': pd.CategoricalDtype(DHSERSAL_CATS),
    # 'sino': pd.CategoricalDtype(['Sí', 'No']),
}


def process_people_df(personas):

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
        defs['ent']
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

    return personas_cat


def build_X(personas_cat):
    cat_cols = [
        col for col in personas_cat.columns
        if personas_cat[col].dtype == 'category'
    ]

    personas_agg = personas_cat.groupby(
        cat_cols, observed=True)[['FACTOR']].sum().sort_index().reset_index()

    return personas_agg


def get_w_vec(X, const):

    def get_mask(X, const):

        mask_list = []
        for col, vals in const.items():
            # Loop over columns included in the constraint
            or_list = []  # Stores mask for valid entries for col

            # print(col, len(vals))
            for val in vals:
                assert val in X[col].cat.categories, (col, val)
                if val not in X[col]:
                    continue
                # Loop or values in the column
                or_list.append((X[col] == val).values)

            # Mask stores valid entris for particular comb of cols (AND clause)
            mask_list.append(np.any(or_list, axis=0))

        mask = np.all(mask_list, axis=0)
        return mask

    # if isinstance(const, list):
    #     mask = np.any([get_mask(X, subconst) for subconst in const], axis=0)
    # else:
    mask = get_mask(X, const)

    return mask.astype(int)


def get_W(X, const_dict):
    w_dict = {}
    for k, const in const_dict.items():
        if k == 'POBTOT':
            w = np.ones(len(X), dtype=int)
        else:
            w = get_w_vec(X, const)
        w_dict[k] = w
    return pd.DataFrame(w_dict).T


def process_extended_survey(data_dir, verbose=True):
    cols_drop = ['ENT', 'LOC50K']

    personas = pd.read_csv(
        data_dir / 'Personas19.CSV').drop(columns=cols_drop)
    viviendas = pd.read_csv(
        data_dir / 'Viviendas19.CSV').drop(columns=cols_drop)

    personas_cat = process_people_df(personas)

    # Split by municipality, the finer aggregation level
    # statistically representative in the survey.
    groups = personas_cat.groupby('MUN')
    XW_dict = {name: {'X': build_X(group)} for name, group in groups}
    for d in XW_dict.values():
        d['W'] = get_W(d['X'], constraints_ind)

    if verbose:
        print('Each municipality has the following number of combinations '
              'and low count (<10) entries and total pop.')
        for k, v in XW_dict.items():
            print(f'{k:>30}: {len(v["X"]):>7} '
                  f'{(v["X"].FACTOR < 10).sum()/len(v["X"])*100:>10.2f}% '
                  f'{v["X"].FACTOR.sum():>10}')

    return XW_dict


def process_census(data_dir_iter, data_dir_resageburb):
    non_count_cols = [
        'REL_H_M', 'PROM_HNV', 'GRAPROES',
        'GRAPROES_F', 'GRAPROES_M', 'PROM_OCUP', 'PRO_OCUP_C'
    ]

    # Load census data
    df_censo = pd.read_csv(
        data_dir_resageburb / 'RESAGEBURB_19CSV20.csv',
        low_memory=False,
        na_values=['N/D'],
    )

    obj_cols = ['NOM_ENT', 'NOM_MUN', 'NOM_LOC', 'AGEB']
    int_cols = ['ENTIDAD', 'MUN', 'LOC', 'MZA', 'POBTOT', 'VIVTOT']

    # For manzanas, asterisc means ommited values where VIVTOT <= 2
    mask = np.logical_and(
        df_censo.values == '*',
        np.broadcast_to((df_censo.VIVTOT.values <=2)[:, None], df_censo.shape)
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
    df_iter = pd.read_csv('/Users/gperaza/Downloads/ITER_19CSV20.csv',
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
    # TODO

    return df_iter_mun, df_iter_loc, df_agebs


def create_implicit_consts(df_censo):
    df_min = df_censo.replace(-1, 0)
    df_max = df_censo.replace(-1, 2)

    # Create columns
    for df in [df_censo, df_min, df_max]:
        df['P_UNK'] = df.POBTOT - (df.POB0_14 + df.P_15YMAS)

    # Mark uncertain values with -1 again
    df_censo['P_UNK'] = df_censo['P_UNK'].where(
        np.logical_or(
            df_min['P_UNK'] == df_max['P_UNK'],
            df_censo['P_UNK'].isna()
        ),
        -1
    )

    return df_censo, df_min, df_max


def process_census_data(
        data_dir_esurvey,
        data_dir_iter,
        data_dir_resageburb,
        verbose=True
):

    XW_dict = process_extended_survey(data_dir_esurvey, verbose)

    df_mun, df_loc, df_agebs = process_census(
        data_dir_iter, data_dir_resageburb)

    return XW_dict
