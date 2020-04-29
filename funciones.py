# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Proyecto Final - Behavioral Finance
# -- archivo: funciones.py - funciones para la elaboracion del proyecto
# -- mantiene:  Tamara Mtz.
# --            Natasha Gamez
# --            María Fernanda Ansoleaga
# -- repositorio: https://github.com/NatashaGamez/proyecto_equipo_2
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd
import numpy as np


# -- -------------------------------------------------------------- FUNCION: Leer archivo -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Leer un archivo externo en Excel

def f_leer_archivo(param_archivo):
    '''

    Parameters
    ----------
    param_archivo : str : nombre de archivo a leer
    Returns
    -------
    df_data : pd.DataFrame : con informacion contenida en archivo leido
    Debugging
    ---------
    param_archivo = 'data2.xlsx'

    '''

    # Leer archivo de datos y guardarlo en un DataFrame
    df_data = pd.read_excel('archivos/' + param_archivo, sheet_name='Datos')

    # Cnvertir en minusculas el nombre de las columnas
    df_data.columns = [list(df_data.columns)[i].lower()
                       for i in range(0, len(df_data.columns))]
    # Asegurar que ciertas son del tipo numerico
    numcols = ['actual', 'previous', 'desv', 'cons']

    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)

    return df_data


# -- ---------------------------------------------------------- FUNCION: Clasificar datos -- #
# -- ------------------------------------------------------------------------------------ -- #
def f_clasificacion_ocurrencia(param_data):
    '''

    Parameters
    ----------
    param_data : str : DataFrame base
    Returns
    -------
    df_clasificacion : pd.DataFrame : con información de calsificacion de ocurrencia A,B,C,D
    Debugging
    ---------
    param_data = df_data

    '''
    # A	Actual >= Consensus >= Previous
    # B	Actual >= Consensus < Previous
    # C	Actual < Consensus >= Previous
    # D	Actual < Consensus < Previous
    # Revisar que si exista NaN en previus poner actual
    for i in range(param_data.shape[0]):
        if np.isnan(param_data['previous'][i]):
            param_data['previous'][i] = param_data['actual'][i]

    # Revisar que si exista NaN en consensus poner previus
    for i in range(param_data.shape[0]):
        if np.isnan(param_data['cons'][i]):
            param_data['cons'][i] = param_data['previous'][i]

    # Clasificar
    a = [(i) for i in range(param_data.shape[0]) if param_data['actual'][i] \
         >= param_data['cons'][i] >= param_data['previous'][i]]
    b = [(i) for i in range(param_data.shape[0]) if param_data['actual'][i] \
         >= param_data['cons'][i] < param_data['previous'][i]]
    c = [(i) for i in range(param_data.shape[0]) if param_data['actual'][i] \
         < param_data['cons'][i] >= param_data['previous'][i]]
    d = [(i) for i in range(param_data.shape[0]) if param_data['actual'][i] \
         < param_data['cons'][i] < param_data['previous'][i]]

    # Tabla informacion datos A
    date = [];
    actual = [];
    con = [];
    prev = []
    for k in range(len(a)):
        for x in range(param_data.shape[0]):
            if a[k] == x:
                date.append(param_data['date'][x])
                actual.append(param_data['actual'][x])
                con.append(param_data['cons'][x])
                prev.append(param_data['previous'][x])

    df_A = pd.DataFrame(list(zip(date, actual, con, prev)), index=a)
    df_A.columns = ('Date', 'Actual', 'Consensus', 'Previus')
    # Tabla informacion datos B
    date = [];
    actual = [];
    con = [];
    prev = []
    for k in range(len(b)):
        for x in range(param_data.shape[0]):
            if b[k] == x:
                date.append(param_data['date'][x])
                actual.append(param_data['actual'][x])
                con.append(param_data['cons'][x])
                prev.append(param_data['previous'][x])

    df_B = pd.DataFrame(list(zip(date, actual, con, prev)), index=b)
    df_B.columns = ('Date', 'Actual', 'Consensus', 'Previus')
    # Tabla informacion datos   C
    date = [];
    actual = [];
    con = [];
    prev = []
    for k in range(len(c)):
        for x in range(param_data.shape[0]):
            if c[k] == x:
                date.append(param_data['date'][x])
                actual.append(param_data['actual'][x])
                con.append(param_data['cons'][x])
                prev.append(param_data['previous'][x])

    df_C = pd.DataFrame(list(zip(date, actual, con, prev)), index=c)
    df_C.columns = ('Date', 'Actual', 'Consensus', 'Previus')
    # Tabla informacion datos D
    date = [];
    actual = [];
    con = [];
    prev = []
    for k in range(len(d)):
        for x in range(param_data.shape[0]):
            if d[k] == x:
                date.append(param_data['date'][x])
                actual.append(param_data['actual'][x])
                con.append(param_data['cons'][x])
                prev.append(param_data['previous'][x])

    df_D = pd.DataFrame(list(zip(date, actual, con, prev)), index=d)
    df_D.columns = ('Date', 'Actual', 'Consensus', 'Previus')
    return df_A, df_B, df_C, df_D
