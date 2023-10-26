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

        # 'P_15A49_F': {
        #     'EDAD': EDAD_15A49,
        #     'SEXO': ['F']
        # },

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

        # 'POB0_14': {
        #     'EDAD': EDAD_0A14
        # },

        # 'POB15_64': {
        #     'EDAD': EDAD_15A64
        # },

        # 'POB65_MAS': {
        #     'EDAD': EDAD_65YMAS
        # },

        # MIGRATION
        # 'PNACENT': {
        #     'ENT_PAIS_NAC': ['EstaEnt'],
        # },
        # 'PNACENT_F': {
        #     'SEXO': ['F'],
        #     'ENT_PAIS_NAC': ['EstaEnt'],
        # },
        # 'PNACENT_M': {
        #     'SEXO': ['M'],
        #     'ENT_PAIS_NAC': ['EstaEnt'],
        # },
        # 'PNACOE': {
        #     'ENT_PAIS_NAC': ['OtraEnt'],
        # },
        # 'PNACOE_F': {
        #     'SEXO': ['F'],
        #     'ENT_PAIS_NAC': ['OtraEnt'],
        # },
        # 'PNACOE_M': {
        #     'SEXO': ['M'],
        #     'ENT_PAIS_NAC': ['OtraEnt'],
        # },

        # 'PRES2015': {
        #     'EDAD': EDAD_5YMAS,
        #     'ENT_PAIS_RES_5A': ['EstaEnt'],
        # },
        # 'PRES2015_F': {
        #     'SEXO': ['F'],
        #     'EDAD': EDAD_5YMAS,
        #     'ENT_PAIS_RES_5A': ['EstaEnt'],
        # },
        # 'PRES2015_M': {
        #     'SEXO': ['M'],
        #     'EDAD': EDAD_5YMAS,
        #     'ENT_PAIS_RES_5A': ['EstaEnt'],
        # },
        # 'PRESOE15': {
        #     'EDAD': EDAD_5YMAS,
        #     'ENT_PAIS_RES_5A': ['OtraEnt'],
        # },
        # 'PRESOE15_F': {
        #     'SEXO': ['F'],
        #     'EDAD': EDAD_5YMAS,
        #     'ENT_PAIS_RES_5A': ['OtraEnt'],
        # },
        # 'PRESOE15_M': {
        #     'SEXO': ['M'],
        #     'EDAD': EDAD_5YMAS,
        #     'ENT_PAIS_RES_5A': ['OtraEnt'],
        # },

        # ETNICITY
        # 'P3YM_HLI': {
        #     'EDAD': EDAD_3YMAS,
        #     'HLENGUA': ['Sí']
        # },
        # 'P3YM_HLI_F': {
        #     'SEXO': ['F'],
        #     'EDAD': EDAD_3YMAS,
        #     'HLENGUA': ['Sí']
        # },
        # 'P3YM_HLI_M': {
        #     'SEXO': ['M'],
        #     'EDAD': EDAD_3YMAS,
        #     'HLENGUA': ['Sí']
        # },

        # 'P3HLINHE': {
        #     'EDAD': EDAD_3YMAS,
        #     'HLENGUA': ['Sí'],
        #     'HESPANOL': ['No']
        # },
        # 'P3HLINHE_F': {
        #     'SEXO': ['F'],
        #     'EDAD': EDAD_3YMAS,
        #     'HLENGUA': ['Sí'],
        #     'HESPANOL': ['No'],
        # },
        # 'P3HLINHE_M': {
        #     'SEXO': ['M'],
        #     'EDAD': EDAD_3YMAS,
        #     'HLENGUA': ['Sí'],
        #     'HESPANOL': ['No'],
        # },
        # 'P3HLI_HE': {
        #     'EDAD': EDAD_3YMAS,
        #     'HLENGUA': ['Sí'],
        #     'HESPANOL': ['Sí']
        # },
        # 'P3HLI_HE_F': {
        #     'SEXO': ['F'],
        #     'EDAD': EDAD_3YMAS,
        #     'HLENGUA': ['Sí'],
        #     'HESPANOL': ['Sí']
        # },
        # 'P3HLI_HE_M': {
        #     'SEXO': ['M'],
        #     'EDAD': EDAD_3YMAS,
        #     'HLENGUA': ['Sí'],
        #     'HESPANOL': ['Sí']
        # },

        # 'P5_HLI': {
        #     'EDAD': EDAD_5YMAS,
        #     'HLENGUA': ['Sí'],
        # },
        # 'P5_HLI_NHE': {
        #     'EDAD': EDAD_5YMAS,
        #     'HLENGUA': ['Sí'],
        #     'HESPANOL': ['No'],
        # },
        # 'P5_HLI_HE': {
        #     'EDAD': EDAD_5YMAS,
        #     'HLENGUA': ['Sí'],
        #     'HESPANOL': ['Sí'],
        # },

        # 'P34HLI': {
        #     'EDAD': ['3-4'],
        #     'HLENGUA': ['Sí']
        # },
        # 'P34HLI_HE': {
        #     'EDAD': ['3-4'],
        #     'HLENGUA': ['Sí'],
        #     'HESPANOL': ['Sí'],
        # },
        # 'P34HLI_NHE': {
        #     'EDAD': ['3-4'],
        #     'HLENGUA': ['Sí'],
        #     'HESPANOL': ['No'],
        # },

        # 'POB_AFRO': {
        #     'AFRODES': ['Sí'],
        # },
        # 'POB_AFRO_F': {
        #     'SEXO': ['F'],
        #     'AFRODES': ['Sí'],
        # },
        # 'POB_AFRO_M': {
        #     'SEXO': ['M'],
        #     'AFRODES': ['Sí'],
        # },

        # DISABILITY
        # 'PCON_DISC': {
        #     'DIS_CON': ['Sí']
        # },
        # 'PCDISC_MOT': {
        #     'DIS_CAMINAR': ['Lo hace con mucha dificultad', 'No puede hacerlo'],
        # },
        # 'PCDISC_VIS': {
        #     'DIS_VER': ['Lo hace con mucha dificultad', 'No puede hacerlo'],
        # },
        # 'PCDISC_LENG': {
        #     'DIS_HABLAR': ['Lo hace con mucha dificultad', 'No puede hacerlo'],
        # },
        # 'PCDISC_AUD': {
        #     'DIS_OIR': ['Lo hace con mucha dificultad', 'No puede hacerlo'],
        # },
        # 'PCDISC_MOT2': {
        #     'DIS_BANARSE': ['Lo hace con mucha dificultad', 'No puede hacerlo'],
        # },
        # 'PCDISC_MEN': {
        #     'DIS_RECORDAR': ['Lo hace con mucha dificultad', 'No puede hacerlo'],
        # },
        # 'PCON_LIMI': {
        #     'DIS_LIMI': ['Sí']
        # },
        # 'PCLIM_CSB': {
        #     'DIS_CAMINAR': ['Lo hace con poca dificultad'],
        # },
        # 'PCLIM_VIS': {
        #     'DIS_VER': ['Lo hace con poca dificultad'],
        # },
        # 'PCLIM_HACO': {
        #     'DIS_HABLAR': ['Lo hace con poca dificultad'],
        # },
        # 'PCLIM_OAUD': {
        #     'DIS_OIR': ['Lo hace con poca dificultad'],
        # },
        # 'PCLIM_MOT2': {
        #     'DIS_BANARSE': ['Lo hace con poca dificultad'],
        # },
        # 'PCLIM_RE_CO': {
        #     'DIS_RECORDAR': ['Lo hace con poca dificultad'],
        # },
        # 'PCLIM_PMEN': {
        #     'DIS_MENTAL': ['Sí'],
        # },
        # 'PSIND_LIM': {
        #     'DIS_VER': ['No tiene dificultad'],
        #     'DIS_OIR': ['No tiene dificultad'],
        #     'DIS_CAMINAR': ['No tiene dificultad'],
        #     'DIS_RECORDAR': ['No tiene dificultad'],
        #     'DIS_BANARSE': ['No tiene dificultad'],
        #     'DIS_HABLAR': ['No tiene dificultad'],
        #     'DIS_MENTAL': ['No'],
        # },

        # EDUCATION
        'P3A5_NOA': {
            'EDAD': EDAD_3A5,
            'ASISTEN': ['No'],
        },
        # 'P3A5_NOA_F': {
        #     'EDAD': EDAD_3A5,
        #     'SEXO': ['F'],
        #     'ASISTEN': ['No'],
        # },
        # 'P3A5_NOA_M': {
        #     'EDAD': EDAD_3A5,
        #     'SEXO': ['M'],
        #     'ASISTEN': ['No'],
        # },

        # 'P6A11_NOA': {
        #     'EDAD': EDAD_6A11,
        #     'ASISTEN': ['No'],
        # },
        # 'P6A11_NOAF': {
        #     'EDAD': EDAD_6A11,
        #     'SEXO': ['F'],
        #     'ASISTEN': ['No'],
        # },
        # 'P6A11_NOAM': {
        #     'EDAD': EDAD_6A11,
        #     'SEXO': ['M'],
        #     'ASISTEN': ['No'],
        # },
        # 'P12A14NOA': {
        #     'EDAD': EDAD_12A14,
        #     'ASISTEN': ['No'],
        # },
        # 'P12A14NOAF': {
        #     'EDAD': EDAD_12A14,
        #     'SEXO': ['F'],
        #     'ASISTEN': ['No'],
        # },
        # 'P12A14NOAM': {
        #     'EDAD': EDAD_12A14,
        #     'SEXO': ['M'],
        #     'ASISTEN': ['No'],
        # },

        'P6A14NOA': {
            'EDAD': EDAD_6A11 + EDAD_12A14,
            'ASISTEN': ['No'],
        },
        # 'P6A14NOAF': {
        #     'EDAD': EDAD_6A11 + EDAD_12A14,
        #     'SEXO': ['F'],
        #     'ASISTEN': ['No'],
        # },
        # 'P6A14NOAM': {
        #     'EDAD': EDAD_6A11 + EDAD_12A14,
        #     'SEXO': ['M'],
        #     'ASISTEN': ['No'],
        # },

        'P15A17A': {
            'EDAD': EDAD_15A17,
            'ASISTEN': ['Sí'],
        },
        # 'P15A17A_F': {
        #     'EDAD': EDAD_15A17,
        #     'SEXO': ['F'],
        #     'ASISTEN': ['Sí'],
        # },
        # 'P15A17A_M': {
        #     'EDAD': EDAD_15A17,
        #     'SEXO': ['M'],
        #     'ASISTEN': ['Sí'],
        # },
        'P18A24A': {
            'EDAD': EDAD_18A24,
            'ASISTEN': ['Sí'],
        },
        # 'P18A24A_F': {
        #     'EDAD': EDAD_18A24,
        #     'SEXO': ['F'],
        #     'ASISTEN': ['Sí'],
        # },
        # 'P18A24A_M': {
        #     'EDAD': EDAD_18A24,
        #     'SEXO': ['M'],
        #     'ASISTEN': ['Sí'],
        # },

        # 'P8A14AN': {
        #     'EDAD': EDAD_8A14,
        #     'ALFABET': ['No'],
        # },
        # 'P8A14AN_F': {
        #     'EDAD': EDAD_8A14,
        #     'SEXO': ['F'],
        #     'ALFABET': ['No'],
        # },
        # 'P8A14AN_M': {
        #     'EDAD': EDAD_8A14,
        #     'SEXO': ['M'],
        #     'ALFABET': ['No'],
        # },
        # 'P15YM_AN': {
        #     'EDAD': EDAD_15YMAS,
        #     'ALFABET': ['No'],
        # },
        # 'P15YM_AN_F': {
        #     'EDAD': EDAD_15YMAS,
        #     'SEXO': ['F'],
        #     'ALFABET': ['No'],
        # },
        # 'P15YM_AN_M': {
        #     'EDAD': EDAD_15YMAS,
        #     'SEXO': ['M'],
        #     'ALFABET': ['No'],
        # },
        # 'P8YM_AN': {
        #     'EDAD': EDAD_8A14 + EDAD_15YMAS,
        #     'ALFABET': ['No'],
        # },
        # 'P8YM_AN_F': {
        #     'EDAD': EDAD_8A14 + EDAD_15YMAS,
        #     'SEXO': ['F'],
        #     'ALFABET': ['No'],
        # },
        # 'P8YM_AN_M': {
        #     'EDAD': EDAD_8A14 + EDAD_15YMAS,
        #     'SEXO': ['M'],
        #     'ALFABET': ['No'],
        # },

        'P15YM_SE': {
            'EDAD': EDAD_15YMAS,
            'EDUC': ['Sin Educación'],
        },
        # 'P15YM_SE_F': {
        #     'EDAD': EDAD_15YMAS,
        #     'SEXO': ['F'],
        #     'EDUC': ['Sin Educación'],
        # },
        # 'P15YM_SE_M': {
        #     'EDAD': EDAD_15YMAS,
        #     'SEXO': ['M'],
        #     'EDUC': ['Sin Educación'],
        # },
        'P15PRI_IN': {
            'EDAD': EDAD_15YMAS,
            'EDUC': ['Primaria_incom'],
        },
        # 'P15PRI_INF': {
        #     'EDAD': EDAD_15YMAS,
        #     'SEXO': ['F'],
        #     'EDUC': ['Primaria_incom'],
        # },
        # 'P15PRI_INM': {
        #     'EDAD': EDAD_15YMAS,
        #     'SEXO': ['M'],
        #     'EDUC': ['Primaria_incom'],
        # },
        'P15PRI_CO': {
            'EDAD': EDAD_15YMAS,
            'EDUC': ['Primaria_com'],
        },
        # 'P15PRI_COF': {
        #     'EDAD': EDAD_15YMAS,
        #     'SEXO': ['F'],
        #     'EDUC': ['Primaria_com'],
        # },
        # 'P15PRI_COM': {
        #     'EDAD': EDAD_15YMAS,
        #     'SEXO': ['M'],
        #     'EDUC': ['Primaria_com'],
        # },
        'P15SEC_IN': {
            'EDAD': EDAD_15YMAS,
            'EDUC': ['Secundaria_incom'],
        },
        # 'P15SEC_INF': {
        #     'EDAD': EDAD_15YMAS,
        #     'SEXO': ['F'],
        #     'EDUC': ['Secundaria_incom'],
        # },
        # 'P15SEC_INM': {
        #     'EDAD': EDAD_15YMAS,
        #     'SEXO': ['M'],
        #     'EDUC': ['Secundaria_incom'],
        # },
        'P15SEC_CO': {
            'EDAD': EDAD_15YMAS,
            'EDUC': ['Secundaria_com'],
        },
        # 'P15SEC_COF': {
        #     'EDAD': EDAD_15YMAS,
        #     'SEXO': ['F'],
        #     'EDUC': ['Secundaria_com'],
        # },
        # 'P15SEC_COM': {
        #     'EDAD': EDAD_15YMAS,
        #     'SEXO': ['M'],
        #     'EDUC': ['Secundaria_com'],
        # },
        'P18YM_PB': {
            'EDAD': EDAD_18YMAS,
            'EDUC': ['Posbásica'],
        },
        # 'P18YM_PB_F': {
        #     'EDAD': EDAD_18YMAS,
        #     'SEXO': ['F'],
        #     'EDUC': ['Posbásica'],
        # },
        # 'P18YM_PB_M': {
        #     'EDAD': EDAD_18YMAS,
        #     'SEXO': ['M'],
        #     'EDUC': ['Posbásica'],
        # },

        # ECONOMICS
        # 'PEA': {
        #     'EDAD': EDAD_12YMAS,
        #     'CONACT': [
        #         'Trabaja',
        #         'Buscó trabajo',
        #     ],
        # },
        # 'PEA_F': {
        #     'EDAD': EDAD_12YMAS,
        #     'SEXO': ['F'],
        #     'CONACT': [
        #         'Trabaja',
        #         'Buscó trabajo',
        #     ],
        # },
        # 'PEA_M': {
        #     'EDAD': EDAD_12YMAS,
        #     'SEXO': ['M'],
        #     'CONACT': [
        #         'Trabaja',
        #         'Buscó trabajo',
        #     ],
        # },
        # 'PE_INAC': {
        #     'EDAD': EDAD_12YMAS,
        #     'CONACT': [
        #         'No trabaja',
        #     ],
        # },
        # 'PE_INAC_F': {
        #     'EDAD': EDAD_12YMAS,
        #     'SEXO': ['F'],
        #     'CONACT': [
        #         'No trabaja',
        #     ],
        # },
        # 'PE_INAC_M': {
        #     'EDAD': EDAD_12YMAS,
        #     'SEXO': ['M'],
        #     'CONACT': [
        #         'No trabaja',
        #     ],
        # },
        'POCUPADA': {
            'EDAD': EDAD_12YMAS,
            'CONACT': [
                'Trabaja',
            ],
        },
        'POCUPADA_F': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['F'],
            'CONACT': [
                'Trabaja',
            ],
        },
        'POCUPADA_M': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['M'],
            'CONACT': [
                'Trabaja',
            ],
        },
        'PNOCUPA': {
            'EDAD': EDAD_12YMAS,
            'CONACT': [
                'No trabaja',
            ],
        },
        'PNOCUPA_F': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['F'],
            'CONACT': [
                'No trabaja',
            ],
        },
        'PNOCUPA_M': {
            'EDAD': EDAD_12YMAS,
            'SEXO': ['M'],
            'CONACT': [
                'No trabaja',
            ],
        },
        # 'PDESOCUP': {
        #     'EDAD': EDAD_12YMAS,
        #     'CONACT': [
        #         'Buscó trabajo',
        #     ],
        # },
        # 'PDESOCUP_F': {
        #     'EDAD': EDAD_12YMAS,
        #     'SEXO': ['F'],
        #     'CONACT': [
        #         'Buscó trabajo',
        #     ],
        # },
        # 'PDESOCUP_M': {
        #     'EDAD': EDAD_12YMAS,
        #     'SEXO': ['M'],
        #     'CONACT': [
        #         'Buscó trabajo',
        #     ],
        # },

        # HEALTH
        # 'PSINDER': {
        #     'DHSERSAL_No afiliado': [1]
        # },
        # 'PDER_SS': {
        #     'DHSERSAL_AFIL': [1]
        # },
        # 'PDER_IMSS': {
        #     'DHSERSAL_IMSS': [1]
        # },
        # 'PDER_ISTE': {
        #     'DHSERSAL_ISSSTE': [1]
        # },
        # 'PDER_ISTEE': {
        #     'DHSERSAL_ISSSTE_E': [1]
        # },
        # 'PAFIL_PDOM': {
        #     'DHSERSAL_P_D_M': [1]
        # },
        # 'PDER_SEGP': {
        #     'DHSERSAL_Popular_NGenración_SBienestar': [1]
        # },
        # 'PDER_IMSSB': {
        #     'DHSERSAL_IMSS_Prospera/Bienestar': [1]
        # },
        # 'PAFIL_IPRIV': {
        #     'DHSERSAL_Privado': [1]
        # },
        # 'PAFIL_OTRAI': {
        #     'DHSERSAL_Otro': [1]
        # },
        # 'PAFIL_PUB': {
        #     'DHSERSAL_PUB': [1]
        # },


        # MARTIAL
        # 'P12YM_SOLT': {
        #     'EDAD': EDAD_12YMAS,
        #     'SITUA_CONYUGAL': ['soltero'],
        # },
        # 'P12YM_CASA': {
        #     'EDAD': EDAD_12YMAS,
        #     'SITUA_CONYUGAL': ['casado'],
        # },
        # 'P12YM_SEPA': {
        #     'EDAD': EDAD_12YMAS,
        #     'SITUA_CONYUGAL': ['separado'],
        # },

        # RELIGION
        # 'PCATOLICA': {
        #     'RELIGION': ['Católica'],
        # },
        # 'PRO_CRIEVA': {
        #     'RELIGION': ['Protestante/cristiano evangélico'],
        # },
        # 'POTRAS_REL': {
        #     'RELIGION': ['Otros credos'],
        # },
        # 'PSIN_RELIG': {
        #     'RELIGION': ['Sin religión / Sin adscripción religiosa'],
        # },
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

        # NOTE: While not controlling for collective, use
        # Change to TOTHOG later
        'TOTHOG': {
            'CLAVIVP': ['Vivienda', 'Otro']
        },  # Same as TVIVPARHAB

        # TODO: consider this constraints after splitting POBTOT and adding
        # collective people class by duplicating person database.
        # Include here total collective dwellings.
        # 'POBHOG': {sum(NUMPERS)},  # POBTOT = POBHOG + POBCOL
        # Can be taken into account implicitly by constraining POBCOL
        # Sames as OCUPVIVPAR
        # 'PHOGJEF_F': {sum(NUMPERS), JEFE_SEXO=F},
        # 'PHOGJEF_M': {sum(NUMPERS), JEFE_SEXO=M},
        # This constraints can be created manually

        # 'HOGJEF_F': {
        #     'JEFE_SEXO': ['F'],
        #     'CLAVIVP': ['Vivienda', 'Otro']
        # },

        # 'HOGJEF_M': {
        #     'JEFE_SEXO': ['M'],
        #     'CLAVIVP': ['Vivienda', 'Otro']
        # },

        # DWELLING LEVEL CONSTRAINTA
        # The following only apply to a subset of particular dwellings
        # the one with characteristics VIVPARH_CV

        # 'VPH_PISODT': {
        #     'CLAVIVP': ['Vivienda'],
        #     'PISOS': [
        #         'No tierra',
        #     ]
        # },

        # 'VPH_PISOTI': {
        #     'CLAVIVP': ['Vivienda'],
        #     'PISOS': ['Tierra']
        # },

        # 'VPH_1DOR': {
        #     'CLAVIVP': ['Vivienda'],
        #     'CUADORM': [1]
        # },

        # 'VPH_2YMASD': {
        #     'CLAVIVP': ['Vivienda'],
        #     'CUADORM': ['2+']
        # },

        # 'VPH_1CUART': {
        #     'CLAVIVP': ['Vivienda'],
        #     'TOTCUART': [1]
        # },

        # 'VPH_2CUART': {
        #     'CLAVIVP': ['Vivienda'],
        #     'TOTCUART': [2]
        # },

        # 'VPH_3YMASC': {
        #     'CLAVIVP': ['Vivienda'],
        #     'TOTCUART': ['3+']
        # },

        # 'VPH_C_ELEC': {
        #     'CLAVIVP': ['Vivienda'],
        #     'ELECTRICIDAD': ['Sí']
        # },

        # 'VPH_S_ELEC': {
        #     'CLAVIVP': ['Vivienda'],
        #     'ELECTRICIDAD': ['No']
        # },

        # 'VPH_AGUADV': {
        #     'CLAVIVP': ['Vivienda'],
        #     'AGUA_ENTUBADA': ['Tiene']
        # },

        # 'VPH_AGUAFV': {
        #     'CLAVIVP': ['Vivienda'],
        #     'AGUA_ENTUBADA': ['No tiene']
        # },

        # 'VPH_AEASP': {
        #     'CLAVIVP': ['Vivienda'],
        #     'AGUA_ENTUBADA': ['Tiene'],
        #     'ABA_AGUA_ENTU': ['Del servicio público de agua.']
        # },

        # 'VPH_TINACO': {
        #     'CLAVIVP': ['Vivienda'],
        #     'TINACO': ['Sí']
        # },

        # 'VPH_CISTER': {
        #     'CLAVIVP': ['Vivienda'],
        #     'CISTERNA': ['Sí']
        # },

        # 'VPH_EXCSA': {
        #     'CLAVIVP': ['Vivienda'],
        #     'SERSAN': ['Taza de baño (excusado o sanitario).']
        # },

        # 'VPH_LETR': {
        #     'CLAVIVP': ['Vivienda'],
        #     'SERSAN': ['Letrina (pozo u hoyo).']
        # },

        # 'VPH_DRENAJ': {
        #     'CLAVIVP': ['Vivienda'],
        #     'DRENAJE': ['Sí']
        # },

        # 'VPH_NODREN': {
        #     'CLAVIVP': ['Vivienda'],
        #     'DRENAJE': ['No']
        # },

        # 'VPH_C_SERV': {
        #     'CLAVIVP': ['Vivienda'],
        #     'ELECTRICIDAD': ['Sí'],
        #     'AGUA_ENTUBADA': ['Tiene'],
        #     'DRENAJE': ['Sí']
        # },

        # 'VPH_NDEAED': {
        #     'CLAVIVP': ['Vivienda'],
        #     'ELECTRICIDAD': ['No'],
        #     'AGUA_ENTUBADA': ['No tiene'],
        #     'DRENAJE': ['No']
        # },

        # 'VPH_DSADMA': {
        #     'CLAVIVP': ['Vivienda'],
        #     'DRENAJE': ['Sí'],
        #     'SERSAN': [
        #         'Taza de baño (excusado o sanitario).',
        #         'Letrina (pozo u hoyo).'
        #     ],
        #     'CONAGUA': ['Sí']
        # },

        'VPH_NDACMM': {
            'CLAVIVP': ['Vivienda'],
            'AUTOPROP': ['No'],
            'MOTOCICLETA': ['No']
        },

        # 'VPH_SNBIEN': {
        #     'CLAVIVP': ['Vivienda'],
        #     'REFRIGERADOR': ['No'],
        #     'LAVADORA': ['No'],
        #     'HORNO': ['No'],
        #     'AUTOPROP': ['No'],
        #     'MOTOCICLETA': ['No'],
        #     'BICICLETA': ['No'],
        #     'RADIO': ['No'],
        #     'TELEVISOR': ['No'],
        #     'COMPUTADORA': ['No'],
        #     'INTERNET': ['No'],
        #     'TELEFONO': ['No'],
        #     'CELULAR': ['No'],
        #     'SERV_TV_PAGA': ['No'],
        #     'SERV_PEL_PAGA': ['No'],
        #     'CON_VJUEGOS': ['No']
        # },

        # 'VPH_REFRI': {
        #     'CLAVIVP': ['Vivienda'],
        #     'REFRIGERADOR': ['Sí'],
        # },

        # 'VPH_LAVAD': {
        #     'CLAVIVP': ['Vivienda'],
        #     'LAVADORA': ['Sí'],
        # },

        # 'VPH_HMICRO': {
        #     'CLAVIVP': ['Vivienda'],
        #     'HORNO': ['Sí'],
        # },

        'VPH_AUTOM': {
            'CLAVIVP': ['Vivienda'],
            'AUTOPROP': ['Sí'],
        },

        'VPH_MOTO': {
            'CLAVIVP': ['Vivienda'],
            'MOTOCICLETA': ['Sí'],
        },

        'VPH_BICI': {
            'CLAVIVP': ['Vivienda'],
            'BICICLETA': ['Sí'],
        },

        # 'VPH_RADIO': {
        #     'CLAVIVP': ['Vivienda'],
        #     'RADIO': ['Sí'],
        # },

        # 'VPH_TV': {
        #     'CLAVIVP': ['Vivienda'],
        #     'TELEVISOR': ['Sí'],
        # },

        # 'VPH_PC': {
        #     'CLAVIVP': ['Vivienda'],
        #     'COMPUTADORA': ['Sí'],
        # },

        # 'VPH_TELEF': {
        #     'CLAVIVP': ['Vivienda'],
        #     'TELEFONO': ['Sí'],
        # },

        # 'VPH_CEL': {
        #     'CLAVIVP': ['Vivienda'],
        #     'CELULAR': ['Sí'],
        # },

        # 'VPH_INTER': {
        #     'CLAVIVP': ['Vivienda'],
        #     'INTERNET': ['Sí'],
        # },

        # 'VPH_STVP': {
        #     'CLAVIVP': ['Vivienda'],
        #     'SERV_TV_PAGA': ['Sí'],
        # },

        # 'VPH_SPMVPI': {
        #     'CLAVIVP': ['Vivienda'],
        #     'SERV_PEL_PAGA': ['Sí'],
        # },

        # 'VPH_CVJ': {
        #     'CLAVIVP': ['Vivienda'],
        #     'CON_VJUEGOS': ['Sí'],
        # },

        # 'VPH_SINRTV': {
        #     'CLAVIVP': ['Vivienda'],
        #     'RADIO': ['No'],
        #     'TELEVISOR': ['No'],
        # },

        # 'VPH_SINLTC': {
        #     'CLAVIVP': ['Vivienda'],
        #     'TELEFONO': ['No'],
        #     'CELULAR': ['No'],
        # },

        # 'VPH_SINCINT': {
        #     'CLAVIVP': ['Vivienda'],
        #     'COMPUTADORA': ['No'],
        #     'INTERNET': ['No'],
        # },

        # 'VPH_SINTIC': {
        #     'CLAVIVP': ['Vivienda'],
        #     'RADIO': ['No'],
        #     'TELEVISOR': ['No'],
        #     'COMPUTADORA': ['No'],
        #     'INTERNET': ['No'],
        #     'TELEFONO': ['No'],
        #     'CELULAR': ['No'],
        #     'SERV_TV_PAGA': ['No'],
        #     'SERV_PEL_PAGA': ['No'],
        #     'CON_VJUEGOS': ['No']
        # },
    }

    return constraints_viv
