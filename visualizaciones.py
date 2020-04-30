# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Proyecto Final - Behavioral Finance
# -- archivo: visualizaciones.py - muestra graficas o imagenes del proyecto
# -- mantiene:  Tamara Mtz.
# --            Natasha Gamez
# --            María Fernanda Ansoleaga
# -- repositorio: https://github.com/NatashaGamez/proyecto_equipo_2
# -- ------------------------------------------------------------------------------------ -- #

from matplotlib import pyplot
import funciones as fn
import plotly.graph_objects as go
import plotly as py
import pandas as pd

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

# -- -------------------------------------------------------------- FUNCION: Serie de tiempo -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Grafica que muestra la serie de tiempo del valor Actual
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
