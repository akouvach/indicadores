# import mysql.connector
import json
from flask import Flask
from flask import Response
from flask import request
from flask import render_template

import Solver.db as db1

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
  print("el indicador es:", nroIndicador)
  cursor = db1.getResultados(nroIndicador)
  # content = "{" + '"' + "data" + '"' + ":" + json.dumps(cursor) + "}"
  json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
  content = "{" + '"' + "data" + '"' + ":" + json_object + "}"
  # content =  json_object 
  # print(json_object)
  # json_object = "{" + '"' + "data" + '"' + ":" + json.loads([dict(ix) for ix in cursor])+ "}"

  # return content

  return Response(content, 
            mimetype='application/json',
            headers={'Content-Disposition':'attachment;filename=indicadores.json'})


@app.route('/resultados_pivot/<int:nroIndicador>/')
@app.route('/resultados_pivot/')
def resultados_pivot(nroIndicador=0):  
  print("el indicador es:", nroIndicador)
  cursor = db1.getResultados_pivot(nroIndicador)
  # content = "{" + '"' + "data" + '"' + ":" + json.dumps(cursor) + "}"
  json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
  content = "{" + '"' + "data" + '"' + ":" + json_object + "}"
  # content =  json_object 
  # print(json_object)
  # json_object = "{" + '"' + "data" + '"' + ":" + json.loads([dict(ix) for ix in cursor])+ "}"

  # return content

  return Response(content, 
            mimetype='application/json',
            headers={'Content-Disposition':'attachment;filename=indicadores.json'})


@app.route('/sources/<nombre>/')
def getSources(nombre=''): 
  misTablas = db1.getMisTablas()
  encontrado=False
  for n in misTablas:
    if nombre == n[0]:
      encontrado=True
      break
  print("encontrado",encontrado)

  if encontrado:
    cursor = db1.getTabla(nombre)
    # content = "{" + '"' + "data" + '"' + ":" + json.dumps(cursor) + "}"
    json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
    content = "{" + '"' + "data" + '"' + ":" + json_object + "}"
  else:
    content = "Tabla no encontrada"
  
  return Response(content, mimetype='application/json')

@app.route('/sources')
def getTablas(): 
  cursor = db1.getMisTablas()
  json_object = json.dumps([dict(ix) for ix in cursor], indent=2)
  content = "{" + '"' + "data" + '"' + ":" + json_object + "}"

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



# app = Flask(__name__)

# @app.route('/')
# def index():
#     return '<h1>Hello man</h1>'


# @app.route('/<name>')
# def name(name):
#     return '<h1>Hello {}</h1>'.format(name)