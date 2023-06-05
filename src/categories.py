import pandas as pd
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

NIVACAD_CATS = []
NIVACAD_CATS += ['Ninguno']
NIVACAD_CATS += [f'Preescolar_{i}' for i in [1, 2, 3, 99]]
NIVACAD_CATS += [f'Primaria_{i}' for i in [1, 2, 3, 4, 5, 6, 99]]
NIVACAD_CATS += [f'Secundaria_{i}' for i in [1, 2, 3, 99]]
NIVACAD_CATS += [f'Preparatoria o bachillerato general_{i}'
                 for i in [1, 2, 3, 4, 99]]
NIVACAD_CATS += [f'Bachillerato tecnológico_{i}' for i in [1, 2, 3, 4, 99]]
NIVACAD_CATS += [f'Estudios técnicos o comerciales con primaria terminada_{i}'
                 for i in [1, 2, 3, 4, 99]]
NIVACAD_CATS += [
    f'Estudios técnicos o comerciales con secundaria terminada_{i}'
    for i in [1, 2, 3, 4, 5, 99]
]
NIVACAD_CATS += [
    f'Estudios técnicos o comerciales con preparatoria terminada_{i}'
    for i in [1, 2, 3, 4, 99]
]
NIVACAD_CATS += [f'Normal con primaria o secundaria terminada_{i}'
                 for i in [1, 2, 3, 4, 99]]
NIVACAD_CATS += [f'Normal de licenciatura_{i}' for i in [1, 2, 3, 4, 5, 6, 99]]
NIVACAD_CATS += [f'Licenciatura_{i}' for i in [1, 2, 3, 4, 5, 6, 7, 8, 99]]
NIVACAD_CATS += [f'Especialidad_{i}' for i in [1, 2, 99]]
NIVACAD_CATS += [f'Maestría_{i}' for i in [1, 2, 3, 4, 5, 6, 99]]
NIVACAD_CATS += [f'Doctorado_{i}' for i in [1, 2, 3, 4, 5, 6, 99]]
NIVACAD_CATS += ['No especificado']
NIVACAD_CATS += ['Blanco por pase']


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
        11: 'Agricultura, cría y explotación de animales,'
        ' aprovechamiento forestal, pesca y caza',
        21: 'Minería',
        22: 'Generación, transmisión, distribución y comercialización'
        ' de energía eléctrica, suministro de agua y de gas natural por'
        ' ductos al consumidor final',
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
        53: 'Servicios inmobiliarios y de alquiler de bienes muebles'
        ' e intangibles',
        54: 'Servicios profesionales, científicos y técnicos',
        55: 'Corporativos',
        56: 'Servicios de apoyo a los negocios y manejo de residuos,'
        ' y servicios de remediación',
        61: 'Servicios educativos',
        62: 'Servicios de salud y de asistencia social',
        71: 'Servicios de esparcimiento, culturales y deportivos, y'
        ' otros servicios recreativos',
        72: 'Servicios de alojamiento temporal y de preparación de'
        ' alimentos y bebidas',
        81: 'Otros servicios excepto actividades gubernamentales',
        93: 'Actividades legislativas, gubernamentales, de impartición'
        ' de justicia y de organismos internacionales y extraterritoriales',
        99: 'Descripciones insuficientemente especificadas general'
        ' de sector de actividad',
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
    'nivacad': pd.CategoricalDtype(NIVACAD_CATS),
    'alfabet': pd.CategoricalDtype(defs['alfabet'].values()),
    'situa_conyugal': pd.CategoricalDtype(defs['situa_conyugal'].values()),
    'conact': pd.CategoricalDtype(defs['conact'].values()),
    'ocupacion': pd.CategoricalDtype(defs['ocupacion'].values()),
    'ocupacion_compact': pd.CategoricalDtype(
        defs['ocupacion_compact'].values()),
    'sittra': pd.CategoricalDtype(defs['sittra'].values()),
    'prestaciones': pd.CategoricalDtype(set(defs['prestaciones'].values())),
    'actividades': pd.CategoricalDtype(set(defs['actividades'].values())),
    'tie_traslado_trab': pd.CategoricalDtype(
        defs['tie_traslado_trab'].values()),
    'dhsersal': pd.CategoricalDtype(DHSERSAL_CATS),
    # 'sino': pd.CategoricalDtype(['Sí', 'No']),
}
