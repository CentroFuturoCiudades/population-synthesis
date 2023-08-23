from itertools import product

EDAD = [
    '0-2', '3-4', '5', '6-7', '8-11', '12-14',
    '15-17', '18-24', '25-49', '50-59', '60-64',
    '65-130'
]
EDAD_3YMAS = EDAD[1:]
EDAD_5YMAS = EDAD[2:]
EDAD_12YMAS = EDAD[5:]
EDAD_15YMAS = EDAD[6:]
EDAD_18YMAS = EDAD[7:]
EDAD_3A5 = EDAD[1:3]
EDAD_6A11 = EDAD[3:5]
EDAD_8A14 = EDAD[4:6]
EDAD_12A14 = EDAD[5:6]
EDAD_15A17 = EDAD[6:7]
EDAD_18A24 = EDAD[7:8]
EDAD_15A49 = EDAD[6:9]
EDAD_60YMAS = EDAD[10:]
EDAD_0A14 = EDAD[:6]
EDAD_15A64 = EDAD[6:11]
EDAD_65YMAS = EDAD[11:]

EDAD.append('Unknown')

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

NIVACAD_BAS = [
    # 'Ninguno',
    # 'Preescolar_1', 'Preescolar_2', 'Preescolar_3', 'Preescolar_99',
    # 'Primaria_1', 'Primaria_2', 'Primaria_3',
    # 'Primaria_4',  'Primaria_5', 'Primaria_99',
    # 'Primaria_6',
    # 'Estudios técnicos o comerciales con primaria terminada_1',
    # 'Estudios técnicos o comerciales con primaria terminada_2',
    # 'Estudios técnicos o comerciales con primaria terminada_3',
    # 'Estudios técnicos o comerciales con primaria terminada_4',
    # 'Estudios técnicos o comerciales con primaria terminada_99',
    # 'Secundaria_1', 'Secundaria_2', 'Secundaria_99',
    # 'Secundaria_3',

    'Sin Educación',
    'Primaria_com',
    'Primaria_incom',
    'EToC_prim',
    'Secundaria_com',
    'Secundaria_incom'
]

NIVACAD_POSBAS = [
    # 'Preparatoria o bachillerato general_1',
    # 'Preparatoria o bachillerato general_2',
    # 'Preparatoria o bachillerato general_3',
    # 'Preparatoria o bachillerato general_4',
    # 'Preparatoria o bachillerato general_99',
    'Preparatoria',

    # 'Bachillerato tecnológico_1',
    # 'Bachillerato tecnológico_2',
    # 'Bachillerato tecnológico_3',
    # 'Bachillerato tecnológico_4',
    # 'Bachillerato tecnológico_99',
    'Bachillerato tecnológico',

    # 'Estudios técnicos o comerciales con secundaria terminada_1',
    # 'Estudios técnicos o comerciales con secundaria terminada_2',
    # 'Estudios técnicos o comerciales con secundaria terminada_3',
    # 'Estudios técnicos o comerciales con secundaria terminada_4',
    # 'Estudios técnicos o comerciales con secundaria terminada_5',
    # 'Estudios técnicos o comerciales con secundaria terminada_99',
    'EToC_sec',

    # 'Estudios técnicos o comerciales con preparatoria terminada_1',
    # 'Estudios técnicos o comerciales con preparatoria terminada_2',
    # 'Estudios técnicos o comerciales con preparatoria terminada_3',
    # 'Estudios técnicos o comerciales con preparatoria terminada_4',
    # 'Estudios técnicos o comerciales con preparatoria terminada_99',
    'EToC_prep',

    # 'Normal con primaria o secundaria terminada_1',
    # 'Normal con primaria o secundaria terminada_2',
    # 'Normal con primaria o secundaria terminada_3',
    # 'Normal con primaria o secundaria terminada_4',
    # 'Normal con primaria o secundaria terminada_99',
    'Normal prim/sec term',

    # 'Normal de licenciatura_1',
    # 'Normal de licenciatura_2',
    # 'Normal de licenciatura_3',
    # 'Normal de licenciatura_4',
    # 'Normal de licenciatura_5',
    # 'Normal de licenciatura_6',
    # 'Normal de licenciatura_99',
    'Normal de licenciatura',

    # 'Licenciatura_1',
    # 'Licenciatura_2',
    # 'Licenciatura_3',
    # 'Licenciatura_4',
    # 'Licenciatura_5',
    # 'Licenciatura_6',
    # 'Licenciatura_7',
    # 'Licenciatura_8',
    # 'Licenciatura_99',
    'Licenciatura',

    # 'Especialidad_1',
    # 'Especialidad_2',
    # 'Especialidad_99',
    'Especialidad',

    # 'Maestría_1',
    # 'Maestría_2',
    # 'Maestría_3',
    # 'Maestría_4',
    # 'Maestría_5',
    # 'Maestría_6',
    # 'Maestría_99',
    'Maestría',

    # 'Doctorado_1',
    # 'Doctorado_2',
    # 'Doctorado_3',
    # 'Doctorado_4',
    # 'Doctorado_5',
    # 'Doctorado_6',
    # 'Doctorado_99',
    'Doctorado'
]

# Specify crosstabulations for census constraints.
# Ommited variables sums over all categories of that variable


