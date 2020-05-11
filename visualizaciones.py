# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Proyecto Final - Behavioral Finance
# -- archivo: visualizaciones.py - muestra graficas o imagenes del proyecto
# -- mantiene:  Tamara Mtz.
# --            Natasha Gamez
# --            María Fernanda Ansoleaga
# -- repositorio: https://github.com/NatashaGamez/proyecto_equipo_2
# -- ------------------------------------------------------------------------------------ -- #

import matplotlib.pyplot as plt
import statsmodels.tsa.seasonal as sts
import plotly.graph_objects as go
import plotly as py
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
import numpy as np
import scipy.stats as st  # Librería estadística

py.offline.init_notebook_mode(connected=True)
from plotly.offline import plot


# -- -------------------------------------------------------------- FUNCION: Serie de tiempo -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Grafica que muestra la serie de tiempo del valor Actual
def plot_profit_diario(datos):
    """

    Parameters
    ----------
    datos: Muestra los valores del  indicador elegido

    Returns
    -------
    Grafica de la serie de tiempo del valor Actual

    Debugging
    --------
    datos = fn.f_leer_archivo(datos)
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=datos.date, y=datos.actual, mode='lines',
                             name='Serie de tiempo del valor Actual', line=dict(color='blue')))
    fig.show()


# -- -------------------------------------------------------------- FUNCION: Autocorrelacion -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Grafica que muestrala autocorrelacion y autocorrelacion parcial de la serie de tiempo del valor Actual
def autocorr(datos):
    """
    Parameters
    ----------
    datos: Muestra los valores del  indicador elegido

    Returns
    -------
    Grafica de la serie de tiempo del valor Actual

    Debugging
    --------
    datos = fn.f_leer_archivo(datos)
    """
    data = datos['actual']
    fig, ax = plt.subplots(3, figsize=(12, 6))
    ax[0] = plot_acf(data, ax=ax[0], lags=25)
    ax[1] = plot_pacf(data, ax=ax[1], lags=25)
    ax[2].plot(data)
    return ax[0], ax[1], ax[2]


# -- -------------------------------------------------------------- FUNCION: Prueba de normalidad -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Grafica que muestra si la serie de tiempo del valor Actual es normal
def f_normtest(param_data):
    """
    Parameters
    ----------
    datos: Muestra los valores del  indicador elegido

    Returns
    -------
    Grafica de la serie de tiempo del valor Actual

    Debugging
    --------
    param_data = fn.f_leer_archivo(data2)
    """
    data = param_data['actual']
    # Creo variables aleatorias normales
    mu = np.mean(data)
    sigma = np.std(data)
    measurements = np.random.normal(loc=mu, scale=sigma, size=100)

    # Histograma de las variables creadas
    divisiones = 10  # Cantidad de barras en el histograma
    plt.hist(data, divisiones, density=True)
    x = np.arange(0, 60, .1)
    y = st.norm.pdf(x, loc=mu, scale=sigma)
    plt.plot(x, y, 'r--')
    plt.ylabel('Probability')
    plt.grid()
    hist = plt.show()

    # gráfica de Q-Q entre las muestras creadas y una curva normal
    ax2 = st.probplot(data, dist="norm", plot=plt)
    plt.grid()
    plt.xlabel('Normal theorical quantiles')
    plt.ylabel('Data theorical quantiles')
    qq = plt.show()
    return hist, qq


def f_normt(param_data):
    """
    Parameters
    ----------
    datos: Muestra los valores del  indicador elegido

    Returns
    -------
    Grafica de la serie de tiempo del valor Actual

    Debugging
    --------
    param_data = fn.f_leer_archivo(data2)
    :param param_data:
    """
    data = param_data['actual']
    J = len(data)  # Cantidad de particiones del histograma bins=159
    [freq_1, x1, p] = plt.hist(data, J, density=True)
    # Se obvia el último valor de x para obtener exactamente J muestras de x
    x1 = x1[:-1]
    mu = np.mean(data)
    sigma = np.std(data)
    pi = st.norm.pdf(data, loc=mu, scale=sigma)
    # Cálculo de la esperanza usando la expresión teórica
    Ei = x1 * pi
    # Cálculo teórico de la chi cuadrada
    x2 = np.sum(list(map(lambda Ei, obs_i: (obs_i - Ei) ** 2 / Ei, Ei, freq_1)))
    print('Valor de chi cuadrado teorico  = ', x2)

    # Cálculo usando la librería estadística de la chi cuadrada
    X2 = st.chisquare(freq_1, Ei)
    print('Valor de chi cuadrado librería = ', X2)

    # Cálculo de Grados de libertad del estadístico
    p = 2  # Parámetros estimados con los datos
    m = J - p - 1  # grados de libertad

    Chi_est = st.chi2.ppf(q=0.95, df=m)
    return 'Estadístico de chi_cuadrado = ', Chi_est, 'Media muestral = ', mu,\
           '\nDesviación estándar muestral = ', sigma


# -- -------------------------------------------------------------- FUNCION: Estacionalidad -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Grafica que muestra la estacionalidad de la serie de tiempo del valor Actual
def f_seasonality(param_data):
    """
    Parameters
    ----------
    datos: Muestra los valores del  indicador elegido

    Returns
    -------
    Grafica de la estacionalidad de la serie de tiempo del valor Actual

    Debugging
    --------
    datos = fn.f_leer_archivo(datos)
    """
    data = param_data['actual']
    result = sts.seasonal_decompose(data, freq=30)
    chart = result.plot()
    return plt.show()


# -- -------------------------------------------------------------- FUNCION: Detección de atipicos -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Grafica que muestra los datos atipicos de la serie de tiempo del valor Actual
def f_outliers(param_data):
    """
    Parameters
    ----------
    datos: Muestra los valores del  indicador elegido

    Returns
    -------
    Grafica de los valores atipicos de la serie de tiempo del valor Actual

    Debugging
    --------
    datos = fn.f_leer_archivo(datos)
    :param param_data:
    :return:
    """
    data = param_data['actual']
    sns.boxplot(x=data)
    return plt.show()
