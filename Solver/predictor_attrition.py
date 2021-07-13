import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Lectura de datos
data = pd.read_csv(...)

# Eliminación de datos nulos
data_n = data.dropna(axis=0)

# Columnas con un único dato
cols_dato_unico = [i for i in data.columns if pd.unique(data[i]).size == 1]
data_n.drop(cols_dato_unico, axis=1, inplace=True)

le = LabelEncoder()
data_n["Attrition"] = le.fit_transform(data_n["Attrition"])
data_n["Gender"] = le.fit_transform(data_n["Gender"])

# Se identifica la columna objetivo
X = data_n.drop("Attrition", axis=1)
y = data_n["Attrition"]

# Se vectorizan las variables categóricas
cols_categoricas = [x for x in data_n.columns if data_n[x].dtypes == "O"]
oh_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)

oh_cols = pd.DataFrame(oh_encoder.fit_transform(X[cols_categoricas]))
oh_names = oh_encoder.get_feature_names()

dict_cols = {}
for i, value in enumerate(cols_categoricas):
    dict_cols['x' + str(i)] = value
    
oh_cols_names = []
for i in dict_cols:
    for j in oh_names:
        if i in j:
            temp = j.replace(i, dict_cols[i])
            oh_cols_names.append(temp)
            
oh_cols.index = X.index
oh_cols.columns = oh_cols_names

cols_numericas = X.drop(cols_categoricas, axis=1)
X = pd.concat([cols_numericas, oh_cols], axis=1)

# Se separa el conjunto de entrenamiento y de prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

employee_id_train = X_train["EmployeeID"]
employee_id_test = X_test["EmployeeID"]

X_train.drop(["EmployeeID"], axis=1, inplace=True)
X_test.drop(["EmployeeID"], axis=1, inplace=True)

X_train.reset_index(drop=True, inplace=True)
X_test.reset_index(drop=True, inplace=True)
y_train.reset_index(drop=True, inplace=True)
y_test.reset_index(drop=True, inplace=True)

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

y_test_prob = bosque.predict_proba(X_test)
y_train_prob = bosque.predict_proba(X_train)

roc_test = roc_auc_score(y_test, y_test_pred)
roc_train = roc_auc_score(y_train, y_train_pred)

# Importancia de cada característica para el modelo
importancia = bosque.feature_importances_
columns = X_train.columns
indices = np.argsort(importancia)[::-1]

cols_importantes = columns[indices][importancia[indices] > (importancia[indices].max() / 3)]

# Se entrena nuevamente el modelo con las columnas más relevantes
bosque.fit(X_train[cols_importantes], y_train)
y_test_pred_imp = bosque.predict(X_test[cols_importantes])
y_train_pred_imp = bosque.predict(X_train[cols_importantes])

y_test_prob_imp = bosque.predict_proba(X_test[cols_importantes])
y_train_prob_imp = bosque.predict_proba(X_train[cols_importantes])

roc_test_imp = roc_auc_score(y_test, y_test_pred)
roc_train_imp = roc_auc_score(y_train, y_train_pred)

# Se calcula la probabilidad de cada empleado
result_train = pd.DataFrame(np.around([y_train_prob_imp[:,1]*100], decimals=2), index=["probability"]).T
result_train.index = employee_id_train.values
result_test = pd.DataFrame(np.around([y_test_prob_imp[:,1]*100], decimals=2), index=["probability"]).T
result_test.index = employee_id_test.values

result = pd.concat([result_train, result_test])
result.sort_index(inplace=True)
