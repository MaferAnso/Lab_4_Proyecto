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
    df_data['date'] = [dt.strptime(df_data['date'][i], '%m/%d/%Y %H:%M:%S')\
                       for i in range(df_data.shape[0])]

    return df_data


# -- ---------------------------------------------------------- FUNCION: Clasificar datos -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Clasifica datos en A, B, C, D
def f_clasificacion(param_data):
    '''

    Parameters
    ----------
    param_data : str : DataFrame base
    Returns
    -------
    df_clase : pd.DataFrame : con información de calsificacion de
    ocurrencia A,B,C,D
    ---------
    param_data = df_data

    '''
    # A	Actual >= Consensus >= Previous
    # B	Actual >= Consensus < Previous
    # C	Actual < Consensus >= Previous
    # D	Actual < Consensus < Previous
    # Revisar fecha no tenga viernes en tarde, sabado y domingo en mañana
    index = []
    for i in range(param_data.shape[0]):
        if param_data.iloc[i, 0].weekday() == 5 or param_data.iloc[i, 0].weekday() == 6:
            index.append(i)
    # Revisar que si exista NaN en previus poner actual
    for i in range(param_data.shape[0]):
        if np.isnan(param_data['previous'][i]):
            param_data['previous'][i] = param_data['actual'][i]

    # Revisar que si exista NaN en consensus poner previus
    for i in range(param_data.shape[0]):
        if np.isnan(param_data['cons'][i]):
            param_data['cons'][i] = param_data['previous'][i]

    # Clasificar
    clasificacion = []
    fecha = []
    for i in range(param_data.shape[0]):
        if param_data['actual'][i] >= param_data['cons'][i] >= param_data['previous'][i] and (i in index) == False:
            clasificacion.append('A')
        if param_data['actual'][i] >= param_data['cons'][i] < param_data['previous'][i] and (i in index) == False:
            clasificacion.append('B')
        if param_data['actual'][i] < param_data['cons'][i] >= param_data['previous'][i] and (i in index) == False:
            clasificacion.append('C')
        if param_data['actual'][i] < param_data['cons'][i] < param_data['previous'][i] and (i in index) == False:
            clasificacion.append('D')
        if (i in index) == False:
            fecha.append(param_data['date'][i].date())

    df_clase = pd.DataFrame(list(zip(fecha, clasificacion)))
    df_clase.columns = ('TimeStamp', 'Escenario')
    return df_clase


# -- -------------------------------------------------------- FUNCION: Descargar precios  -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Descarga precios de los 30 minutos despues que sale el indicador
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
    # token de OANDA
    OA_In = "EUR_USD"  # Instrumento
    OA_Gn = "M1"  # Granularidad de velas
    fini = pd.to_datetime(param_data.iloc[0, 0]).tz_localize('GMT')  # Fecha inicial
    ffin = pd.to_datetime(param_data.iloc[0, 0] + min30).tz_localize('GMT')  # Fecha final
    df_pe = pr.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn,
                                 p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=4900)
    a = []
    for i in range(param_data.shape[0]):
        if i > 0 and i != index[0] and i != index[1]:
            fini = pd.to_datetime(param_data.iloc[i, 0]).tz_localize('GMT')  # Fecha inicial
            ffin = pd.to_datetime(param_data.iloc[i, 0] + min30).tz_localize('GMT')  # Fecha final
            df_pe1 = pr.f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn,
                                          p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=4900)
            df_pe = pd.concat([df_pe, df_pe1])
            df_pe = df_pe.reset_index(drop=True)
    return df_pe


