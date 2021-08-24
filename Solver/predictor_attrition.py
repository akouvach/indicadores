import sqlite3
import os

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

from Solver.db import getAttritionData


def process_data(data):
    # Eliminación de datos nulos
    data_n = data.dropna(axis=0)

    # Columnas con un único dato
    unique_data_cols = [i for i in data_n.columns if pd.unique(data_n[i]).size == 1]
    data_n.drop(unique_data_cols, axis=1, inplace=True)
    data_n.rename(columns={"EmployeeNumber": "EmployeeID"}, inplace=True)

    le = LabelEncoder()
    data_n["Attrition"] = le.fit_transform(data_n["Attrition"])
    data_n["Gender"] = le.fit_transform(data_n["Gender"])
    data_n["OverTime"] = le.fit_transform(data_n["OverTime"])

    # Se identifica la columna objetivo
    X = data_n.drop("Attrition", axis=1)
    y = data_n["Attrition"]

    # Se vectorizan las variables categóricas
    categorical_cols = [x for x in data_n.columns if data_n[x].dtypes == "O"]           # DEFINIR EL TIPO DE OBJETO DE LAS TABLAS -------------------------------
    oh_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)

    oh_cols = pd.DataFrame(oh_encoder.fit_transform(X[categorical_cols]))
    oh_names = pd.Series(oh_encoder.get_feature_names()).str.split("_")

    dict_cols = {}
    for i, value in enumerate(categorical_cols):
        dict_cols['x' + str(i)] = value
        
    oh_cols_names = []
    for i in oh_names:
        oh_cols_names.append(dict_cols[i[0]] + "_" + i[1])

    oh_cols.index = X.index
    oh_cols.columns = oh_cols_names

    cols_numericas = X.drop(categorical_cols, axis=1)
    X = pd.concat([cols_numericas, oh_cols], axis=1)

    return X, y


def split_data(data): # data=process_data()
    X, y = data

    # Se separa el conjunto de entrenamiento y de prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

    employee_id_train = X_train["EmployeeID"]
    employee_id_test = X_test["EmployeeID"]
    employee_ids = {"Train": employee_id_train, "Test": employee_id_test}

    X_train.drop(["EmployeeID"], axis=1, inplace=True)
    X_test.drop(["EmployeeID"], axis=1, inplace=True)

    X_train.reset_index(drop=True, inplace=True)
    X_test.reset_index(drop=True, inplace=True)
    y_train.reset_index(drop=True, inplace=True)
    y_test.reset_index(drop=True, inplace=True)

    return X_train, X_test, y_train, y_test, employee_ids


def run_machine_learning_model(data): # data=split_data()
    X_train, X_test, y_train, y_test, employee_ids = data

    # Se crea el modelo a utilizar para predecir
    bosque = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=1,
        max_samples=None,
        max_features='auto',
        criterion='gini',
        oob_score=True,
        n_jobs=-1,
        random_state=42
    )

    bosque.fit(X_train, y_train)
    y_test_pred = bosque.predict(X_test)
    y_train_pred = bosque.predict(X_train)

    roc_test = roc_auc_score(y_test, y_test_pred)
    roc_train = roc_auc_score(y_train, y_train_pred)
    # Agún tipo de evaluación que ayude a evaluar la capacidad del modelo
    # if ... bla bla bla

    # Importancia de cada característica para el modelo
    importancia = bosque.feature_importances_
    columns = X_train.columns
    indices = np.argsort(importancia)[::-1]

    cols_importantes = columns[indices][importancia[indices] > (importancia[indices].max() / 3)]

    # Se entrena nuevamente el modelo con las columnas más relevantes
    bosque.fit(X_train[cols_importantes], y_train)
    y_test_pred_imp = bosque.predict(X_test[cols_importantes])
    y_train_pred_imp = bosque.predict(X_train[cols_importantes])

    roc_test_imp = roc_auc_score(y_test, y_test_pred_imp)
    roc_train_imp = roc_auc_score(y_train, y_train_pred_imp)
    # Agún tipo de evaluación que ayude a evaluar la capacidad del modelo
    # if ... bla bla bla

    y_test_prob_imp = bosque.predict_proba(X_test[cols_importantes])
    y_train_prob_imp = bosque.predict_proba(X_train[cols_importantes])

    # Se calcula la probabilidad de cada empleado
    employee_id_test = employee_ids["Test"]
    employee_id_train = employee_ids["Train"]

    result_train = pd.DataFrame(np.around([y_train_prob_imp[:,1]*100], decimals=2), index=["probability"]).T
    result_train.index = employee_id_train.index
    result_test = pd.DataFrame(np.around([y_test_prob_imp[:,1]*100], decimals=2), index=["probability"]).T
    result_test.index = employee_id_test.index

    result = pd.concat([result_train, result_test])
    result.sort_index(inplace=True)

    return result


if __name__ == "__main__":
    # Lectura Excel
    employees_file = "DataSetInnoLab.xlsx"
    data = pd.read_excel(os.path.abspath(employees_file))

    # Lectura Base de Datos
    # employees_file = "indicadores.db"
    # cnx = sqlite3.connect(os.path.abspath(employees_file))

    # data = pd.read_sql_query("SELECT * FROM ...", cnx) # Definir nombre de tabla después de que sea cargada
    # data_numeric_cols = [
    #     "EmployeeID", "Age", "DistanceFromHome", "Education", "JobLevel", "MonthlyIncome", "NumCompaniesWorked", "PercentSalaryHike",
    #     "StockOptionLevel", "TotalWorkingYears", "TrainingTimesLastYear", "YearsAtCompany", "YearsSinceLastPromotion", "YearsWithCurrManager"
    # ]
    # for col in data_numeric_cols:
    #     data[col] = pd.to_numeric(data[col])

    # data = data[data["NumCompaniesWorked"] != "NA"]
    # data = data[data["TotalWorkingYears"] != "NA"]

    pre_process_data = process_data(data)
    splitted_data = split_data(pre_process_data)

    probability = run_machine_learning_model(splitted_data)
    result_df = pd.concat([data, probability], axis=1)
    breakpoint()

    # result_df.to_excel("output.xlsx")
    # test = result_df[["Attrition", "probability"]]
    # ((test["probability"] >= 50) == (test["Attrition"] == "Yes")).sum()
    # len((test["probability"] >= 50) == (test["Attrition"] == "Yes"))
