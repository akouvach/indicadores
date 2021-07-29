# import mysql.connector
import json
from flask import Flask
from flask import Response
import Solver.db as db1

app = Flask(__name__)

@app.route('/')
def inicio():  
  return """
  <h1>Power My Kpi</h1>

  <form action='/resultados'>
  <button>Mostrar resultados</button>
  </form>




  """
  #   <form action='/cargardatos'>
  # <button>Cargar datos</button>
  # </form>


@app.route('/resultados/')
def resultados():  
  cursor = db1.getResultados()
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



@app.route('/cargardatos')
def cargardatos():  
  cursor = db1.getResultados()
  return json.dumps(cursor)


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