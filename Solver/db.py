import sqlite3
import os

import pandas as pd
from datetime import datetime

from Solver.varios import getVariableList

DBNAME = "DataModel/indicadores.db"

def openDb():
    try:
        sqliteConnection = sqlite3.connect(os.path.abspath(DBNAME))
        sqliteConnection.row_factory = sqlite3.Row
        return sqliteConnection

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        raise Exception("error en la conexión de la base de datos")

def closeDb(conn):
    try:
        conn.close()
        return True
        
    except sqlite3.Error as error:
        print("Error while closing", error)
        raise Exception("error en el cierre de la base de datos")


def crearYcargarDb():
    try:
        print("----------creando y cargando datos en bd...----------")
        dbConn = openDb()
        cursor = dbConn.cursor()
        sql_file = open("populate.sql")
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)
        print("se terminó de cargar los datos..")
    except sqlite3.Error as error:
        print("Error while crearYCargarDB", error)
        raise Exception("Error en la carga de base de datos")
    finally:
        if dbConn:
            closeDb(dbConn)

def dbEjecutar(stmt, data_tuple=()):
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()
        if len(data_tuple) == 0:
            cursor.execute(stmt)
        else:
            cursor.execute(stmt,data_tuple)
        record = cursor.fetchall()
        cursor.close()
        dbConn.commit()
        return record

    except sqlite3.Error as error:
        print("Error while dbEjecutar", error)
        raise Exception("error en la ejecucion en la base de datos")
    finally:
        if dbConn:
            closeDb(dbConn)


def getAttritionData():
    try:
        cnx = openDb()
        rdo = pd.read_sql_query("Select * from ST_d3_data_set", cnx)
        return rdo
    except Exception as error:
        print("Error obteniendo el valor de datos de attition...",error)


def getIndicadoresValoresData():

    try:
        cnx = openDb()
        # rdo = pd.read_sql_query("Select * from ST_d2_general_data", cnx)
        rdo = pd.read_sql_query("Select * from indicadoresValores", cnx)
        return rdo
    except Exception as error:
        print("Error obteniendo el valor de datos de indicadoresValores...",error)


def getDbVersion():
    try:
        record = dbEjecutar("select sqlite_version();")
        print("SQLite Database Version is: ", record)
        return record
    except sqlite3.Error as error:
        print("error obtaining de version")

def eliminarResultados():
    try:
        records = dbEjecutar("delete from variablesValores;")
        records = dbEjecutar("delete from indicadoresValores;")
        return records

    except Exception as error:
        print("Error al eliminar indicadores valores..",error)

def getVariables():
    try:
        records = dbEjecutar("select * from variables;")
        return records

    except Exception as error:
        print("Error al recuperar las variables..",error)

def getResultados(l_indicador=0):
    try:
        stmt = ""
        if(l_indicador==0):
            stmt = "select * from IndicadoresValores;"
        else:
            stmt = "select * from IndicadoresValores where indicadorId = " + str(l_indicador) + ";"
        records = dbEjecutar(stmt)
        return records

    except Exception as error:
        print("Error al recuperar los resultados de los indicadores..",error)

def getResultados_pivot(l_indicador=0):
    try:
        stmt = ""
        if(l_indicador==0):
            stmt = "select * from indicadoresValoresPivot;"
        else:
            stmt = "select * from indicadoresValoresPivot where indicadorId = " + str(l_indicador) + ";"
        records = dbEjecutar(stmt)
        return records

    except Exception as error:
        print("Error al recuperar los resultados de los indicadores_pivot..",error)

def getMisTablas():
    try:
        stmt = "select * from mistablas order by tabla;"
        records = dbEjecutar(stmt)
        return records

    except Exception as error:
        print("Error al recuperar las tablas existentes",error)

def getTabla(nombre):
    try:
        stmt = "select * from " + nombre + ";"# + " limit 100;"
        records = dbEjecutar(stmt)
        return records

    except Exception as error:
        print("Error al recuperar el valor de la tabla " + nombre,error)

def getIndicadores(indicador=0):
    try:
        stmt = "select * from indicadores"
        if(indicador!=0):
            stmt += " where id = ?" 
            data_tuple = (indicador,)
            records = dbEjecutar(stmt,data_tuple)
        else:
            records = dbEjecutar(stmt)
        return records

    except Exception as error:
        print("Error al recuperar los indicadores..",error)


def variablesValoresInsert(l_variableId,l_fecha=datetime.today(), l_grupo = '', l_valor=-1, l_essimulacion=0):
    try:
        # print("inserting in valoresVariables...")
        dbConn = openDb()
        cursor = dbConn.cursor()

        sqlite_insert_query = """INSERT INTO variablesValores
                            (variableId, fecha, grupo, valor, essimulacion) 
                            VALUES (?,?,?,?,?);"""
        data_tuple = (l_variableId, l_fecha, l_grupo, l_valor, l_essimulacion)
        count = cursor.execute(sqlite_insert_query,data_tuple )
        dbConn.commit()

        # print("Insert Total rows are:  ", count)
        cursor.close()
        
    except sqlite3.Error as error:
        print("Error while inserting to  variablesValores", error)
        
    finally:
        if dbConn:
            closeDb(dbConn)
            #print("The SQLite connection is closed")


