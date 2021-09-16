import datetime
import sqlite3
import os

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

from Solver.db import getValoresPonderados, deleteIndicadoresValoresDataFrameData, insertIndicadoresValoresDataFrameData


def create_indicadores_dict(data):
    data_indicadores = data[["indicadorId", "grupo"]]
    any_empty_string_mask = (data_indicadores == "").any(axis=1)
    data_indicadores = data_indicadores.loc[~any_empty_string_mask]
    indicadores_dict = {}
    for indicador in data_indicadores["indicadorId"].unique():
        indicador_df = data_indicadores[data_indicadores["indicadorId"] == indicador]
        indicador_groups = indicador_df["grupo"].unique()
        indicadores_dict[indicador] = indicador_groups
        
    return indicadores_dict


def create_indicador_dataframe(data, indicadores_dict): # indicadores_dict=create_indicadores_dict()
    dataframes = {}
    for key, values in indicadores_dict.items():
        for value in values:
            indicador_mask = (data["indicadorId"] == key)
            group_mask = (data["grupo"] == value)
            indicador_group_df = data[indicador_mask & group_mask][["Fecha", "valor"]]
            dataframes[(key, value)] = indicador_group_df
    return dataframes


def clean_dataframe(dataframe):
    dataframe.rename(columns={"valor": "valor"}, inplace=True)

    # Se inspeccionan los datos atípicos utilizando la regla de los 3 sigmas
    ds = float(dataframe["valor"].std())
    mean = float(dataframe["valor"].mean())

    r3s_inf = round(mean - 3*ds, 5)
    r3s_sup = round(mean + 3*ds, 5)

    # Los datos atípicos son llevados a la expresión de dato nulo
    #data_n = data.copy()
    dataframe[(dataframe["valor"] < (r3s_inf - 0.00001)) | (dataframe["valor"] > (r3s_sup + 0.00001))] = np.nan

    # Se interpolan los datos nulos
    dataframe.interpolate(inplace=True)
    dataframe.set_index("Fecha", inplace=True)


def train_test_split(dataframe, threshold=180, split=3):
    if dataframe.shape[0] < threshold:
        return
    # Se hace limpieza del dataframe
    clean_dataframe(dataframe)

    # Se establece el look back del modelo. Este define cuantos pasos temporales previos serán tomados en cuenta
    # para predecir la siguiente instacia de la serie de tiempo
    look_back = 80
    # día_1, día_2, ..., día_penúltimo, día_final                   -
    # [1,     2,    ..., n-1,           n]                          |
    # [2,     3,    ..., n-1,           n] shape[0] - look_back (cantidad de días para separar train/test)
    # ...                                                           |
    # |-------------look_back------------>                          v

    # Se crea el conjunto de datos para el modelo a partir de la serie de tiempo y la ventana de look back
    X = np.zeros((dataframe.shape[0] - look_back, look_back))
    y = np.zeros(dataframe.shape[0] - look_back)

    for i in range(X.shape[0]):
        X[i,:] = dataframe.iloc[i: i+look_back]['valor']
        y[i] = dataframe.iloc[i+look_back]['valor']

    # Se separa el conjunto de datos en dos partes, una para el entrenamiento y otra para la evaluación de los
    # resultados (últimos 30 días)
    n_split = int(X.shape[0] * (1 - 1/split))

    X_train = X[:-31, :] # se deberia usar esto: X[:n_split, :]
    y_train = y[:-31] # se deberia usar esto: y[:n_split]

    X_test = X[-31:, :] # se deberia usar esto: X[n_split:, :]
    y_test = y[-31:] # se deberia usar esto: y[n_split:]

    return X_train, X_test, y_train, y_test


def run_future_machine_learning_model(data): # data=create_indicador_dataframe().items()
    machine_learning_result = {}
    for indicador, df in data:
        # Se realiza la separación de los datos en entrenamiento y testeo
        X_train, X_test, y_train, y_test = train_test_split(df)

        # Se crea el modelo a utilizar para predecir
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=2,
            min_samples_leaf=1,
            oob_score=True,
            n_jobs=-1,
            random_state=42
        )
        model.fit(X_train, y_train)
        
        # Valores predichos para comprobación del modelo
        y_test_pred = model.predict(X_test)
        y_train_pred = model.predict(X_train)

        r2_test = r2_score(y_test, y_test_pred)
        r2_train = r2_score(y_train, y_train_pred)
        # if r2_test < 0.5 or r2_train < 0.5:
        #     continue

        # Con el modelo de One-Step ya entrenado, se utiliza el método recursivo para hacer Multi-Step Prediction
        y_ms_futuro_pred = []

        # Se toma la última instancia del X_test ya que son los parámetros al límite del ahora en el tiempo
        X_ms_futuro = X_test[0, :]

        # La idea es ir modificando el X_ms_futuro con cada iteración, moviéndose un paso en el tiempo hacia adelante
        # y utilizando la instancia calculada para completar dicho desplazamiento
        for i in range(y_test.size):
            y_os_pred = model.predict(X_ms_futuro.reshape(1, -1))
            y_ms_futuro_pred.append(y_os_pred)
            X_ms_futuro = np.append(X_ms_futuro[1:], y_os_pred)

        y_ms_futuro_pred = np.array(y_ms_futuro_pred)
        fecha_actual= datetime.date.today()

        fecha_futuro = [fecha_actual + datetime.timedelta(days=i) for i in range(31)]

        df_futuro = pd.DataFrame(
            data={
                "indicadorId": [indicador[0]]*len(y_ms_futuro_pred),
                "grupo": [indicador[1]]*len(y_ms_futuro_pred),
                "Fecha": fecha_futuro,
                "valor": np.squeeze(y_ms_futuro_pred),
                "esSimulacion": [0]*len(y_ms_futuro_pred),
                "esPrediccion": [1]*len(y_ms_futuro_pred)
            }
        )

        valores_ponderados = []
        for i in range(len(y_ms_futuro_pred)):
            valor_ponderado_futuro = getValoresPonderados(
                indicador=indicador[0],
                valor=y_ms_futuro_pred[i],
            )
            valores_ponderados.append(valor_ponderado_futuro.loc[0, "ponderacion"])
        
        df_futuro["valorPonderado"] = valores_ponderados
        machine_learning_result[(indicador[0], indicador[1])] = df_futuro
        deleteIndicadoresValoresDataFrameData(fecha_actual)
        insertIndicadoresValoresDataFrameData(df_futuro)

    return machine_learning_result


if __name__ == "__main__":
    # BAD;DEV - BAD;AP
    indicadores_file = "indicadores.db"
    cnx = sqlite3.connect(os.path.abspath(indicadores_file))

    data = pd.read_sql_query("SELECT * FROM indicadoresValores", cnx)
    data = data[data["esSimulacion"] == 0]
    data.dropna(axis=0, inplace=True)

    ind_dict = create_indicadores_dict(data)
    ind_df = create_indicador_dataframe(data, ind_dict)

    machine_learning = run_future_machine_learning_model(ind_df.items())
    breakpoint()
