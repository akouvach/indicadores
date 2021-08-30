import os
import json

import pandas as pd
from datetime import date, datetime

from flask import Flask, Response, request, render_template, send_from_directory, abort, jsonify

import Solver.db as db
import Solver.solver as solver
from Solver.pivot_table import create_pivot_table
from Solver.predictor_futuro import (
  create_indicador_dataframe,
  create_indicadores_dict,
  run_future_machine_learning_model
)
from Solver.predictor_attrition import (
  process_data,
  split_data,
  run_attrition_machine_learning_model,
)


app = Flask(__name__, template_folder="templates")


@app.route('/')
def inicio():  
  return render_template('index.html')

@app.route('/status')
def status():  
  param = request.ars.get("params1", "No contiene este parámetro")
  return "El parametro es {}".format(param)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
      os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )


@app.route('/inicializarbase/<fechahasta>')
@app.route('/inicializarbase/')
def inicializarbase(fechahasta=date.today()):  
  try:
    if(isinstance(fechahasta, str)):
      solver.cargarDatos(datetime.strptime(fechahasta, '%Y-%m-%d'))
    else:  
      solver.cargarDatos(fechahasta)
    return jsonify('OK')
  except Exception as error:
    return jsonify('Error calculating variables:'+error)


@app.route('/calcularvalores/<fecha>/', methods=['POST'])
@app.route('/calcularvalores/', methods=['POST'])
def calcularvalores(fecha=date.today()): 
  solver.calcularValores(fecha)
  return jsonify('OK')


@app.route('/resultados/<int:nroIndicador>/ultimos/')
def resultadosultimos(nroIndicador=0):  
  content = ""
  cursor = db.getResultados(nroIndicador,1)
  if (cursor is None):
    abort(404, description="Resource not found")
  else:
    json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
    content = "{\"data\":" + json_object + "}"

  return Response(
    content, 
    mimetype='application/json',
    headers={'Content-Disposition':'attachment;filename=indicadores.json'}
  )

@app.route('/resultados/<int:nroIndicador>/')
@app.route('/resultados/')
def resultados(nroIndicador=0):  
  content = ""
  cursor = db.getResultados(nroIndicador)
  if (cursor is None):
    abort(404, description="Resource not found")
  else:
    json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
    content = "{\"data\":" + json_object + "}"

  return Response(
    content, 
    mimetype='application/json',
    headers={'Content-Disposition':'attachment;filename=indicadores.json'}
  )


@app.route('/resultados-pivot/<int:nroIndicador>/')
@app.route('/resultados-pivot/')
def resultados_pivot(nroIndicador=0):
  # Se actualiza primero la base de datos, la tabla indicadoresValoresPivot
  cursor = db.getIndicadoresValoresData()
  data = cursor[cursor["esSimulacion"] == 0]
  data.dropna(axis=0, inplace=True)
  pivot_table_data = create_pivot_table(data)
  db.insertIndicadoresValoresPivotData(pivot_table_data)

  # Se filtran, de requerirse, los valores solicitados
  cursor_pivot = db.getIndicadoresValoresPivotData(nroIndicador)
  json_object = cursor_pivot.to_json(orient="records", indent=2)
  content = "{\"data\":" + json_object + "}"
  print("--El indicador es: {}".format(nroIndicador if nroIndicador else "Indicador no especificado"))

  return Response(
    content, 
    mimetype='application/json',
    headers={'Content-Disposition':'attachment;filename=indicadores.json'}
  )


@app.route('/sources')
def getTablas():
  cursor = db.getMisTablas()
  json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
  content = "{\"data\":" + json_object + "}"

  return Response(content, mimetype='application/json')


        
@app.route('/indicadores/<int:idIndicador>/')
def getIndicador(idIndicador):
  cursor = db.getIndicador(idIndicador)
  json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
  content = "{\"data\":" + json_object + "}"
  return Response(content, mimetype='application/json')

@app.route('/indicadores/<int:idIndicador>/variables/')
def getIndicadorvariables(idIndicador):
  cursor = db.getIndicadorVariables(idIndicador)
  json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
  content = "{\"data\":" + json_object + "}"
  return Response(content, mimetype='application/json')

