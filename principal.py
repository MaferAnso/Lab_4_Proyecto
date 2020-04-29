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
[df_A, df_B, df_C, df_D] = fn.f_clasificacion_ocurrencia(param_data=datos)