# -- ------------------------------------------------------------------ FUNCION: Metricas -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Determina la direccion de precios, pips alcistas, pips bajistas, volatilidad
def f_metrica(param_data):
    """
    Parameters
    ----------
    param_data : DataFrame con los datos del precio del indicador
    Returns
    -------
    df_metricas : pd.DataFrame : con informacion contenida en archivo leido
    Debugging
    ---------
    param_data = df_data
    """
    # Separar dias
    dia_fin = []
    fecha = []
    for i in range(param_data.shape[0]):
        if i < (param_data.shape[0] - 1) and param_data['TimeStamp'][i].date() != \
                param_data['TimeStamp'][i + 1].date():
            dia_fin.append(i)
            fecha.append(param_data['TimeStamp'][i].date())
        if i == (param_data.shape[0] - 1):
            dia_fin.append(i)
            fecha.append(param_data['TimeStamp'][i].date())
    # obtener direccion
    direccion = []
    dir1 = []
    for k in range(len(dia_fin)):
        if k == 0:
            direccion.append((param_data['Close'][dia_fin[k]] -
                              param_data['Open'][dia_fin[k] - 30])*10000)
            if param_data['Close'][dia_fin[k]] > param_data['Open'][dia_fin[k] - 30]:
                dir1.append(1)
            else:
                dir1.append(-1)
        if k > 0:
            direccion.append(param_data['Close'][dia_fin[k]] -
                             param_data['Open'][dia_fin[k - 1] + 1]*10000)
            if param_data['Close'][dia_fin[k]] > param_data['Open'][dia_fin[k] - 30]:
                dir1.append(1)
            else:
                dir1.append(-1)

    # Pips alcista y Pips bajista y Volatilidad
    maxi = []
    mini = []
    op = [param_data['Open'][0]]
    for g in range(len(dia_fin)):
        if g <= 0:
            col = param_data['High'][g:dia_fin[g] + 1]
            col2 = param_data['Low'][g:dia_fin[g] + 1]
            maxi.append(col.max())
            mini.append(col2.min())
        if g > 0:
            col = param_data['High'][dia_fin[g - 1] + 1:dia_fin[g] + 1]
            col2 = param_data['Low'][dia_fin[g - 1] + 1:dia_fin[g] + 1]
            maxi.append(col.max())
            mini.append(col2.min())
    for m in range(len(dia_fin)):
        if m <= 155:
            op.append(param_data['Open'][dia_fin[m] + 1])
    al = []
    baj = []
    vol = []
    for k in range(len(op)):
        al.append((maxi[k] - op[k])*10000) # Pips alcistas
        baj.append((op[k] - mini[k])*10000) # Pips bajistas
        vol.append((maxi[k]-mini[k])*10000) # Volatilidad
    df_metricas = pd.DataFrame(list(zip(fecha,dir1,al,baj,vol)))
    df_metricas.columns = ('TimeStamp','Direccion', 'Pip Alcista', 'Pip Bajista', 'Volatilidad')

    return df_metricas

# -- ---------------------------------------------------------------- FUNCION: Escenarios -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Muestra tabla completa de escenarios en tiempo de trainin
def f_escenarios(param_metricas,param_clasificacion, fini,ffin):
    """
    Parameters
    ----------
    param_metricas: DataFrame con metricas de precios
    param_clasificacion: DataFrame con clasificacion indice
    fini: Fecha inicial de entranmiento
    ffin: Fecha final de entranamiento
    Returns
    -------
    df_escenarios : pd.DataFrame : con informacion contenida en archivo leido
    Debugging
    ---------
    param_data = df_data
    """
    df = pd.concat([param_clasificacion, param_metricas['Direccion'],
                    param_metricas['Pip Alcista'], param_metricas['Pip Bajista'],
                    param_metricas['Volatilidad']], axis=1)

    Index = [i for i in range(df.shape[0]) if fini <= df['TimeStamp'][i] <= ffin]
    df_escenarios = df.iloc[Index[0]:Index[len(Index) - 1], :]
    df_escenarios = df_escenarios.reset_index(drop=True)

    return df_escenarios

# ESTADISTICA
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import pacf
import statsmodels.api as sm
import statsmodels.stats.diagnostic as smd
import scipy.stats as st
from statsmodels.tsa.stattools import adfuller


