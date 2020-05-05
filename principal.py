# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Proyecto Final - Behavioral Finance
# -- archivo: principal.py - aplicación de las funciones a los datos
# -- mantiene:  Tamara Mtz.
# --            Natasha Gamez
# --            María Fernanda Ansoleaga
# -- repositorio: https://github.com/NatashaGamez/proyecto_equipo_2
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import visualizaciones as vn

datos = fn.f_leer_archivo(param_archivo='data2.xlsx')
df_pe = fn.f_precios(param_data=datos)
serie = vn.plot_profit_diario(datos=datos)
estacionariedad = fn.f_estacionaria(param_data=datos)
autocorr = fn.f_autocorrelation(param_data=datos)
pltauto= vn.autocorr(datos)
seasonality = vn.f_seasonality(param_data=datos)
hetero = fn.f_hetero(param_data=datos)
normtest = fn.f_normality_test(param_data=datos)
pltnorm = vn.f_normtest(param_data=datos)
outliers = vn.f_outliers(param_data=datos)
df_clasificacion = fn.f_clasificacion(param_data=datos)
df_metricas = fn.f_metrica(param_data=df_pe)