def get_ind_const():
    constraints_ind = {
        # POPULATION
        'POBTOT': {},

        'POBFEM': {
            'SEXO': ['F']
        },

        'POBMAS': {
            'SEXO': ['M']
        },

        'P_0A2': {
            'EDAD': ['0-2']
        },
        'P_0A2_F': {
            'EDAD': ['0-2'],
            'SEXO': ['F']
        },
        'P_0A2_M': {
            'EDAD': ['0-2'],
            'SEXO': ['M']
        },

        'P_3YMAS': {
            'EDAD': EDAD_3YMAS
        },
        'P_3YMAS_M': {
            'EDAD': EDAD_3YMAS,
            'SEXO': ['M']
        },
        'P_3YMAS_F': {
            'EDAD': EDAD_3YMAS,
            'SEXO': ['F']
        },

        'P_5YMAS': {
            'EDAD': EDAD_5YMAS
        },
        'P_5YMAS_M': {
            'EDAD': EDAD_5YMAS,
            'SEXO': ['M']
        },
        'P_5YMAS_F': {
            'EDAD': EDAD_5YMAS,
            'SEXO': ['F']
        },

        'P_12YMAS': {
            'EDAD': EDAD_12YMAS
        },
        'P_12YMAS_M': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['M']
        },
        'P_12YMAS_F': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['F']
        },

        'P_15YMAS': {
            'EDAD': EDAD_15YMAS
        },
        'P_15YMAS_M': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['M']
        },
        'P_15YMAS_F': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['F']
        },

        'P_18YMAS': {
            'EDAD': EDAD_18YMAS
        },
        'P_18YMAS_M': {
            'EDAD': EDAD_18YMAS,
            'SEXO': ['M']
        },
        'P_18YMAS_F': {
            'EDAD': EDAD_18YMAS,
            'SEXO': ['F']
        },

        'P_3A5': {
            'EDAD': EDAD_3A5
        },
        'P_3A5_M': {
            'EDAD': EDAD_3A5,
            'SEXO': ['M']
        },
        'P_3A5_F': {
            'EDAD': EDAD_3A5,
            'SEXO': ['F']
        },

        'P_6A11': {
            'EDAD': EDAD_6A11
        },
        'P_6A11_M': {
            'EDAD': EDAD_6A11,
            'SEXO': ['M']
        },
        'P_6A11_F': {
            'EDAD': EDAD_6A11,
            'SEXO': ['F']
        },

        'P_8A14': {
            'EDAD': EDAD_8A14
        },
        'P_8A14_M': {
            'EDAD': EDAD_8A14,
            'SEXO': ['M']
        },
        'P_8A14_F': {
            'EDAD': EDAD_8A14,
            'SEXO': ['F']
        },

        'P_12A14': {
            'EDAD': EDAD_12A14
        },
        'P_12A14_M': {
            'EDAD': EDAD_12A14,
            'SEXO': ['M']
        },
        'P_12A14_F': {
            'EDAD': EDAD_12A14,
            'SEXO': ['F']
        },

        'P_15A17': {
            'EDAD': EDAD_15A17
        },
        'P_15A17_M': {
            'EDAD': EDAD_15A17,
            'SEXO': ['M']
        },
        'P_15A17_F': {
            'EDAD': EDAD_15A17,
            'SEXO': ['F']
        },

        'P_18A24': {
            'EDAD': EDAD_18A24
        },
        'P_18A24_M': {
            'EDAD': EDAD_18A24,
            'SEXO': ['M']
        },
        'P_18A24_F': {
            'EDAD': EDAD_18A24,
            'SEXO': ['F']
        },

        'P_15A49_F': {
            'EDAD': EDAD_15A49,
            'SEXO': ['F']
        },

        'P_60YMAS': {
            'EDAD': EDAD_60YMAS
        },
        'P_60YMAS_M': {
            'EDAD': EDAD_60YMAS,
            'SEXO': ['M']
        },
        'P_60YMAS_F': {
            'EDAD': EDAD_60YMAS,
            'SEXO': ['F']
        },

        'POB0_14': {
            'EDAD': EDAD_0A14
        },

        'POB15_64': {
            'EDAD': EDAD_15A64
        },

        'POB65_MAS': {
            'EDAD': EDAD_65YMAS
        },

        # Implicit
        'P_UNK_F': {
            'SEXO': ['F'],
            'EDAD': ['Unknown']
        },
        'P_UNK_M': {
            'SEXO': ['M'],
            'EDAD': ['Unknown']
        },

        # MIGRATION

        'PNACENT': {
            'ENT_PAIS_NAC': ['EstaEnt'],
        },
        'PNACENT_F': {
            'SEXO': ['F'],
            'ENT_PAIS_NAC': ['EstaEnt'],
        },
        'PNACENT_M': {
            'SEXO': ['M'],
            'ENT_PAIS_NAC': ['EstaEnt'],
        },
        'PNACOE': {
            'ENT_PAIS_NAC': ['OtraEnt'],
        },
        'PNACOE_F': {
            'SEXO': ['F'],
            'ENT_PAIS_NAC': ['OtraEnt'],
        },
        'PNACOE_M': {
            'SEXO': ['M'],
            'ENT_PAIS_NAC': ['OtraEnt'],
        },
        'PRES2015': {
            'EDAD': EDAD_5YMAS,
            'ENT_PAIS_RES_5A': ['EstaEnt'],
        },
        'PRES2015_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_5YMAS,
            'ENT_PAIS_RES_5A': ['EstaEnt'],
        },
        'PRES2015_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_5YMAS,
            'ENT_PAIS_RES_5A': ['EstaEnt'],
        },
        'PRESOE15': {
            'EDAD': EDAD_5YMAS,
            'ENT_PAIS_RES_5A': ['OtraEnt'],
        },
        'PRESOE15_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_5YMAS,
            'ENT_PAIS_RES_5A': ['OtraEnt'],
        },
        'PRESOE15_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_5YMAS,
            'ENT_PAIS_RES_5A': ['OtraEnt'],
        },
        # Implicit
        'PNA_OP_BPP_NE_F': {
            'SEXO': ['F'],
            'ENT_PAIS_NAC': ['OtroPais', 'No especificado'],
        },
        'PNA_OP_BPP_NE_M': {
            'SEXO': ['M'],
            'ENT_PAIS_NAC': ['OtroPais', 'No especificado'],
        },
        'PRES15_OP_BPP_NE_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_5YMAS,
            'ENT_PAIS_RES_5A': ['OtroPais', 'No especificado'],
        },
        'PRES15_OP_BPP_NE_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_5YMAS,
            'ENT_PAIS_RES_5A': ['OtroPais', 'No especificado'],
        },

        # ETNICITY

        'P3YM_HLI': {
            'EDAD': EDAD_3YMAS,
            'HLENGUA': ['Sí/Sí Español', 'Sí/No español', 'Sí/No especificado']
        },
        'P3YM_HLI_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_3YMAS,
            'HLENGUA': ['Sí/Sí Español', 'Sí/No español', 'Sí/No especificado']
        },
        'P3YM_HLI_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_3YMAS,
            'HLENGUA': ['Sí/Sí Español', 'Sí/No español', 'Sí/No especificado']
        },
        'P3HLINHE': {
            'EDAD': EDAD_3YMAS,
            'HLENGUA': ['Sí/No español'],
        },
        'P3HLINHE_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_3YMAS,
            'HLENGUA': ['Sí/No español'],
        },
        'P3HLINHE_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_3YMAS,
            'HLENGUA': ['Sí/No español'],
        },
        'P3HLI_HE': {
            'EDAD': EDAD_3YMAS,
            'HLENGUA': ['Sí/Sí Español'],
        },
        'P3HLI_HE_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_3YMAS,
            'HLENGUA': ['Sí/Sí Español'],
        },
        'P3HLI_HE_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_3YMAS,
            'HLENGUA': ['Sí/Sí Español'],
        },
        'P5_HLI': {
            'EDAD': EDAD_5YMAS,
            'HLENGUA': [
                'Sí/Sí Español', 'Sí/No español', 'Sí/No especificado'
            ],
        },
        'P5_HLI_NHE': {
            'EDAD': EDAD_5YMAS,
            'HLENGUA': ['Sí/No español'],
        },
        'P5_HLI_HE': {
            'EDAD': EDAD_5YMAS,
            'HLENGUA': ['Sí/Sí Español'],
        },
        'POB_AFRO': {
            'AFRODES': ['Sí'],
        },
        'POB_AFRO_F': {
            'SEXO': ['F'],
            'AFRODES': ['Sí'],
        },
        'POB_AFRO_M': {
            'SEXO': ['M'],
            'AFRODES': ['Sí'],
        },
        # Implicit
        'POB_AFRO_NO_NE_F': {
            'SEXO': ['F'],
            'AFRODES': ['No', 'No especificado']
        },
        'POB_AFRO_NO_NE_M': {
            'SEXO': ['M'],
            'AFRODES': ['No', 'No especificado']
        },
        'P3_LI_NO_BPP_NE_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_3YMAS,
            'HLENGUA': ['No especificado', 'No']
        },
        'P3_LI_NO_BPP_NE_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_3YMAS,
            'HLENGUA': ['No especificado', 'No']
        },
        'P5_LI_NO_BPP_NE': {
            'EDAD': EDAD_5YMAS,
            'HLENGUA': ['No especificado', 'No']
        },
        'P3HLI_NE_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_3YMAS,
            'HLENGUA': ['Sí/No especificado'],
        },
        'P3HLI_NE_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_3YMAS,
            'HLENGUA': ['Sí/No especificado'],
        },
        'P5HLI_NE': {
            'EDAD': EDAD_5YMAS,
            'HLENGUA': ['Sí/No especificado'],
        },
        'P34HLI_HE': {
            'EDAD': ['3-4'],
            'HLENGUA': ['Sí/Sí Español'],
        },
        'P34HLI_NHE': {
            'EDAD': ['3-4'],
            'HLENGUA': ['Sí/No español'],
        },
        'P34HLI_NE': {
            'EDAD': ['3-4'],
            'HLENGUA': ['Sí/No especificado'],
        },

        # DISABILITY
        'PCON_DISC': {
            'DIS': [c for c in DIS_CATS if '3' in c or '4' in c]
        },
        'PCDISC_MOT': {
            'DIS': [c for c in DIS_CATS if c[2] in ['3', '4']],
        },
        'PCDISC_VIS': {
            'DIS': [c for c in DIS_CATS if c[0] in ['3', '4']],
        },
        'PCDISC_LENG': {
            'DIS': [c for c in DIS_CATS if c[5] in ['3', '4']],
        },
        'PCDISC_AUD': {
            'DIS': [c for c in DIS_CATS if c[1] in ['3', '4']],
        },
        'PCDISC_MOT2': {
            'DIS': [c for c in DIS_CATS if c[4] in ['3', '4']],
        },
        'PCDISC_MEN': {
            'DIS': [c for c in DIS_CATS if c[3] in ['3', '4']],
        },
        'PCON_LIMI': {
            'DIS': [c for c in DIS_CATS if '2' in c]
        },
        'PCLIM_CSB': {
            'DIS': [c for c in DIS_CATS if c[2] == '2'],
        },
        'PCLIM_VIS': {
            'DIS': [c for c in DIS_CATS if c[0] == '2'],
        },
        'PCLIM_HACO': {
            'DIS': [c for c in DIS_CATS if c[5] == '2'],
        },
        'PCLIM_OAUD': {
            'DIS': [c for c in DIS_CATS if c[1] == '2'],
        },
        'PCLIM_MOT2': {
            'DIS': [c for c in DIS_CATS if c[4] == '2'],
        },
        'PCLIM_RE_CO': {
            'DIS': [c for c in DIS_CATS if c[3] == '2'],
        },
        'PCLIM_PMEN': {
            'DIS': [c for c in DIS_CATS if c[6] == '5'],
        },
        'PSIND_LIM': {
            'DIS': ['1111116'],
        },

        # EDUCATION
        'P3A5_NOA': {
            'EDAD': EDAD_3A5,
            'ASISTEN': ['No'],
        },
        'P3A5_NOA_F': {
            'EDAD': EDAD_3A5,
            'SEXO': ['F'],
            'ASISTEN': ['No'],
        },
        'P3A5_NOA_M': {
            'EDAD': EDAD_3A5,
            'SEXO': ['M'],
            'ASISTEN': ['No'],
        },
        'P6A11_NOA': {
            'EDAD': EDAD_6A11,
            'ASISTEN': ['No'],
        },
        'P6A11_NOAF': {
            'EDAD': EDAD_6A11,
            'SEXO': ['F'],
            'ASISTEN': ['No'],
        },
        'P6A11_NOAM': {
            'EDAD': EDAD_6A11,
            'SEXO': ['M'],
            'ASISTEN': ['No'],
        },
        'P12A14NOA': {
            'EDAD': EDAD_12A14,
            'ASISTEN': ['No'],
        },
        'P12A14NOAF': {
            'EDAD': EDAD_12A14,
            'SEXO': ['F'],
            'ASISTEN': ['No'],
        },
        'P12A14NOAM': {
            'EDAD': EDAD_12A14,
            'SEXO': ['M'],
            'ASISTEN': ['No'],
        },
        'P15A17A': {
            'EDAD': EDAD_15A17,
            'ASISTEN': ['Sí'],
        },
        'P15A17A_F': {
            'EDAD': EDAD_15A17,
            'SEXO': ['F'],
            'ASISTEN': ['Sí'],
        },
        'P15A17A_M': {
            'EDAD': EDAD_15A17,
            'SEXO': ['M'],
            'ASISTEN': ['Sí'],
        },
        'P18A24A': {
            'EDAD': EDAD_18A24,
            'ASISTEN': ['Sí'],
        },
        'P18A24A_F': {
            'EDAD': EDAD_18A24,
            'SEXO': ['F'],
            'ASISTEN': ['Sí'],
        },
        'P18A24A_M': {
            'EDAD': EDAD_18A24,
            'SEXO': ['M'],
            'ASISTEN': ['Sí'],
        },
        # Implicit
        'P3A5_A_NE_BPP_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_3A5,
            'ASISTEN': ['Sí', 'No especificado']
        },
        'P6A11_A_NE_BPP_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_6A11,
            'ASISTEN': ['Sí', 'No especificado']
        },
        'P12A14_A_NE_BPP_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_12A14,
            'ASISTEN': ['Sí', 'No especificado']
        },
        'P3A5_A_NE_BPP_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_3A5,
            'ASISTEN': ['Sí', 'No especificado']
        },
        'P6A11_A_NE_BPP_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_6A11,
            'ASISTEN': ['Sí', 'No especificado']
        },
        'P12A14_A_NE_BPP_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_12A14,
            'ASISTEN': ['Sí', 'No especificado']
        },
        'P15A17_NOA_NE_BPP_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_15A17,
            'ASISTEN': ['No', 'No especificado'],
        },
        'P18A24_NOA_NE_BPP_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_18A24,
            'ASISTEN': ['No', 'No especificado'],
        },
        'P15A17_NOA_NE_BPP_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_15A17,
            'ASISTEN': ['No', 'No especificado'],
        },
        'P18A24_NOA_NE_BPP_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_18A24,
            'ASISTEN': ['No', 'No especificado'],
        },

        'P8A14AN': {
            'EDAD': EDAD_8A14,
            'ALFABET': ['No'],
        },
        'P8A14AN_F': {
            'EDAD': EDAD_8A14,
            'SEXO': ['F'],
            'ALFABET': ['No'],
        },
        'P8A14AN_M': {
            'EDAD': EDAD_8A14,
            'SEXO': ['M'],
            'ALFABET': ['No'],
        },
        'P15YM_AN': {
            'EDAD': EDAD_15YMAS,
            'ALFABET': ['No'],
        },
        'P15YM_AN_F': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['F'],
            'ALFABET': ['No'],
        },
        'P15YM_AN_M': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['M'],
            'ALFABET': ['No'],
        },
        # Implicit
        'P8A14AS_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_8A14,
            'ALFABET': ['Sí', 'No especificado'],
        },
        'P8A14AS_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_8A14,
            'ALFABET': ['Sí', 'No especificado'],
        },
        'P15YM_AS_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_15YMAS,
            'ALFABET': ['Sí', 'No especificado'],
        },
        'P15YM_AS_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_15YMAS,
            'ALFABET': ['Sí', 'No especificado'],
        },

        'P15YM_SE': {
            'EDAD': EDAD_15YMAS,
            'NIVACAD': [
                'Sin Educación',
                # 'Ninguno',
                # 'Preescolar_1', 'Preescolar_2', 'Preescolar_3',
                # 'Preescolar_99',
            ],
        },
        'P15YM_SE_F': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['F'],
            'NIVACAD': [
                'Sin Educación',
                # 'Ninguno',
                # 'Preescolar_1', 'Preescolar_2', 'Preescolar_3',
                # 'Preescolar_99',
            ],
        },
        'P15YM_SE_M': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['M'],
            'NIVACAD': [
                'Sin Educación',
                # 'Ninguno',
                # 'Preescolar_1', 'Preescolar_2', 'Preescolar_3',
                # 'Preescolar_99',
            ],
        },
        'P15PRI_IN': {
            'EDAD': EDAD_15YMAS,
            'NIVACAD': [
                'Primaria_incom',
                # 'Primaria_1', 'Primaria_2', 'Primaria_3',
                # 'Primaria_4',  'Primaria_5', 'Primaria_99'
            ],
        },
        'P15PRI_INF': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['F'],
            'NIVACAD': [
                'Primaria_incom',
                # 'Primaria_1', 'Primaria_2', 'Primaria_3',
                # 'Primaria_4',  'Primaria_5', 'Primaria_99'
            ],
        },
        'P15PRI_INM': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['M'],
            'NIVACAD': [
                'Primaria_incom',
                # 'Primaria_1', 'Primaria_2', 'Primaria_3',
                # 'Primaria_4',  'Primaria_5', 'Primaria_99'
            ],
        },
        'P15PRI_CO': {
            'EDAD': EDAD_15YMAS,
            'NIVACAD': [
                'Primaria_com',
                'EToC_prim',
                # 'Primaria_6',
                # 'Estudios técnicos o comerciales con primaria terminada_1',
                # 'Estudios técnicos o comerciales con primaria terminada_2',
                # 'Estudios técnicos o comerciales con primaria terminada_3',
                # 'Estudios técnicos o comerciales con primaria terminada_4',
                # 'Estudios técnicos o comerciales con primaria terminada_99'
            ],
        },
        'P15PRI_COF': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['F'],
            'NIVACAD': [
                'Primaria_com',
                'EToC_prim',
                # 'Primaria_6',
                # 'Estudios técnicos o comerciales con primaria terminada_1',
                # 'Estudios técnicos o comerciales con primaria terminada_2',
                # 'Estudios técnicos o comerciales con primaria terminada_3',
                # 'Estudios técnicos o comerciales con primaria terminada_4',
                # 'Estudios técnicos o comerciales con primaria terminada_99'
            ],
        },
        'P15PRI_COM': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['M'],
            'NIVACAD': [
                'Primaria_com',
                'EToC_prim',
                # 'Primaria_6',
                # 'Estudios técnicos o comerciales con primaria terminada_1',
                # 'Estudios técnicos o comerciales con primaria terminada_2',
                # 'Estudios técnicos o comerciales con primaria terminada_3',
                # 'Estudios técnicos o comerciales con primaria terminada_4',
                # 'Estudios técnicos o comerciales con primaria terminada_99'
            ],
        },
        'P15SEC_IN': {
            'EDAD': EDAD_15YMAS,
            'NIVACAD': [
                'Secundaria_incom',
                # 'Secundaria_1', 'Secundaria_2', 'Secundaria_99'
            ],
        },
        'P15SEC_INF': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['F'],
            'NIVACAD': [
                'Secundaria_incom',
                # 'Secundaria_1', 'Secundaria_2', 'Secundaria_99'
            ],
        },
        'P15SEC_INM': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['M'],
            'NIVACAD': [
                'Secundaria_incom',
                # 'Secundaria_1', 'Secundaria_2', 'Secundaria_99'
            ],
        },
        'P15SEC_CO': {
            'EDAD': EDAD_15YMAS,
            'NIVACAD': [
                'Secundaria_com',
                # 'Secundaria_3'
            ],
        },
        'P15SEC_COF': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['F'],
            'NIVACAD': [
                'Secundaria_com',
                # 'Secundaria_3'
            ],
        },
        'P15SEC_COM': {
            'EDAD': EDAD_15YMAS,
            'SEXO': ['M'],
            'NIVACAD': [
                'Secundaria_com',
                # 'Secundaria_3'
            ],
        },
        'P18YM_PB': {
            'EDAD': EDAD_18YMAS,
            'NIVACAD': NIVACAD_POSBAS,
        },
        'P18YM_PB_F': {
            'EDAD': EDAD_18YMAS,
            'SEXO': ['F'],
            'NIVACAD': NIVACAD_POSBAS,
        },
        'P18YM_PB_M': {
            'EDAD': EDAD_18YMAS,
            'SEXO': ['M'],
            'NIVACAD': NIVACAD_POSBAS,
        },
        # Implicit
        'P15_POSBAS_BPP_NE_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_15YMAS,
            'NIVACAD': NIVACAD_POSBAS + ['No especificado'],
        },
        'P15_POSBAS_BPP_NE_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_15YMAS,
            'NIVACAD': NIVACAD_POSBAS + ['No especificado'],
        },
        'P18_BAS_BPP_NE_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_18YMAS,
            'NIVACAD': NIVACAD_BAS + ['No especificado'],
        },
        'P18_BAS_BPP_NE_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_18YMAS,
            'NIVACAD': NIVACAD_BAS + ['No especificado'],
        },

        # ECONOMICS
        'PEA': {
            'EDAD': EDAD_12YMAS,
            'CONACT': [
                'Trabaja',
                # 'Trabajó',
                # 'Declara que busca trabajo /  se rescata que trabaja',
                # 'Declara jubilado o pensionado / se rescata que trabaja',
                # 'Declara estudiante / se rescata que trabaja',
                # 'Se dedica a los quehaceres del hogar / se rescata que trabaja',
                # 'Declara que tiene limitaciónes / se rescata que trabaja',
                # 'Declara otra situación de actividad / se rescata que trabaja',
                # 'No se tiene información / se rescata que trabaja',
                # 'Tenía trabajo pero no trabajó',
                'Buscó trabajo',
            ],
        },
        'PEA_F': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['F'],
            'CONACT': [
                'Trabaja',
                # 'Trabajó',
                # 'Declara que busca trabajo /  se rescata que trabaja',
                # 'Declara jubilado o pensionado / se rescata que trabaja',
                # 'Declara estudiante / se rescata que trabaja',
                # 'Se dedica a los quehaceres del hogar / se rescata que trabaja',
                # 'Declara que tiene limitaciónes / se rescata que trabaja',
                # 'Declara otra situación de actividad / se rescata que trabaja',
                # 'No se tiene información / se rescata que trabaja',
                # 'Tenía trabajo pero no trabajó',
                'Buscó trabajo',
            ],
        },
        'PEA_M': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['M'],
            'CONACT': [
                'Trabaja',
                # 'Trabajó',
                # 'Declara que busca trabajo /  se rescata que trabaja',
                # 'Declara jubilado o pensionado / se rescata que trabaja',
                # 'Declara estudiante / se rescata que trabaja',
                # 'Se dedica a los quehaceres del hogar / se rescata que trabaja',
                # 'Declara que tiene limitaciónes / se rescata que trabaja',
                # 'Declara otra situación de actividad / se rescata que trabaja',
                # 'No se tiene información / se rescata que trabaja',
                # 'Tenía trabajo pero no trabajó',
                'Buscó trabajo',
            ],
        },
        'PE_INAC': {
            'EDAD': EDAD_12YMAS,
            'CONACT': [
                # 'Es pensionada(o) o jubilada(o)',
                # 'Es estudiante',
                # 'Se dedica a los quehaceres del hogar',
                # 'Está incapacitado permanentemente para trabajar',
                'No trabaja',
            ],
        },
        'PE_INAC_F': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['F'],
            'CONACT': [
                # 'Es pensionada(o) o jubilada(o)',
                # 'Es estudiante',
                # 'Se dedica a los quehaceres del hogar',
                # 'Está incapacitado permanentemente para trabajar',
                'No trabaja',
            ],
        },
        'PE_INAC_M': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['M'],
            'CONACT': [
                # 'Es pensionada(o) o jubilada(o)',
                # 'Es estudiante',
                # 'Se dedica a los quehaceres del hogar',
                # 'Está incapacitado permanentemente para trabajar',
                'No trabaja',
            ],
        },
        'POCUPADA': {
            'EDAD': EDAD_12YMAS,
            'CONACT': [
                'Trabaja',
                # 'Trabajó',
                # 'Declara que busca trabajo /  se rescata que trabaja',
                # 'Declara jubilado o pensionado / se rescata que trabaja',
                # 'Declara estudiante / se rescata que trabaja',
                # 'Se dedica a los quehaceres del hogar / se rescata que trabaja',
                # 'Declara que tiene limitaciónes / se rescata que trabaja',
                # 'Declara otra situación de actividad / se rescata que trabaja',
                # 'No se tiene información / se rescata que trabaja',
                # 'Tenía trabajo pero no trabajó',
            ],
        },
        'POCUPADA_F': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['F'],
            'CONACT': [
                'Trabaja',
                # 'Trabajó',
                # 'Declara que busca trabajo /  se rescata que trabaja',
                # 'Declara jubilado o pensionado / se rescata que trabaja',
                # 'Declara estudiante / se rescata que trabaja',
                # 'Se dedica a los quehaceres del hogar / se rescata que trabaja',
                # 'Declara que tiene limitaciónes / se rescata que trabaja',
                # 'Declara otra situación de actividad / se rescata que trabaja',
                # 'No se tiene información / se rescata que trabaja',
                # 'Tenía trabajo pero no trabajó',
            ],
        },
        'POCUPADA_M': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['M'],
            'CONACT': [
                'Trabaja',
                # 'Trabajó',
                # 'Declara que busca trabajo /  se rescata que trabaja',
                # 'Declara jubilado o pensionado / se rescata que trabaja',
                # 'Declara estudiante / se rescata que trabaja',
                # 'Se dedica a los quehaceres del hogar / se rescata que trabaja',
                # 'Declara que tiene limitaciónes / se rescata que trabaja',
                # 'Declara otra situación de actividad / se rescata que trabaja',
                # 'No se tiene información / se rescata que trabaja',
                # 'Tenía trabajo pero no trabajó',
            ],
        },
        'PDESOCUP': {
            'EDAD': EDAD_12YMAS,
            'CONACT': [
                'Buscó trabajo',
            ],
        },
        'PDESOCUP_F': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['F'],
            'CONACT': [
                'Buscó trabajo',
            ],
        },
        'PDESOCUP_M': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['M'],
            'CONACT': [
                'Buscó trabajo',
            ],
        },
        # Implicit
        'PE_BPP_NE_F': {
            'SEXO': ['F'],
            'EDAD': EDAD_12YMAS,
            'CONACT': ['No especificado'],
        },
        'PE_BPP_NE_M': {
            'SEXO': ['M'],
            'EDAD': EDAD_12YMAS,
            'CONACT': ['No especificado'],
        },

        # HEALTH
        'PSINDER': {
            'DHSERSAL': [c for c in DHSERSAL_CATS if c[8] == '1']
        },
        'PDER_SS': {
            'DHSERSAL': [
                c for c in DHSERSAL_CATS
                if sum(int(cc) for cc in c[:8]) > 0
            ]
        },
        # Implicit
        'PDER_NE': {
            'DHSERSAL': ['0000000001']
        },
        'PDER_IMSS': {
            'DHSERSAL': [c for c in DHSERSAL_CATS if c[0] == '1']
        },
        'PDER_ISTE': {
            'DHSERSAL': [c for c in DHSERSAL_CATS if c[1] == '1']
        },
        'PDER_ISTEE': {
            'DHSERSAL': [c for c in DHSERSAL_CATS if c[2] == '1']
        },
        'PAFIL_PDOM': {
            'DHSERSAL': [c for c in DHSERSAL_CATS if c[3] == '1']
        },
        'PDER_SEGP': {
            'DHSERSAL': [c for c in DHSERSAL_CATS if c[4] == '1']
        },
        'PDER_IMSSB': {
            'DHSERSAL': [c for c in DHSERSAL_CATS if c[5] == '1']
        },
        'PAFIL_IPRIV': {
            'DHSERSAL': [c for c in DHSERSAL_CATS if c[6] == '1']
        },
        'PAFIL_OTRAI': {
            'DHSERSAL': [c for c in DHSERSAL_CATS if c[7] == '1']
        },

        # MARTIAL
        'P12YM_SOLT': {
            'EDAD': EDAD_12YMAS,
            'SITUA_CONYUGAL': ['soltera(o)'],
        },
        'P12YM_CASA': {
            'EDAD': EDAD_12YMAS,
            'SITUA_CONYUGAL': [
                'unión libre',
                'casada(o) sólo por el civil',
                'casada(o) sólo religiosamente',
                'casada(o) civil y religiosamente',
            ],
        },
        'P12YM_SEPA': {
            'EDAD': EDAD_12YMAS,
            'SITUA_CONYUGAL': [
                'separada(o)',
                'divorciada(o)',
                'viuda(o)',
            ],
        },
        # Implicit
        'P12YM_BPP_NE': {
            'EDAD': EDAD_12YMAS,
            'SITUA_CONYUGAL': ['No especificado'],
        },

        # RELIGION
        'PCATOLICA': {
            'RELIGION': ['Católica'],
        },
        'PRO_CRIEVA': {
            'RELIGION': ['Protestante/cristiano evangélico'],
        },
        'POTRAS_REL': {
            'RELIGION': ['Otros credos'],
        },
        'PSIN_RELIG': {
            'RELIGION': ['Sin religión / Sin adscripción religiosa'],
        },
        # Implicit
        'PRELIG_NE': {
            'RELIGION': ['Religión no especificada']
        },
    }

    return constraints_ind