@app.route('/sources/<nombre>/')
def getSources(nombre=""):
  content = ""
  print("--Buscando a: ", nombre)
  misTablas = db.getMisTablas(nombre)
  print("--misTablas: ", misTablas, len(misTablas))

  if len(misTablas) > 0:
    cursor = db.getTabla(nombre)
    print("--Cantidad de registros recuperados: ", len(cursor))
    json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
    content = "{\"data\":" + json_object + "}"
  else:
    content = "{\"data\": 'Tabla no encontrada'}"
  
  return Response(content, mimetype='application/json')


@app.route('/attrition')
def getPrediccionAttrition():
  cursor = db.getAttritionData()
  pre_process_data = process_data(cursor)
  splitted_data = split_data(pre_process_data)
  probability = run_attrition_machine_learning_model(splitted_data)
  result_df = pd.concat([cursor, probability], axis=1)

  db.insertAttritionData(result_df)
  json_df = result_df[["EmployeeNumber", "probability"]].copy()
  json_df.rename(columns={"EmployeeNumber": "employee_id", "probability": "attrition_value"}, inplace=True)
  json_df["date"] = [datetime.today().strftime('%Y-%m-%d')]*json_df.shape[0]
  json_object = json_df.to_json(orient="records", indent=2)
  content = "{\"data\":" + json_object + "}"

  return Response(
    content, 
    mimetype='application/json',
    headers={'Content-Disposition':'attachment;filename=employee_attrition_values.json'}
  )


@app.route('/kpi-prediction')
def getPrediccionFutura():
  cursor = db.getIndicadoresValoresData()
  data = cursor[cursor["esSimulacion"] == 0]
  data.dropna(axis=0, inplace=True)
  ind_dict = create_indicadores_dict(data)
  ind_df = create_indicador_dataframe(data, ind_dict)

  prediction = run_future_machine_learning_model(ind_df.items())
  breakpoint()

  data_frame_content = ""
  for indicador, data_frame in prediction.items():
    json_object = data_frame.to_json(orient="records", indent=2)
    data_frame_content = data_frame_content + f"\"{indicador}\": {json_object}"
  content = "{\"data\":[" + data_frame_content + "]}"

  return Response(
    content, 
    mimetype='application/json',
    headers={'Content-Disposition':'attachment;filename=employee_attrition_values.json'}
  )


@app.route('/test')
def getTest():
  cursor = db.getIndicadoresValoresData()
  data = cursor[cursor["esSimulacion"] == 0]
  data.dropna(axis=0, inplace=True)
  pivot_table_data = create_pivot_table(data)

  db.insertIndicadoresValoresPivotData(pivot_table_data)

  # json_df = result_df[["EmployeeNumber", "probability"]].copy()
  # json_df.rename(columns={"EmployeeNumber": "employee_id", "probability": "attrition_value"}, inplace=True)
  # json_df["date"] = [datetime.today().strftime('%Y-%m-%d')]*json_df.shape[0]
  # json_object = json_df.to_json(orient="records", indent=2)
  # content = "{\"data\":" + json_object + "}"

  # return Response(
  #   content, 
  #   mimetype='application/json',
  #   headers={'Content-Disposition':'attachment;filename=employee_attrition_values.json'}
  # )


# @app.route('/widgets')
# def get_widgets() :
#   mydb = mysql.connector.connect(
#     host="mysqldb",
#     user="root",
#     password="p@ssw0rd1",
#     database="inventory"
#   )
#   cursor = mydb.cursor()


#   cursor.execute("SELECT * FROM widgets")

#   row_headers=[x[0] for x in cursor.description] #this will extract row headers

#   results = cursor.fetchall()
#   json_data=[]
#   for result in results:
#     json_data.append(dict(zip(row_headers,result)))

#   cursor.close()

#   return json.dumps(json_data)

# @app.route('/initdb')
# def db_init():
#   mydb = mysql.connector.connect(
#     host="mysqldb",
#     user="root",
#     password="p@ssw0rd1"
#   )
#   cursor = mydb.cursor()

#   cursor.execute("DROP DATABASE IF EXISTS inventory")
#   cursor.execute("CREATE DATABASE inventory")
#   cursor.close()

#   mydb = mysql.connector.connect(
#     host="mysqldb",
#     user="root",
#     password="p@ssw0rd1",
#     database="inventory"
#   )
#   cursor = mydb.cursor()

#   cursor.execute("DROP TABLE IF EXISTS widgets")
#   cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
#   cursor.close()

#   return 'init database'

if __name__ == "__main__":
  app.run(host ='0.0.0.0')
