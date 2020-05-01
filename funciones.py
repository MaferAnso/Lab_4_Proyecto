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
import procesos as pr
from datos import OA_Ak
import datetime
from datetime import datetime as dt


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
    df_data['date'] = [dt.strptime(df_data['date'][i], '%m/%d/%Y %H:%M:%S') for i in range(df_data.shape[0])]

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
    df_A,df_A, df_B, df_C, df_D : pd.DataFrame : con información de calsificacion de
    ocurrencia A,B,C,D
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

# -- -------------------------------------------------------- FUNCION: Descargar precios  -- #
# -- ------------------------------------------------------------------------------------ -- #
def f_precios(param_data):
    '''

    Parameters
    ----------
    param_data : str : DataFrame base
    Returns
    -------
    df_precios : pd.DataFrame :
        ---------
        param_data = df_data

    '''
    # Verificar que no haya viernes, despues de 4, sabado o domingo antes de 4
    index = []
    for i in range(param_data.shape[0]):
        if param_data.iloc[i, 0].weekday() == 5 or param_data.iloc[i, 0].weekday() == 6:
            index.append(i)
    min30 = datetime.timedelta(minutes=32)
    min1 = datetime.timedelta(minutes=1)
    # token de OANDA
    OA_In = "EUR_USD"  # Instrumento
    OA_Gn = "M1"  # Granularidad de velas
    fini = pd.to_datetime(param_data.iloc[0, 0] + min1).tz_localize('GMT')  # Fecha inicial
    ffin = pd.to_datetime(param_data.iloc[0, 0] + min30).tz_localize('GMT')  # Fecha final
    df_pe = pr.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn,
                                 p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=4900)
    a = []
    for i in range(param_data.shape[0]):
        if i > 0 and i != index[0] and i != index[1]:
            fini = pd.to_datetime(param_data.iloc[i, 0] + min1).tz_localize('GMT')  # Fecha inicial
            ffin = pd.to_datetime(param_data.iloc[i, 0] + min30).tz_localize('GMT')  # Fecha final
            df_pe1 = pr.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn,
                                          p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=4900)
            df_pe = pd.concat([df_pe, df_pe1])
    return df_pe
