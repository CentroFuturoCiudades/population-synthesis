AGE = [
    '0-2', '3-4', '5', '6-7', '8-11', '12-14',
    '15-17', '18-24', '25-49', '50-59', '60-64',
    '65-130'
]
AGE_3YMAS = AGE[1:]
AGE_5YMAS = AGE[2:]
AGE_12YMAS = AGE[5:]
AGE_15YMAS = AGE[6:]
AGE_18YMAS = AGE[7:]
AGE_3A5 = AGE[1:3]
AGE_6A11 = AGE[3:5]
AGE_8A14 = AGE[4:6]
AGE_12A14 = AGE[5:6]
AGE_15A17 = AGE[6:7]
AGE_18A24 = AGE[7:8]
AGE_15A49 = AGE[6:9]
AGE_60YMAS = AGE[10:]
AGE_0A14 = AGE[:6]
AGE_15A64 = AGE[6:11]
AGE_65YMAS = AGE[11:]

AGE.append('Unknown')

dimensions_ind = {
    'SEX': ['M', 'F'],

    'AGE': AGE,

    # Migración # Crosstabulates AGE_5YMAS, SEXO
    'PLACE_BIRTH': ['EstaEnt', 'OtraEnt'],
    'PLACE_RES_2015': ['EstaEnt', 'OtraEnt'],

    # Etnicidad
    'SPEAKS_NATIVE': ['Yes', 'No'],  # CT with AGE_3YMAS, AGE_5YMAS, SEXO
    'SPEAKS_SPANISH': ['Yes', 'No'],  # CT with AGE_3YMAS, AGE_5YMAS, SEXO
    'IS_AFRO': ['Yes', 'No'],  # CT with SEXO

    # Discapacidad # Does not CT
    'DISC_MOT': ['DISC', 'LIM', 'No'],
    'DISC_VIS': ['DISC', 'LIM', 'No'],
    'DISC_LENG': ['DISC', 'LIM', 'No'],
    'DISC_AUD': ['DISC', 'LIM', 'No'],
    'DISC_MOT2': ['DSIC', 'LIM', 'No'],
    'DISC_MEN': ['DISC', 'LIM', 'No'],
    'DISC_MEN2': ['Yes', 'No'],

    # Educacion # CT with AGE and SEX
    'STUDENT': ['Yes', 'No'],
    'CAN_READ_WRITE': ['Yes', 'No'],
    'EDU_LEVEL': ['Ninguno/Preescolar', '5Primaria', '6Primaria',
                  '2Secundaria', '3Secundaria', 'Posbasica'],

    # Características económicas CT with AGE and SEX
    # Census distinguishes between economically active
    # and econmically busy people
    # Active means they are employed or unemployed but looking for a job
    # Busy means they are employed and not busy searching for a job.
    # So empliyed people are BUSY: Yes, and unemploye people are ACTIVE: No
    'EMPLOYED': ['Yes', 'Searching', 'No'],

    # Salud Does not CT
    # The first constraint can be modelled using chaining on the
    # condition of at least one affiliation
    'SS_AFFILIATED': ['Yes', 'No'],
    'SS_IMSS': ['Yes', 'No'],
    'SS_ISTE': ['Yes', 'No'],
    'SS_ISTEE': ['Yes', 'No'],
    'SS_PDOM': ['Yes', 'No'],
    'SS_SEGP': ['Yes', 'No'],
    'SS_IMSSB': ['Yes', 'No'],
    'SS_PRIV': ['Yes', 'No'],
    'SS_OTHER': ['Yes', 'No'],

    # Conyugal CT AGE and SEX
    'MARITAL_STATUS': ['Single', 'Paired', 'Split'],

    # Religion Does no CT
    'RELIGION': ['Catolic', 'Crieva', 'Other', 'Without'],

    # Viviendas
    'VIV_TYPE': ['Particular', 'Colectiva', 'Sin'],

    # Hogares Censales TODO
    'CENSAL_HOUSEHOLD': ['Yes', 'No'],
    'NATIVE_HOUSEHOLD': ['Yes', 'No'],
}


dim_viv = {
    'HAB': ['Yes', 'No', 'Uso_temp'],
    'TYPE': ['Particular', 'Colectiva'],
    'HAS_INFO': ['Yes', 'No'],
    'HAS_CHARS': ['Yes', 'No'],

    'NUM_ROOMS': ['1', '2', '3YMAS'],
    'NUM_BEDROOMS': ['1', '2YMAS'],
    'FLOOR': ['Dirt', 'Other'],

    'HAS_ELEC': ['Yes', 'No'],
}