def get_viv_const():

    constraints_viv = {
        # Not used since they inclued abandoned houses
        # VIVTOT, includes collective, temporal and abandoned
        # TVIVHAB, includes collective
        # TVIVPAR, includes abandoned and temporal
        # VIVPARHAB, excludes houses with no resident info

        # HOUSEHOLS LEVEL CONSTRAINTS
        # Apply to all particular dwellings TOTHOG/TVIVPARHAB

        'TOTHOG': {},  # Same as TVIVPARHAB

        # TODO: consider this constraints after splitting POBTOT and adding
        # collective people class by duplicating person database.
        # Include here total collective dwellings.
        # 'POBHOG': {},  # Conflicts with POBTOT since POBTOT = POBHOG + POBCOL
        # Sames as OCUPVIVPAR
        # 'PHOGJEF_F': {},
        # 'PHOGJEF_M': {},

        'HOGJEF_F': {
            'JEFE_SEXO': ['F']
        },

        'HOGJEF_M': {
            'JEFE_SEXO': ['M']
        },

        # DWELLING LEVEL CONSTRAINTA
        # The following only apply to a subset of particular dwellings
        # the one with characteristics VIVPARH_CV

        'VPH_PISODT': {
            'PISOS': [
                'No Tierra',
                # 'Cemento o firme', 'Madera, mosaico u otro recubrimiento'
            ]
        },

        'VPH_PISOTI': {
            'PISOS': ['Tierra']
        },

        # IMPLICIT
        'VPH_PISONE': {
            'PISOS': ['Blanco por pase', 'No especificado']
        },

        'VPH_1DOR': {
            'CUADORM': [1]
        },

        'VPH_2YMASD': {
            'CUADORM': ['2+']  # list(range(2, 26))
        },

        # IMPLICIT
        'VPH_NEDOR': {
            'CUADORM': ['No especificado', 'Blanco por pase']
        },

        'VPH_1CUART': {
            'TOTCUART': [1]
        },

        'VPH_2CUART': {
            'TOTCUART': [2]
        },

        'VPH_3YMASC': {
            'TOTCUART': ['3+']  # list(range(3, 26))
        },

        # IMPLICIT
        'VPH_NECUART': {
            'TOTCUART': ['No especificado', 'Blanco por pase']
        },

        'VPH_C_ELEC': {
            'ELECTRICIDAD': ['Sí']
        },

        'VPH_S_ELEC': {
            'ELECTRICIDAD': ['No']
        },

        # IMPLICIT
        'VPH_NE_ELEC': {
            'ELECTRICIDAD': ['No especificado', 'Blanco por pase']
        },

        'VPH_AGUADV': {
            'AGUA_ENTUBADA': [
                'Tienen agua entubada.',
                # 'Dentro de la vivienda.',
                # 'Sólo en el patio o terreno.'
            ]
        },

        'VPH_AGUAFV': {
            'AGUA_ENTUBADA': [
                'No tienen agua entubada.',
            ]
        },

        # IMPLICIT
        'VPH_AGUANE': {
            'AGUA_ENTUBADA': ['No especificado', 'Blanco por pase']
        },

        'VPH_AEASP': {
            'AGUA_ENTUBADA': [
                'Tienen agua entubada.',
                # 'Dentro de la vivienda.',
                # 'Sólo en el patio o terreno.'
            ],
            'ABA_AGUA_ENTU': ['Del servicio público de agua.']
        },

        # IMPLICIT
        'VPH_AENSP': {
            'AGUA_ENTUBADA': [
                'Tienen agua entubada.',
                # 'Dentro de la vivienda.',
                # 'Sólo en el patio o terreno.'
            ],
            'ABA_AGUA_ENTU': [
                # 'De un pozo comunitario.',
                # 'De un pozo particular.',
                # 'De una pipa.',
                # 'De otra vivienda.',
                # 'De la lluvia.',
                'De otro lugar.',
                'No especificado',
                'Blanco por pase'
            ]
        },

        'VPH_TINACO': {
            'TINACO': ['Sí']
        },

        # IMPLICIT
        'VPH_TINACO_NO_NE': {
            'TINACO': ['No', 'No especificado', 'Blanco por pase']
        },

        'VPH_CISTER': {
            'CISTERNA': ['Sí']
        },

        # IMPLICIT
        'VPH_CISTER_NO_NE': {
            'CISTERNA': ['No', 'No especificado', 'Blanco por pase']
        },

        'VPH_EXCSA': {
            'SERSAN': ['Taza de baño (excusado o sanitario).']
        },

        'VPH_LETR': {
            'SERSAN': ['Letrina (pozo u hoyo).']
        },

        # IMPLICIT
        'VPH_NO_EXCSA': {
            'SERSAN': [
                'No tienen taza de baño ni letrina.',
                'No especificado',
                'Blanco por pase']
        },

        'VPH_DRENAJ': {
            'DRENAJE': [
                'Tiene drenaje.',
                # 'La red pública.',
                # 'Una fosa séptica o tanque séptico (biodigestor).',
                # 'Una tubería que va a dar a una barranca o grieta.',
                # 'Una tubería que va a dar a un río, lago o mar.',
            ]
        },

        'VPH_NODREN': {
            'DRENAJE': [
                'No tiene drenaje.',
            ]
        },

        'VPH_NEDREN': {
            'DRENAJE': [
                'No especificado', 'Blanco por pase',
            ]
        },

        'VPH_C_SERV': {
            'ELECTRICIDAD': ['Sí'],
            'AGUA_ENTUBADA': [
                'Tienen agua entubada.',
                # 'Dentro de la vivienda.',
                # 'Sólo en el patio o terreno.'
            ],
            'DRENAJE': [
                'Tiene drenaje.',
                # 'La red pública.',
                # 'Una fosa séptica o tanque séptico (biodigestor).',
                # 'Una tubería que va a dar a una barranca o grieta.',
                # 'Una tubería que va a dar a un río, lago o mar.',
            ]
        },

        'VPH_NDEAED': {
            'ELECTRICIDAD': ['No'],
            'AGUA_ENTUBADA': [
                'No tienen agua entubada.',
            ],
            'DRENAJE': [
                'No tiene drenaje.',
            ]
        },

        'VPH_DSADMA': {
            'DRENAJE': [
                'Tiene drenaje.',
                # 'La red pública.',
                # 'Una fosa séptica o tanque séptico (biodigestor).',
                # 'Una tubería que va a dar a una barranca o grieta.',
                # 'Una tubería que va a dar a un río, lago o mar.',
                    ],
            'SERSAN': [
                'Taza de baño (excusado o sanitario).',
                'Letrina (pozo u hoyo).'
            ],
            'CONAGUA': [
                'Con agua.',
                # 'Tiene descarga directa de agua.',
                # 'Le echan agua con cubeta.'
            ]
        },

        'VPH_NDACMM': {
            'AUTOPROP': ['No'],
            'MOTOCICLETA': ['No']
        },

        'VPH_SNBIEN': {
            'REFRIGERADOR': ['No'],
            'LAVADORA': ['No'],
            'HORNO': ['No'],
            'AUTOPROP': ['No'],
            'MOTOCICLETA': ['No'],
            'BICICLETA': ['No'],
            'RADIO': ['No'],
            'TELEVISOR': ['No'],
            'COMPUTADORA': ['No'],
            'INTERNET': ['No'],
            'TELEFONO': ['No'],
            'CELULAR': ['No'],
            'SERV_TV_PAGA': ['No'],
            'SERV_PEL_PAGA': ['No'],
            'CON_VJUEGOS': ['No']
        },

        'VPH_REFRI': {
            'REFRIGERADOR': ['Sí'],
        },
        # IMPLICIT
        'VPH_REFRI_NO': {
            'REFRIGERADOR': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_LAVAD': {
            'LAVADORA': ['Sí'],
        },
        'VPH_LAVAD_NO': {
            'LAVADORA': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_HMICRO': {
            'HORNO': ['Sí'],
        },
        'VPH_HMICRO_NO': {
            'HORNO': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_AUTOM': {
            'AUTOPROP': ['Sí'],
        },
        'VPH_AUTOM_NO': {
            'AUTOPROP': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_MOTO': {
            'MOTOCICLETA': ['Sí'],
        },
        'VPH_MOTO_NO': {
            'MOTOCICLETA': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_BICI': {
            'BICICLETA': ['Sí'],
        },
        'VPH_BICI_NO': {
            'BICICLETA': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_RADIO': {
            'RADIO': ['Sí'],
        },
        'VPH_RADIO_NO': {
            'RADIO': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_TV': {
            'TELEVISOR': ['Sí'],
        },
        'VPH_TV_NO': {
            'TELEVISOR': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_PC': {
            'COMPUTADORA': ['Sí'],
        },
        'VPH_PC_NO': {
            'COMPUTADORA': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_TELEF': {
            'TELEFONO': ['Sí'],
        },
        'VPH_TELEF_NO': {
            'TELEFONO': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_CEL': {
            'CELULAR': ['Sí'],
        },
        'VPH_CEL_NO': {
            'CELULAR': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_INTER': {
            'INTERNET': ['Sí'],
        },
        'VPH_INTER_NO': {
            'INTERNET': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_STVP': {
            'SERV_TV_PAGA': ['Sí'],
        },
        'VPH_STVP_NO': {
            'SERV_TV_PAGA': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_SPMVPI': {
            'SERV_PEL_PAGA': ['Sí'],
        },
        'VPH_SPMVPI_NO': {
            'SERV_PEL_PAGA': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_CVJ': {
            'CON_VJUEGOS': ['Sí'],
        },
        'VPH_CVJ_NO': {
            'CON_VJUEGOS': ['No', 'No especificado', 'Blanco por pase'],
        },

        'VPH_SINRTV': {
            'RADIO': ['No'],
            'TELEVISOR': ['No'],
        },

        'VPH_SINLTC': {
            'TELEFONO': ['No'],
            'CELULAR': ['No'],
        },

        'VPH_SINCINT': {
            'COMPUTADORA': ['No'],
            'INTERNET': ['No'],
        },

        'VPH_SINTIC': {
            'RADIO': ['No'],
            'TELEVISOR': ['No'],
            'COMPUTADORA': ['No'],
            'INTERNET': ['No'],
            'TELEFONO': ['No'],
            'CELULAR': ['No'],
            'SERV_TV_PAGA': ['No'],
            'SERV_PEL_PAGA': ['No'],
            'CON_VJUEGOS': ['No']
        },
    }

    return constraints_viv
