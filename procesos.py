# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Proyecto Final - Behavioral Finance
# -- archivo: procesos.py -
# -- mantiene:  Tamara Mtz.
# --            Natasha Gamez
# --            María Fernanda Ansoleaga
# -- repositorio: https://github.com/NatashaGamez/proyecto_equipo_2
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd                                       # dataframes y utilidades
import numpy as np
from datetime import timedelta                            # diferencia entre datos tipo tiempo
from oandapyV20 import API                                # conexion con broker OANDA
import oandapyV20.endpoints.instruments as instruments    # informacion de precios historicos


# -- --------------------------------------------------------- FUNCION: Descargar precios -- #
# -- Descargar precios historicos con OANDA

def f_precios_masivos(p0_fini, p1_ffin, p2_gran, p3_inst, p4_oatk, p5_ginc):
    """
    Parameters
    ----------
    p0_fini
    p1_ffin
    p2_gran
    p3_inst
    p4_oatk
    p5_ginc

    Returns
    -------
    dc_precios

    Debugging
    ---------

    """

    def f_datetime_range_fx(p0_start, p1_end, p2_inc, p3_delta):
        """

        Parameters
        ----------
        p0_start
        p1_end
        p2_inc
        p3_delta

        Returns
        -------
        ls_resultado

        Debugging
        ---------
        """

        ls_result = []
        nxt = p0_start

        while nxt <= p1_end:
            ls_result.append(nxt)
            if p3_delta == 'minutes':
                nxt += timedelta(minutes=p2_inc)
            elif p3_delta == 'hours':
                nxt += timedelta(hours=p2_inc)
            elif p3_delta == 'days':
                nxt += timedelta(days=p2_inc)

        return ls_result

    # inicializar api de OANDA

    api = API(access_token=p4_oatk)

    gn = {'S30': 30, 'S10': 10, 'S5': 5, 'M1': 60, 'M5': 60 * 5, 'M15': 60 * 15,
          'M30': 60 * 30, 'H1': 60 * 60, 'H4': 60 * 60 * 4, 'H8': 60 * 60 * 8,
          'D': 60 * 60 * 24, 'W': 60 * 60 * 24 * 7, 'M': 60 * 60 * 24 * 7 * 4}

    # -- para el caso donde con 1 peticion se cubran las 2 fechas
    if int((p1_ffin - p0_fini).total_seconds() / gn[p2_gran]) < 4999:

        # Fecha inicial y fecha final
        f1 = p0_fini.strftime('%Y-%m-%dT%H:%M:%S')
        f2 = p1_ffin.strftime('%Y-%m-%dT%H:%M:%S')

        # Parametros pra la peticion de precios
        params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                  "to": f2}

        # Ejecutar la peticion de precios
        a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
        a1_hist = api.request(a1_req1)

        # Para debuging
        # print(f1 + ' y ' + f2)
        lista = list()

        # Acomodar las llaves
        for i in range(len(a1_hist['candles']) - 1):
            lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                          'Open': a1_hist['candles'][i]['mid']['o'],
                          'High': a1_hist['candles'][i]['mid']['h'],
                          'Low': a1_hist['candles'][i]['mid']['l'],
                          'Close': a1_hist['candles'][i]['mid']['c']})

        # Acomodar en un data frame
        r_df_final = pd.DataFrame(lista)
        r_df_final = r_df_final[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
        r_df_final['TimeStamp'] = pd.to_datetime(r_df_final['TimeStamp'])
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final

    # -- para el caso donde se construyen fechas secuenciales
    else:

        # hacer series de fechas e iteraciones para pedir todos los precios
        fechas = f_datetime_range_fx(p0_start=p0_fini, p1_end=p1_ffin, p2_inc=p5_ginc,
                                     p3_delta='minutes')

        # Lista para ir guardando los data frames
        lista_df = list()

        for n_fecha in range(0, len(fechas) - 1):

            # Fecha inicial y fecha final
            f1 = fechas[n_fecha].strftime('%Y-%m-%dT%H:%M:%S')
            f2 = fechas[n_fecha + 1].strftime('%Y-%m-%dT%H:%M:%S')

            # Parametros pra la peticion de precios
            params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                      "to": f2}

            # Ejecutar la peticion de precios
            a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
            a1_hist = api.request(a1_req1)

            # Para debuging
            print(f1 + ' y ' + f2)
            lista = list()

            # Acomodar las llaves
            for i in range(len(a1_hist['candles']) - 1):
                lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                              'Open': a1_hist['candles'][i]['mid']['o'],
                              'High': a1_hist['candles'][i]['mid']['h'],
                              'Low': a1_hist['candles'][i]['mid']['l'],
                              'Close': a1_hist['candles'][i]['mid']['c']})

            # Acomodar en un data frame
            pd_hist = pd.DataFrame(lista)
            pd_hist = pd_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
            pd_hist['TimeStamp'] = pd.to_datetime(pd_hist['TimeStamp'])

            # Ir guardando resultados en una lista
            lista_df.append(pd_hist)

        # Concatenar todas las listas
        r_df_final = pd.concat([lista_df[i] for i in range(0, len(lista_df))])

        # resetear index en dataframe resultante porque guarda los indices del dataframe pasado
        r_df_final = r_df_final.reset_index(drop=True)
        r_df_final['Open'] = pd.to_numeric(r_df_final['Open'], errors='coerce')
        r_df_final['High'] = pd.to_numeric(r_df_final['High'], errors='coerce')
        r_df_final['Low'] = pd.to_numeric(r_df_final['Low'], errors='coerce')
        r_df_final['Close'] = pd.to_numeric(r_df_final['Close'], errors='coerce')

        return r_df_final