def attritionDataInsert(data, fecha=datetime.today().strftime('%Y-%m-%d')):
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()

        for row in data.iterrows():
            sqlite_insert_query = """INSERT INTO employeeAttrition
                (employee_id, date, attrition_value)
                VALUES (?,?,?);"""
            data_tuple = (row[1]["EmployeeNumber"], fecha, row[1]["probability"])
            count = cursor.execute(sqlite_insert_query, data_tuple)

        dbConn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while inserting to employeeAttrition table", error)        
    finally:
        if dbConn:
            closeDb(dbConn)


def indicadoresValoresInsert(l_indicadorId,l_grupo="", l_fecha=datetime.today(), l_valor=-1, l_essimulacion=0, l_valorPonderado = -1):
    try:
        #print("inserting in IndicadoresVariables...\n")
        dbConn = openDb()
        cursor = dbConn.cursor()

        sqlite_insert_query = """INSERT INTO indicadoresValores
                            (indicadorId, grupo,fecha, valor, essimulacion, valorPonderado) 
                            VALUES (?,?,?,?,?,?);"""
        data_tuple = (l_indicadorId, l_grupo,l_fecha, l_valor, l_essimulacion, l_valorPonderado)
        count = cursor.execute(sqlite_insert_query,data_tuple )
        dbConn.commit()

        #print("Insert indicadores are:  ", count)
        cursor.close()
        
    except sqlite3.Error as error:
        print("Error while inserting to  indicadoresValores", error)
        raise Exception("error al insertar IndicadoresValores")
    finally:
        if dbConn:
            closeDb(dbConn)
            #print("The SQLite connection is closed")





def getValorIndicador(l_indicadorId, l_fecha = datetime.today(),l_essimulacion=0):
    try:
        stmt = """
            select vv.grupo,vv.valor 
            from 
            (select * from variablesValores where variableId = ?) vv
            inner join (select max(fecha) as maxFecha from variablesValores 
            where variableId = ? and fecha<=?) ult
            on (vv.fecha = ult.maxFecha)"""
        data_tuple = (l_indicadorId, l_indicadorId, l_fecha.strftime("%Y-%m-%d %H:%M:%S.%f"))
        rdo = dbEjecutar(stmt, data_tuple)
        #print("resultado:",rdo)
        if not rdo:
            return -1
        else:
            return rdo
    except Exception as error:
        print("Error obteniendo el valor de un indicador...",error)
            
def getPonderacionIndicador(l_indicadorId, l_fecha = datetime.today(), l_valorHasta=-1):
    try:
        stmt = """
            Select i.ponderacion
            from 
            (select * from ponderaciones where indicadorid=?) i
            inner join 
            (select indicadorId,max(fechaDesde) as maxFecha 
            from ponderaciones where indicadorid = ? and fechaDesde <= ?) ultFecha
            on (ultFecha.indicadorid = i.indicadorId and i.fechaDesde = ultFecha.maxFecha)
            where valorHasta > ?
            order by valorHasta asc
            limit 1"""
        data_tuple = (l_indicadorId, l_indicadorId, l_fecha.strftime("%Y-%m-%d %H:%M:%S.%f"), l_valorHasta)
        rdo = dbEjecutar(stmt, data_tuple)
        #print("resultado ponderaciones:",rdo)
        if not rdo:
            return -1
        else:
            return rdo
    except Exception as error:
        print("Error obteniendo la ponderación del indicador", error)

def getGruposIndicador(l_indicadorId, l_fecha = datetime.today()):
    try:
        #voy a buscar la variables que componen a un indicador
        indicador = getIndicadores(l_indicadorId)
        formula = indicador[0][2]
        variables = getVariableList(formula)
        filtroIndicadores =""
        for v in variables:
            if(filtroIndicadores!=""):
                filtroIndicadores+=","
            filtroIndicadores += "'" + v + "'"
        #print("filtro indicadores",filtroIndicadores)

        stmt = """
            select distinct vv.grupo 
            from 
            (select * from variablesValores where variableId in ({variables}) ) vv
            inner join (select variableId ,max(fecha) as maxFecha from variablesValores 
            where variableId in ({variables}) and fecha<=? group by variableId) ult
            on (vv.fecha = ult.maxFecha and vv.variableId = ult.variableID)"""
        #reemplazo {variables} con la lista separada por comas de 
        #variables que participan de la formula de un indicador
        stmt = stmt.replace("{variables}",filtroIndicadores)
        data_tuple = (l_fecha.strftime("%Y-%m-%d %H:%M:%S.%f"),)
        rdo = dbEjecutar(stmt, data_tuple)
        if not rdo:
            return -1
        else:
            return rdo
    except Exception as error:
        print("Error al obtener los grupos por indicador...",error)

        
    