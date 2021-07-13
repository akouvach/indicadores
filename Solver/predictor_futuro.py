import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor

# Lectura de datos
data = pd.read_csv(...)

# Se inspeccionan los datos atípicos utilizando la regla de los 3 sigmas
ds = float(data['indicador'].std())
mean = float(data['indicador'].mean())

r3s_inf = round(mean - 3*ds, 5)
r3s_sup = round(mean + 3*ds, 5)

# Los datos atípicos son llevados a la expresión de dato nulo
data_n = data[(data['indicador'] <= r3s_inf) | (data['indicador'] >= r3s_sup)] = np.nan

# Se interpolan los datos nulos
data_n = data_n.interpolate()

# Se establece el look back del modelo. Este define cuantos pasos temporales previos serán tomados en cuenta
# para predecir la siguiente instacia de la serie de tiempo
look_back = 90

# Se crea el conjunto de datos para el modelo a partir de la serie de tiempo y la ventana de look back
X = np.zeros((data_n.shape[0] - look_back - 1, look_back))
y = np.zeros(data_n.shape[0] - look_back - 1)

for i in range(X.shape[0]):
    X[i,:] = data_n.iloc[i: i+look_back]['indicador']
    y[i] = data_n.iloc[i+look_back]

# Se separa el conjunto de datos en dos partes, una para el entrenamiento y otra para la evaluación de los
# resultados (últimos 30 días)
n_split = int(X.shape[0] - 30)

X_train = X[:n_split, :]
y_train = y[:n_split]

X_test = X[n_split:, :]
y_test = y[n_split:]

# Se crea el modelo a utilizar para predecir
bosque = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    min_samples_split=2,
    min_samples_leaf=1,
    oob_score=True,
    n_jobs=-1,
    random_state=42
)

bosque.fit(X_train, y_train)
    
y_test_pred = bosque.predict(X_test)
y_train_pred = bosque.predict(X_train)

# Con el modelo de One-Step ya entrenado, se utiliza el método recursivo para hacer Multi-Step Prediction
y_ms_test_pred = []
x = X_test[0, :]

for i in range(y_test.size):
    y_os_pred = bosque.predict(x.reshape(1,-1))
    y_ms_test_pred.append(y_os_pred)
    x = np.append(x[1:], y_os_pred)

y_test_pred_ms = np.array(y_ms_test_pred)
y_train_pred_ms = bosque.predict(X_train)
