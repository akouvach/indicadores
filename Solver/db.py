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

    except Exception as error:
        print("--Error while openDb", error)
        raise Exception("Error en la conexión de la base de datos")


def closeDb(conn):
    try:
        conn.close()
        return True

    except Exception as error:
        print("--Error while closeDb", error)
        raise Exception("Error en el cierre de la base de datos")


def createDb():
    try:
        print("--Creando y cargando la base de datos")
        dbConn = openDb()
        cursor = dbConn.cursor()
        sql_file = open("populate.sql")
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)
        print("--Finaliza carga de datos en base de datos")

    except Exception as error:
        print("--Error while createDb", error)
        raise Exception("Error en la carga de base de datos")

    finally:
        if dbConn:
            closeDb(dbConn)


def dbVersion():
    try:
        record = dbEjecutar("Select sqlite_version()")
        print("--SQLite Database Version: ", record)
        return record

    except Exception as error:
        print("--Error while dbVersion")


def dbEjecutar(stmt, data_tuple=()):
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()
        if len(data_tuple) == 0:
            cursor.execute(stmt)
        else:
            cursor.execute(stmt, data_tuple)
        record = cursor.fetchall()
        cursor.close()
        dbConn.commit()
        return record

    except Exception as error:
        print("--Error while dbEjecutar", error)
        raise Exception("Error en la ejecucion en la base de datos")

    finally:
        if dbConn:
            closeDb(dbConn)


def getTabla(nombre):
    try:
        stmt = "Select * from " + nombre + " limit 100;"
        records = dbEjecutar(stmt)
        return records

    except Exception as error:
        print("--Error while getTabla {}".format(nombre), error)


def getTablas():
    try:
        stmt = "Select * from mistablas order by tabla;"
        records = dbEjecutar(stmt)
        return records

    except Exception as error:
        print("--Error while getTablas", error)


def getVariablesData():
    try:
        records = dbEjecutar("Select * from variables")
        return records

    except Exception as error:
        print("--Error while getVariablesData", error)


def getIndicadoresData(indicador=0):
    try:
        cnx = openDb()
        if not indicador:
            stmt = "Select * from indicadores"
        else:
            stmt = "Select * from indicadoresValoresPivot where id = " + str(indicador)
        rdo = pd.read_sql_query(stmt, cnx)
        return rdo

    except Exception as error:
        print("--Error while getIndicadoresData", error)


def getAttritionData():
    try:
        cnx = openDb()
        rdo = pd.read_sql_query("Select * from ST_d3_data_set", cnx)
        return rdo

    except Exception as error:
        print("--Error while getAttritionData", error)


def getIndicadoresValoresData(indicador=0):
    try:
        cnx = openDb()
        if not indicador:
            stmt = "Select * from indicadoresValores"
        else:
            stmt = "Select * from indicadoresValores where indicadorId = " + str(indicador)
        rdo = pd.read_sql_query(stmt, cnx)
        return rdo

    except Exception as error:
        print("--Error while getIndicadoresValoresData", error)


def getIndicadoresValoresPivotData(indicador=0):
    try:
        cnx = openDb()
        if not indicador:
            stmt = "Select * from indicadoresValoresPivot"
        else:
            stmt = "Select * from indicadoresValoresPivot where indicadorId = " + str(indicador)
        rdo = pd.read_sql_query(stmt, cnx)
        return rdo

    except Exception as error:
        print("--Error while getIndicadoresValoresPivotData", error)


def deleteIndicadoresValoresData():
    try:
        records = dbEjecutar("Delete from variablesValores;")
        records = dbEjecutar("Delete from indicadoresValores;")
        return records

    except Exception as error:
        print("--Error while deleteIndicadoresValoresData", error)


### Juntarla con getIndicadoresValoresData


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


###


def insertVariablesValoresData(l_variableId, l_grupo="", l_fecha=datetime.today(), l_valor=-1, l_essimulacion=0):
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()

        sqlite_insert_query = """INSERT INTO variablesValores
            (variableId, fecha, grupo, valor, essimulacion) 
            VALUES (?,?,?,?,?);"""

        data_tuple = (l_variableId, l_fecha, l_grupo, l_valor, l_essimulacion)
        count = cursor.execute(sqlite_insert_query, data_tuple)
        dbConn.commit()
        cursor.close()

    except Exception as error:
        print("--Error while insertVariablesValoresData", error)
        raise Exception("Error al insertar VariablesValores")
        
    finally:
        if dbConn:
            closeDb(dbConn)


def insertIndicadoresValoresData(l_indicadorId, l_grupo="", l_fecha=datetime.today(), l_valor=-1, l_essimulacion=0, l_valorPonderado=-1):
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()

        sqlite_insert_query = """INSERT INTO indicadoresValores
            (indicadorId, grupo, fecha, valor, essimulacion, valorPonderado) 
            VALUES (?,?,?,?,?,?);"""

        data_tuple = (l_indicadorId, l_grupo, l_fecha, l_valor, l_essimulacion, l_valorPonderado)
        count = cursor.execute(sqlite_insert_query, data_tuple)
        dbConn.commit()
        cursor.close()

    except Exception as error:
        print("--Error while insertIndicadoresValoresData", error)
        raise Exception("Error al insertar IndicadoresValores")

    finally:
        if dbConn:
            closeDb(dbConn)


def insertAttritionData(data, fecha=datetime.today().strftime('%Y-%m-%d')):
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

    except Exception as error:
        print("--Error while insertAttritionData", error)
        raise Exception("Error al insertar Attrition")

    finally:
        if dbConn:
            closeDb(dbConn)


###


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
        indicador = getIndicadoresData(l_indicadorId)
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