# -- --------------------------------------------------------- FUNCION: Resume escenarios -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Resumen de acontecimientos de direccion postiva, negativa, pips bajistas y alcistas
# -- promedio Y volumen pormedio por caso A,B,C,D
def f_resumen_escenarios(param_data):
    """
    Parameters
    ----------
    param_data: DataFrame con informacion de escenarios

    Returns
    -------
    df_resumen: DataFrame con informacion resultante

    Debugging
    ---------
    """

    dpA = 0
    dnA = 0
    paA = []
    pbA = []
    vA = []
    dpB = 0
    dnB = 0
    paB = []
    pbB = []
    vB = []
    dpC = 0
    dnC = 0
    paC = []
    pbC = []
    vC = []
    dpD = 0
    dnD = 0
    paD = []
    pbD = []
    vD = []
    for i in range(param_data.shape[0]):
        if param_data['Escenario'][i] == 'A':
            paA.append(param_data['Pip Alcista'][i])
            pbA.append(param_data['Pip Bajista'][i])
            vA.append(param_data['Volatilidad'][i])
            if param_data['Direccion'][i] == 1:
                dpA = dpA + 1
            else:
                dnA = dnA + 1
        elif param_data['Escenario'][i] == 'B':
            paB.append(param_data['Pip Alcista'][i])
            pbB.append(param_data['Pip Bajista'][i])
            vB.append(param_data['Volatilidad'][i])
            if param_data['Direccion'][i] == 1:
                dpB = dpB + 1
            else:
                dnB = dnB + 1
        elif param_data['Escenario'][i] == 'C':
            paC.append(param_data['Pip Alcista'][i])
            pbC.append(param_data['Pip Bajista'][i])
            vC.append(param_data['Volatilidad'][i])
            if param_data['Direccion'][i] == 1:
                dpC = dpC + 1
            else:
                dnC = dnC + 1
        else:
            paD.append(param_data['Pip Alcista'][i])
            pbD.append(param_data['Pip Bajista'][i])
            vD.append(param_data['Volatilidad'][i])
            if param_data['Direccion'][i] == 1:
                dpD = dpD + 1
            else:
                dnD = dnD + 1
    paA = np.mean(paA)
    pbA = np.mean(pbA)
    vA = np.mean(vA)
    paB = np.mean(paB)
    pbB = np.mean(pbB)
    vB = np.mean(vB)
    paC = np.mean(paC)
    pbC = np.mean(pbC)
    vC = np.mean(vC)
    paD = np.mean(paD)
    pbD = np.mean(pbD)
    vD = np.mean(vD)
    df_resumen = {'Escenario': ['A','B','C','D'],
                  'Direccion Positiva': [dpA, dpB, dpC, dpD],
                  'Direccion Negativa': [dnA, dnB, dnC, dnD],
                  'Pip Alcistas': [paA, paB, paC, paD],
                  'Pip Bajistas': [pbA, pbB, pbC, pbD],
                  'Volatilidad': [vA, vB, vC, vD]}
    df_resumen = pd.DataFrame(df_resumen)
    return df_resumen
# -- ------------------------------------------------------------------------------------ -- #
