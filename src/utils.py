from itertools import product
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import struct

def mtx2df (file:str):
	#header schema based in https://tmg.utoronto.ca/doc/1.6/gtamodel/user_guide/file_formats/emme_binary_matrix.html
	header_schema = [ 'magic',
			'version',
			'type',  #float32 = 1, float64 = 2, int32 = 3, int64 = 4
			'dim',  #Scalar = 0, Vector = 1, Matrix = 2
			'index',
			'zones'
			]
	type_dict = {1:np.float32, 2:np.float64, 3:np.int32, 4:np.int64}  
	with open(file, mode='rb') as inF:
	    header = { h : struct.unpack('i', inF.read(4))[0] for h in header_schema}
	    #reading columns and rows numbers
	    columnsRows = [struct.unpack('i', inF.read(4))[0] for i in range(header['dim'] * header['zones'])]
	    #reading data
	    data = inF.read( header['index'] * header['zones'] * np.dtype(type_dict[header['type']]).itemsize)



	data = np.frombuffer(data, dtype= type_dict[header['type']])
	data = np.resize(data,(header['index'], header['zones']))
	df = pd.DataFrame(data)
	df.columns = df.columns + 1
	df.index = df.index + 1
	return df

def draw_table_1way(tabkey, table, constraints, df):
    colname = tabkey[0]
    columns = {c: [] for c in df[colname].cat.categories}

    for const in table:
        for cval in constraints[const][colname]:
            columns[cval].append(const)

    celltext = [[' '.join(x) for x in columns.values()]]
    collabels = list(columns.keys())

    fig, ax = plt.subplots(figsize=(2*len(columns), 0.05*len(columns)))
    ax.set_axis_off()
    ptable = plt.table(cellText=celltext, colLabels=collabels, loc='center')


def draw_table_2way(tabkey, table, constraints, df):
    colname = tabkey[0]
    rowname = tabkey[1]
    columns = {c: i for i, c in enumerate(df[colname].cat.categories)}
    rows = {c: i for i, c in enumerate(df[rowname].cat.categories)}
    data = [['']*len(columns) for _ in range(len(rows))]

    for const in table:
        for v1, v2 in product(
                constraints[const][rowname],
                constraints[const][colname]):
            # create product of constarint values
            data[rows[v1]][columns[v2]] += ' ' + const

    collabels = list(columns.keys())
    rowlabels = list(rows.keys())

    fig, ax = plt.subplots(figsize=(2*len(columns), 2*len(rows)/10))
    ax.set_axis_off()
    ptable = plt.table(
        ellText=data,
        colLabels=collabels,
        rowLabels=rowlabels,
        loc='center'
    )


def draw_table_3way(tabkey, table, constraints, df):
    # Split 3way table into two 2way tables by SEXO
    table_F = [v for v in table if v.endswith('F')]
    table_M = [v for v in table if v.endswith('M')]
    tabkey = [v for v in tabkey if v != 'SEXO']
    assert len(tabkey) == 2

    draw_table_2way(tabkey, table_F, constraints, df)