# -- ----------------------------------------------------------- FUNCION: Autocorrelación -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Determina la autocorrelación que hay en la serie
def f_autocorrelation(param_data):
    """

    Parameters
    ----------
    param_data : DataFrame con los datos del precio del indicador
    Returns
    -------
    autocorrelation : pd.DataFrame : con informacion contenida en archivo leido
    Debugging
    ---------
    param_data = df_data

    """
    data = param_data['actual']
    acf_array = acf(data, nlags=20, qstat=True)
    autocorrelation = data.autocorr()
    part_acf = pacf(data, nlags=20)
    return {acf_array, part_acf}


# -- -------------------------------------------------------- FUNCION: Heterocedasticidad -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Determina la heterocedasticidad que hay en la serie
def f_hetero(param_data):
    """
    Parameters
    ----------
    param_data : DataFrame con los datos del precio del indicador
    Returns
    -------
    heterokedasticity : valores para vereficar la heterocedasticidad de la serie
    Debugging
    ---------
    param_data = df_data
    """
    data = param_data['actual']
    # hetero = sm.OLS(data, sm.add_constant(data.index)).fit()
    # res = hetero.resid
    # bp_test = smd.het_breuschpagan(res, hetero.model.exog)
    bp_test = smd.het_arch(data)
    labels = ['LM Statistic', 'LM-Test p-value', 'F-Statistic', 'F-Test p-value']
    heterokedasticity = [dict(zip(labels, bp_test))]
    return heterokedasticity


# -- ------------------------------------------------------ FUNCION: Prueba de normalidad -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Determina si la serie es normal
def f_normality_test(param_data):
    """
    Parameters
    ----------
    param_data : DataFrame con los datos del precio del indicador
    Returns
    -------
    p_value : str : Si los datos son normales o no
    Debugging
    ---------
    param_data = df_data
    """
    data = param_data['actual']
    k2, p = st.normaltest(data)  # prueba de normalidad con D’Agostino and Pearson’s tests
    shapiro, ps = st.shapiro(data)  # prueba de normalidad con Shapiro-Wilk test
    alpha = .05  # Es con un intervalo de confianza del 95%
    if p < alpha and ps < alpha:
        return "p-value = ", p, "La hipótesis nula se rechaza"
    else:
        return "p-value = ", p, "La hipótesis nula no se rechaza"


# -- ------------------------------------------------- FUNCION: Prueba de estacionariedad -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Determina si la serie es estacionaria
def f_estacionaria(param_data):
    """

    Parameters
    ----------
    param_data : DataFrame con los datos del precio del indicador
    Returns
    -------
    p_value : str : Si los datos son estacionarios o no
    Debugging
    ---------
    param_data = df_data
    """
    data = param_data['actual']
    result = adfuller(data)
    p_value = result[1]
    alpha = .05  # Es con un intervalo de confianza del 95%
    if p_value < alpha:
        return "p-value = ", p_value, "La hipótesis nula se rechaza"
    else:
        return "p-value = ", p_value, "La hipótesis nula no se rechaza"

# ESTRATEGIA
# -- ---------------------------------------------------------------- FUNCION: Decisiones -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Determina las estrategias que se tomaran para hacer trading
def f_decisiones(param_data):
    """
    Parameters
    ----------
    param_data: DataFrame con informacion de escenarios

    Returns
    -------
    df_decisiones: DataFrame con informacion resultante

    Debugging
    ---------
    """
    # Obtener resumen
    param = pr.f_resumen_escenarios(param_data)
    # Obtener estrategia
    operacion = []
    sl = []
    tp = []
    for i in range(param.shape[0]):
        if param['Direccion Positiva'][i] > param['Direccion Negativa'][i]:
            operacion.append('Compra')
            tp.append(round(param['Pip Alcistas'][i]+param['Volatilidad'][i]))
            sl.append(round(param['Pip Bajistas'][i]+param['Volatilidad'][i]))
        else:
            operacion.append('Venta')
            sl.append(round(param['Pip Alcistas'][i] + param['Volatilidad'][i]))
            tp.append(round(param['Pip Bajistas'][i] + param['Volatilidad'][i]))

    df_decision = {'Escenario': ['A','B','C','D'],
                  'Operacion': operacion, 'sl': sl,'tp':tp}
    df_decision = pd.DataFrame(df_decision)


    return df_decision