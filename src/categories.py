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

    # 'conact': {
    #     10: 'Trabajó',
    #     13: 'Declara que busca trabajo /  se rescata que trabaja',
    #     14: 'Declara jubilado o pensionado / se rescata que trabaja',
    #     15: 'Declara estudiante / se rescata que trabaja',
    #     16: 'Se dedica a los quehaceres del hogar / se rescata que trabaja',
    #     17: 'Declara que tiene limitaciónes / se rescata que trabaja',
    #     18: 'Declara otra situación de actividad / se rescata que trabaja',
    #     19: 'No se tiene información / se rescata que trabaja',
    #     20: 'Tenía trabajo pero no trabajó',
    #     30: 'Buscó trabajo',
    #     40: 'Es pensionada(o) o jubilada(o)',
    #     50: 'Es estudiante',
    #     60: 'Se dedica a los quehaceres del hogar',
    #     70: 'Está incapacitado permanentemente para trabajar',
    #     80: 'No trabaja',
    #     99: 'No especificado',
    #     'Blanco por pase': 'Blanco por pase',
    # },

    'conact': {
        10: 'Trabaja',
        13: 'Trabaja',
        14: 'Trabaja',
        15: 'Trabaja',
        16: 'Trabaja',
        17: 'Trabaja',
        18: 'Trabaja',
        19: 'Trabaja',
        20: 'Trabaja',
        30: 'Buscó trabajo',
        40: 'No trabaja',
        50: 'No trabaja',
        60: 'No trabaja',
        70: 'No trabaja',
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

    'paredes': {
        1: 'Material de desecho',
        2: 'Lámina de cartón',
        3: 'Lámina de asbesto o metálica',
        4: 'Carrizo, bambú  o palma',
        5: 'Embarro o bajareque',
        6: 'Madera',
        7: 'Adobe',
        8: 'Tabique, ladrillo, block, piedra, cantera, cemento o concreto',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'techos': {
        1: 'Material de desecho',
        2: 'Lámina de cartón',
        3: 'Lámina metálica',
        4: 'Lámina de asbesto ',
        5: 'Lámina de fibrocemento',
        6: 'Palma o paja',
        7: 'Madera o tejamanil',
        8: 'Terrado con viguería',
        9: 'Teja',
        10: 'Losa de concreto o viguetas con bovedilla',
        99: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'pisos': {
        1: 'Tierra',
        2: 'No Tierra',  # 'Cemento o firme',
        3: 'No Tierra',  # 'Madera, mosaico u otro recubrimiento',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'cocina': {
        1: 'Sí',
        3: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'cuadorm': {1: 1} | {i: '2+' for i in range(2, 26)} | {
        99: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'totcuart': {1: 1, 2: 2} | {i: '3+' for i in range(3, 26)} | {
        99: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'lug_coc': {
        1: 'Interior de la vivienda.',
        2: 'Cuarto separado de la vivienda.',
        3: 'Pasillo o corredor fuera de la vivienda.',
        4: 'Tejabán o techito.',
        5: 'Al aire libre.',
        6: 'No tiene un espacio para cocinar.',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'combustible': {
        1: 'Leña o carbón',
        2: 'Gas',
        3: 'Electricidad',
        4: 'Otro combustible',
        5: 'No cocinan',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'estufa': {
        1: 'Tiene un tubo o chimenea para sacar el humo.',
        3: 'No tiene tubo o chimenea para sacar el humo.',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'electricidad': {
        1: 'Sí',
        3: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'focos': {i: i for i in range(1, 999)} | {
        999: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'focos_ahorra': {i: i for i in range(0, 999)} | {
        999: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'agua_entubada': {
        1: 'Tienen agua entubada.',  # 'Dentro de la vivienda.',
        2: 'Tienen agua entubada.',  # 'Sólo en el patio o terreno.',
        3: 'No tienen agua entubada.',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'aba_agua_entu': {
        1: 'Del servicio público de agua.',
        2: 'De otro lugar.',  # 'De un pozo comunitario.',
        3: 'De otro lugar.',  # 'De un pozo particular.',
        4: 'De otro lugar.',  # 'De una pipa.',
        5: 'De otro lugar.',  # 'De otra vivienda.',
        6: 'De otro lugar.',  # 'De la lluvia.',
        7: 'De otro lugar.',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'aba_agua_no_entu': {
        1: 'Un pozo.',
        2: 'Una llave comunitaria.',
        3: 'Otra vivienda.',
        4: 'Un río, arroyo o lago.',
        5: 'La trae una pipa.',
        6: 'La captan de la lluvia.',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'tinaco': {
        1: 'Sí',
        2: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'cisterna': {
        3: 'Sí',
        4: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'bomba_agua': {
        5: 'Sí',
        6: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'regadera': {
        7: 'Sí',
        8: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'boiler': {
        1: 'Sí',
        2: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'calentador_solar': {
        3: 'Sí',
        4: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'aire_acon': {
        5: 'Sí',
        6: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'panel_solar': {
        7: 'Sí',
        8: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'sersan': {
        1: 'Taza de baño (excusado o sanitario).',
        2: 'Letrina (pozo u hoyo).',
        3: 'No tienen taza de baño ni letrina.',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'conagua': {
        1: 'Con agua.',  # 'Tiene descarga directa de agua.',
        2: 'Con agua.',  # 'Le echan agua con cubeta.',
        3: 'No se le puede echar agua.',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'usoexc': {
        1: 'Sí',
        3: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'drenaje': {
        1: 'Tiene drenaje.',  # 'La red pública.',
        2: 'Tiene drenaje.',  # 'Una fosa séptica o tanque séptico (biodigestor).',
        3: 'Tiene drenaje.',  # 'Una tubería que va a dar a una barranca o grieta.',
        4: 'Tiene drenaje.',  # 'Una tubería que va a dar a un río, lago o mar.',
        5: 'No tiene drenaje.',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'separacion1': {
        1: 'Sí',
        2: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'separacion2': {
        3: 'Sí',
        4: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'separacion3': {
        5: 'Sí',
        6: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'separacion4': {
        7: 'Sí',
        8: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'destino_bas': {
        1: 'Se la dan a un camión o carrito de basura.',
        2: 'La dejan en un contenedor o depósito.',
        3: 'La queman.',
        4: 'La entierran.',
        5: 'La llevan al basurero público.',
        6: 'La tiran en otro lugar. (Calle, baldío, barranca, río)',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'refrigerador': {
        1: 'Sí',
        2: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'lavadora': {
        3: 'Sí',
        4: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'horno': {
        5: 'Sí',
        6: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'autoprop': {
        7: 'Sí',
        8: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'motocicleta': {
        1: 'Sí',
        2: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'bicicleta': {
        3: 'Sí',
        4: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'radio': {
        5: 'Sí',
        6: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'televisor': {
        7: 'Sí',
        8: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'computadora': {
        1: 'Sí',
        2: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'telefono': {
        3: 'Sí',
        4: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'celular': {
        5: 'Sí',
        6: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'internet': {
        7: 'Sí',
        8: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'serv_tv_paga': {
        1: 'Sí',
        2: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'serv_pel_paga': {
        3: 'Sí',
        4: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'con_vjuegos': {
        5: 'Sí',
        6: 'No',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'tenencia': {
        1: 'Vive la persona que es dueña o propietaria.',
        2: 'Se paga renta.',
        3: 'Es de un familiar o les prestan la vivienda.',
        4: 'La ocupan en otra situación.',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'escrituras': {
        1: 'A nombre de la persona dueña o propietaria.',
        2: 'A nombre de otra persona.',
        3: 'No tiene escrituras.',
        8: 'No sabe',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'forma_adqui': {
        1: 'La compró hecha.',
        2: 'La mandó construir.',
        3: 'La construyó ella (él) misma(o) o familiares.',
        4: 'La heredó.',
        5: 'La recibió como apoyo del gobierno.',
        6: 'La obtuvo de otra manera.',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'financiamiento1': {
        1: 'INFONAVIT',
        2: 'FOVISSSTE',
        3: 'PEMEX',
        4: 'FONHAPO',
        5: 'Banco',
        6: 'Otra institución',
        7: 'Le prestó un familiar, amiga(o) o prestamista.',
        8: 'Usó sus propios recursos.',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'financiamiento2': {
        2: 'FOVISSSTE',
        3: 'PEMEX',
        4: 'FONHAPO',
        5: 'Banco',
        6: 'Otra institución',
        7: 'Le prestó un familiar, amiga(o) o prestamista.',
        8: 'Usó sus propios recursos.',
        'Blanco por pase': 'Blanco por pase'
    },

    'financiamiento3': {
        3: 'PEMEX',
        4: 'FONHAPO',
        5: 'Banco',
        6: 'Otra institución',
        7: 'Le prestó un familiar, amiga(o) o prestamista.',
        8: 'Usó sus propios recursos.',
        'Blanco por pase': 'Blanco por pase'
    },

    'deuda': {
        1: 'Está totalmente pagada',
        2: 'La están pagando',
        3: 'La dejaron de pagar',
        8: 'No sabe',
        9: 'No especificado',
        'Blanco por pase': 'Blanco por pase'
    },

    'mconmig': {
        1: 'Sí',
        3: 'No',
        9: 'No especificado',
    },

    'ingr_perotropais': {
        1: 'Sí',
        2: 'No',
        9: 'No especificado',
    },

    'ingr_perdentpais': {
        3: 'Sí',
        4: 'No',
        9: 'No especificado',
    },

    'ingr_ayugob': {
        5: 'Sí',
        6: 'No',
        9: 'No especificado',
    },

    'ingr_jubpen': {
        7: 'Sí',
        8: 'No',
        9: 'No especificado',
    },

    'alimentacion': {
        1: 'Sí',
        3: 'No',
        9: 'No especificado',
    },

    'alim_adl1': {
        1: 'Sí',
        2: 'No',
        9: 'No especificado',
    },

    'alim_adl2': {
        3: 'Sí',
        4: 'No',
        9: 'No especificado',
    },

    'ing_alim_adl1': {
        1: 'Sí',
        2: 'No',
        9: 'No especificado',
    },

    'ing_alim_adl2': {
        3: 'Sí',
        4: 'No',
        9: 'No especificado',
    },

    'ing_alim_adl3': {
        5: 'Sí',
        6: 'No',
        9: 'No especificado',
    },

    'tipohog': {
        1: 'Hogar Nuclear (Familiar)',
        2: 'Hogar Ampliado (Familiar)',
        3: 'Hogar Compuesto (Familiar)',
        4: 'Hogar no especificado (Familiar)',
        5: 'Hogar unipersonal (No familiar)',
        6: 'Hogar corresidente (No familiar)',
        9: 'No se sabe la composición',
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
    'conact': pd.CategoricalDtype(set(defs['conact'].values())),
    'ocupacion': pd.CategoricalDtype(defs['ocupacion'].values()),
    'ocupacion_compact': pd.CategoricalDtype(
        defs['ocupacion_compact'].values()),
    'sittra': pd.CategoricalDtype(defs['sittra'].values()),
    'prestaciones': pd.CategoricalDtype(set(defs['prestaciones'].values())),
    'actividades': pd.CategoricalDtype(set(defs['actividades'].values())),
    'tie_traslado_trab': pd.CategoricalDtype(
        defs['tie_traslado_trab'].values()),
    'dhsersal': pd.CategoricalDtype(DHSERSAL_CATS),
    'paredes': pd.CategoricalDtype(defs['paredes'].values()),
    'techos': pd.CategoricalDtype(defs['techos'].values()),
    'pisos': pd.CategoricalDtype(set(defs['pisos'].values())),
    'cocina': pd.CategoricalDtype(defs['cocina'].values()),
    'cuadorm': pd.CategoricalDtype(set(defs['cuadorm'].values())),
    'totcuart': pd.CategoricalDtype(set(defs['totcuart'].values())),
    'lug_coc': pd.CategoricalDtype(defs['lug_coc'].values()),
    'combustible': pd.CategoricalDtype(defs['combustible'].values()),
    'estufa': pd.CategoricalDtype(defs['estufa'].values()),
    'electricidad': pd.CategoricalDtype(defs['electricidad'].values()),
    'focos': pd.CategoricalDtype(defs['focos'].values()),
    'focos_ahorra': pd.CategoricalDtype(defs['focos_ahorra'].values()),
    'agua_entubada': pd.CategoricalDtype(set(defs['agua_entubada'].values())),
    'aba_agua_entu': pd.CategoricalDtype(set(defs['aba_agua_entu'].values())),
    'aba_agua_no_entu': pd.CategoricalDtype(defs['aba_agua_no_entu'].values()),
    'tinaco': pd.CategoricalDtype(defs['tinaco'].values()),
    'cisterna': pd.CategoricalDtype(defs['cisterna'].values()),
    'bomba_agua': pd.CategoricalDtype(defs['bomba_agua'].values()),
    'regadera': pd.CategoricalDtype(defs['regadera'].values()),
    'boiler': pd.CategoricalDtype(defs['boiler'].values()),
    'calentador_solar': pd.CategoricalDtype(defs['calentador_solar'].values()),
    'aire_acon': pd.CategoricalDtype(defs['aire_acon'].values()),
    'panel_solar': pd.CategoricalDtype(defs['panel_solar'].values()),
    'sersan': pd.CategoricalDtype(defs['sersan'].values()),
    'conagua': pd.CategoricalDtype(set(defs['conagua'].values())),
    'usoexc': pd.CategoricalDtype(defs['usoexc'].values()),
    'drenaje': pd.CategoricalDtype(set(defs['drenaje'].values())),
    'separacion1': pd.CategoricalDtype(defs['separacion1'].values()),
    'separacion2': pd.CategoricalDtype(defs['separacion2'].values()),
    'separacion3': pd.CategoricalDtype(defs['separacion3'].values()),
    'separacion4': pd.CategoricalDtype(defs['separacion4'].values()),
    'destino_bas': pd.CategoricalDtype(defs['destino_bas'].values()),
    'refrigerador': pd.CategoricalDtype(defs['refrigerador'].values()),
    'lavadora': pd.CategoricalDtype(defs['lavadora'].values()),
    'horno': pd.CategoricalDtype(defs['horno'].values()),
    'autoprop': pd.CategoricalDtype(defs['autoprop'].values()),
    'motocicleta': pd.CategoricalDtype(defs['motocicleta'].values()),
    'bicicleta': pd.CategoricalDtype(defs['bicicleta'].values()),
    'radio': pd.CategoricalDtype(defs['radio'].values()),
    'televisor': pd.CategoricalDtype(defs['televisor'].values()),
    'computadora': pd.CategoricalDtype(defs['computadora'].values()),
    'telefono': pd.CategoricalDtype(defs['telefono'].values()),
    'celular': pd.CategoricalDtype(defs['celular'].values()),
    'internet': pd.CategoricalDtype(defs['internet'].values()),
    'serv_tv_paga': pd.CategoricalDtype(defs['serv_tv_paga'].values()),
    'serv_pel_paga': pd.CategoricalDtype(defs['serv_pel_paga'].values()),
    'con_vjuegos': pd.CategoricalDtype(defs['con_vjuegos'].values()),
    'tenencia': pd.CategoricalDtype(defs['tenencia'].values()),
    'escrituras': pd.CategoricalDtype(defs['escrituras'].values()),
    'forma_adqui': pd.CategoricalDtype(defs['forma_adqui'].values()),
    'financiamiento1': pd.CategoricalDtype(defs['financiamiento1'].values()),
    'financiamiento2': pd.CategoricalDtype(defs['financiamiento2'].values()),
    'financiamiento3': pd.CategoricalDtype(defs['financiamiento3'].values()),
    'deuda': pd.CategoricalDtype(defs['deuda'].values()),
    'mconmig': pd.CategoricalDtype(defs['mconmig'].values()),
    'ingr_perotropais': pd.CategoricalDtype(defs['ingr_perotropais'].values()),
    'ingr_perdentpais': pd.CategoricalDtype(defs['ingr_perdentpais'].values()),
    'ingr_ayugob': pd.CategoricalDtype(defs['ingr_ayugob'].values()),
    'ingr_jubpen': pd.CategoricalDtype(defs['ingr_jubpen'].values()),
    'alimentacion': pd.CategoricalDtype(defs['alimentacion'].values()),
    'alim_adl1': pd.CategoricalDtype(defs['alim_adl1'].values()),
    'alim_adl2': pd.CategoricalDtype(defs['alim_adl2'].values()),
    'ing_alim_adl1': pd.CategoricalDtype(defs['ing_alim_adl1'].values()),
    'ing_alim_adl2': pd.CategoricalDtype(defs['ing_alim_adl2'].values()),
    'ing_alim_adl3': pd.CategoricalDtype(defs['ing_alim_adl3'].values()),
    'tipohog': pd.CategoricalDtype(defs['tipohog'].values()),

}
