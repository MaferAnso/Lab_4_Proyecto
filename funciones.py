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
