import json

import pandas as pd
from datetime import datetime

import Solver.db as db1
from flask import Flask, Response, request, render_template
from Solver.predictor_futuro import create_indicador_dataframe, create_indicadores_dict
from Solver.predictor_attrition import process_data, split_data, run_machine_learning_model


app = Flask(__name__, template_folder="templates")

@app.route('/')
def inicio():  
  return render_template('index.html')


@app.route('/status')
def status():  
  param = request.ars.get("params1","no contiene este parametro")
  return 'El parametro es {}'.format(param)


@app.route('/resultados/<int:nroIndicador>/')
@app.route('/resultados/')
def resultados(nroIndicador=0):
  cursor = db1.getResultados(nroIndicador)
  json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
  content = "{\"data\":" + json_object + "}"

  print("El indicador es:", nroIndicador)
  return Response(
    content, 
    mimetype='application/json',
    headers={'Content-Disposition':'attachment;filename=indicadores.json'}
  )


@app.route('/resultados_pivot/<int:nroIndicador>/')
@app.route('/resultados_pivot/')
def resultados_pivot(nroIndicador=0):
  cursor = db1.getResultados_pivot(nroIndicador)
  json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
  content = "{\"data\":" + json_object + "}"

  print("El indicador es:", nroIndicador)
  return Response(
    content, 
    mimetype='application/json',
    headers={'Content-Disposition':'attachment;filename=indicadores.json'}
  )


@app.route('/sources')
def getTablas(): 
  cursor = db1.getMisTablas()
  json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
  content = "{\"data\":" + json_object + "}"

  return Response(content, mimetype='application/json')


@app.route('/sources/<nombre>/')
def getSources(nombre=''): 
  misTablas = db1.getMisTablas()
  encontrado=False
  for n in misTablas:
    if nombre == n[0]:
      encontrado=True
      break

  if encontrado:
    cursor = db1.getTabla(nombre)
    json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
    content = "{\"data\":" + json_object + "}"
  else:
    content = "Tabla no encontrada"
  
  return Response(content, mimetype='application/json')


@app.route('/attrition')
def getPrediccionAttrition():
  cursor = db1.getAttritionData()
  pre_process_data = process_data(cursor)
  splitted_data = split_data(pre_process_data)
  probability = run_machine_learning_model(splitted_data)
  result_df = pd.concat([cursor, probability], axis=1)

  db1.attritionDataInsert(result_df)
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
  cursor = db1.getIndicadoresValoresData()
  ind_dict = create_indicadores_dict(cursor)
  ind_df = create_indicador_dataframe(ind_dict)

  machine_learning = run_machine_learning_model(ind_df.items())
  print(machine_learning)
  json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
  content = "{\"data\":" + json_object + "}"

  return Response(content, mimetype='application/json')


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
