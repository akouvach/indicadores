import sqlite3
import os

import pandas as pd
from datetime import datetime, date

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


def getMisTablas(tabla=None):
    try:
        if not tabla:
            stmt = """select * from mistablas;"""
            records = dbEjecutar(stmt)
            return records
        else:
            stmt = """select name as tabla from sqlite_master 
                where type in ('table','view') 
                and tbl_name = ?"""
            data_tuples = (tabla,)
            records = dbEjecutar(stmt,data_tuples)
            return records

    except Exception as error:
        print("--Error while getMisTablas", error)


def getVariablesData():
    try:
        records = dbEjecutar("Select * from variables")
        return records

    except Exception as error:
        print("--Error while getVariablesData", error)


def getIndicadoresData(indicador=0):
    try:
        cnx = openDb()
        if not indicador or indicador==0:
            stmt = "Select * from indicadores"
        else:
            stmt = "Select * from indicadores where id = " + str(indicador)
        rdo = pd.read_sql_query(stmt, cnx)
        return rdo

    except Exception as error:
        raise("--Error while getIndicadoresData" + error)





def getUltimosPromediosFechas(ultimos=10):
    try:
        stmt = """Select distinct fecha 
            FROM
            (
            Select indicadorId, fecha, 
            (Select max(fecha) as maxima from indicadoresValores) as ultima,
            julianday((Select max(fecha) as maxima from indicadoresValores)) - julianday(fecha) as dif,
            avg(valor) as promedio, avg(valorPonderado) as promedioponderado 
            from indicadoresValores 
            group by indicadorid, fecha
            ) TEMPO 
            where dif<=?"""
        data_tuple = (ultimos,)
        rdo = dbEjecutar(stmt,data_tuple)
        return rdo

    except Exception as error:
        raise("--Error while getultimosPromediosFecha" + str(error))


def getUltimosPromediosIndicadores(ultimos=10):
    try:
        stmt = """Select distinct indicadores.* 
            FROM
            (
            Select indicadorId, fecha, 
            (Select max(fecha) as maxima from indicadoresValores) as ultima,
            julianday((Select max(fecha) as maxima from indicadoresValores)) - julianday(fecha) as dif,
            avg(valor) as promedio, avg(valorPonderado) as promedioponderado 
            from indicadoresValores 
            group by indicadorid, fecha
            ) TEMPO inner join indicadores on (tempo.indicadorId = indicadores.id) 
            where dif<=?"""
        data_tuple = (ultimos,)
        rdo = dbEjecutar(stmt,data_tuple)
        return rdo

    except Exception as error:
        raise("--Error while getultimosPromediosFecha" + str(error))

def getUltimosPromedios(ultimos=10):
    try:
        stmt = """Select tempo.* 
            FROM
            (
            Select 'v' as type, indicadorId, fecha,
            (Select max(fecha) as maxima from indicadoresValores where esPrediccion=0) as ultima,
            julianday((Select max(fecha) as maxima from indicadoresValores where esPrediccion=0)) - julianday(fecha) as dif,
            avg(valor) as promedio, avg(valorPonderado) as promedioponderado 
            from indicadoresValores 
			where esPrediccion = 0
            group by indicadorid, fecha
			union
			Select 'p' as type, indicadorId, fecha,
            (Select max(fecha) as maxima from indicadoresValores where esPrediccion=1) as ultima,
            julianday((Select max(fecha) as maxima from indicadoresValores where esPrediccion=1)) - julianday(fecha) as dif,
            avg(valor) as promedio, avg(valorPonderado) as promedioponderado 
            from indicadoresValores 
			where esPrediccion = 1
			and julianday(fecha) > (Select julianday(max(fecha)) as maxima from indicadoresValores where esPrediccion=0)
            group by indicadorid, fecha
            ) TEMPO 
            where dif<=? 
            order by indicadorId, type desc, fecha"""
        data_tuple = (ultimos,)
        rdo = dbEjecutar(stmt,data_tuple)
        return rdo

    except Exception as error:
        raise("--Error while getultimosPromedios" + error)

def getIndicadoresAKData(indicador=0):
    try:
        if(indicador==0):
            stmt = "Select * from indicadores"
        else:
            stmt = "select * from indicadores where id = " + str(indicador)
        rdo = dbEjecutar(stmt)
        return rdo

    except Exception as error:
        raise("--Error while getIndicadoresAKData" + error)


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
### Juntarla con getIndicadoresValoresData
def getResultados(l_indicador=0, ultimos=0):
    try:
        stmt = ""
        if(l_indicador==0):
            
            stmt = "select * from IndicadoresValores order by fecha desc "
        else:
            stmt = "select * from IndicadoresValores where indicadorId = " + str(l_indicador) + " order by fecha desc "
        if(ultimos!=0):
            #le agrego el limit de 100
            stmt = stmt + " limit 100; "
        records = dbEjecutar(stmt)
        return records

    except Exception as error:
        print("Error al recuperar los resultados de los indicadores..", error)
###

def getPredicciones(l_indicador, l_grupo):
    try:

        sqlite_query = """select fecha,valor,valorPonderado from IndicadoresValores 
        where esPrediccion = 1 and indicadorId = ? and grupo = ? 
        order by fecha desc limit 100;"""

        data_tuple = (l_indicador, l_grupo)

        rdo = dbEjecutar(sqlite_query, data_tuple)
        if not rdo:
            return None
        else:
            return rdo

    except Exception as error:
        print("--Error while obtainin predictions", error)
        raise Exception("Error al obtener predicciones")



def getValoresPonderados(indicador, valor):
    try:
        # TODO: El predictor futuro actualmente funciona para predecir de la actualidad en adelante.
        # Cuando se cambie eso, se deberá modificar este query para buscar la fecha de interés
        cnx = openDb()
        stmt = "Select * from ponderaciones"
        stmt += f" where indicadorid = {indicador} and valorHasta >= {valor[0]}"
        stmt += " order by valorHasta asc, fechaDesde desc limit 1"

        rdo = pd.read_sql_query(stmt, cnx)
        return rdo

    except Exception as error:
        print("--Error while getValorPonderado", error)


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


def deleteResultadosData():
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()
        cursor.execute("Delete from variablesValores;")
        cursor.execute("Delete from indicadoresValores;")
        dbConn.commit()
        cursor.close()
        return True

    except Exception as error:
        print("--Error while deleteResultadosData", error)

    finally:
        if dbConn:
            closeDb(dbConn)


def deleteVariablesValoresData(l_variableId, l_fecha, l_grupo):
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()

        sqlite_delete_query = """Delete from variablesValores
            where variableId = ? and fecha = ? and grupo =?;"""

        data_tuple = (l_variableId, l_fecha, l_grupo)
        count = cursor.execute(sqlite_delete_query, data_tuple)
        dbConn.commit()
        cursor.close()

    except Exception as error:
        print("--Error while deleteVariablesValoresData", error)
        raise Exception("Error al eliminar VariablesValores")

    finally:
        if dbConn:
            closeDb(dbConn)


def deleteIndicadoresValoresData(l_indicadorId, l_grupo, l_fecha):
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()

        sqlite_delete_query = """Delete from indicadoresValores where
            indicadorId = ? and grupo = ? and fecha = ?;"""

        data_tuple = (l_indicadorId, l_grupo, l_fecha)
        count = cursor.execute(sqlite_delete_query, data_tuple)
        dbConn.commit()
        cursor.close()

    except Exception as error:
        print("--Error while deleteIndicadoresValoresData", error)
        raise Exception("Error al eliminar IndicadoresValores")

    finally:
        if dbConn:
            closeDb(dbConn)


def deleteIndicadoresValoresDataFrameData(indicador, grupo, fecha_actual):
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()

        sqlite_insert_query = """delete from indicadoresValores
            where indicadorId = ? and grupo = ? and Fecha >= ? and esPrediccion = 1;"""

        data_tuple = (int(indicador), grupo, fecha_actual)
        count = cursor.execute(sqlite_insert_query, data_tuple)
        dbConn.commit()
        cursor.close()

    except Exception as error:
        print("--Error while deleteIndicadoresValoresDataFrameData", error)
        raise Exception("Error al borrar predicción de indicadores")

    finally:
        if dbConn:
            closeDb(dbConn)


def deleteIndicadoresValoresPivotData():
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()

        sqlite_insert_query = """delete from indicadoresValoresPivot;"""

        count = cursor.execute(sqlite_insert_query)
        dbConn.commit()
        cursor.close()

    except Exception as error:
        print("--Error while deleteIndicadoresValoresPivotData", error)
        raise Exception("Error al borrar indicadores valores pivot")

    finally:
        if dbConn:
            closeDb(dbConn)


def deleteAttitionData(fecha):
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()

        sqlite_insert_query = """delete from employeeAttrition
            where date = ?;"""

        data_tuple = (fecha,)
        count = cursor.execute(sqlite_insert_query, data_tuple)
        dbConn.commit()
        cursor.close()

    except Exception as error:
        print("--Error while deleteAttitionData", error)
        raise Exception("Error al borrar Attrition")

    finally:
        if dbConn:
            closeDb(dbConn)


def insertVariablesValoresData(l_variableId, l_fecha=datetime.today(), l_grupo="", l_valor=-1, l_essimulacion=0):
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


def insertIndicadoresValoresDataFrameData(data_frame):
    try:
        dbConn = openDb()
        data_frame.to_sql("indicadoresValores", dbConn, if_exists="append", index=False)
        dbConn.commit()

    except Exception as error:
        print("--Error while insertIndicadoresValoresDataFrameData", error)
        raise Exception("Error al insertar IndicadoresValores")

    finally:
        if dbConn:
            closeDb(dbConn)


def insertIndicadoresValoresPivotData(data_frame):
    try:
        dbConn = openDb()
        data_frame.to_sql("indicadoresValoresPivot", dbConn, if_exists="append", index=False)
        dbConn.commit()

    except Exception as error:
        print("--Error while insertIndicadoresValoresPivotData", error)
        raise Exception("Error al insertar IndicadoresValoresPivot")

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
        if not rdo:
            return -1
        else:
            return rdo
    except Exception as error:
        print("Error obteniendo el valor de un indicador...",error)
            
def getIndicador(l_indicadorId):
    try:
        stmt = "select * from indicadores where id = ?"
        data_tuple = (l_indicadorId, )
        rdo = dbEjecutar(stmt, data_tuple)
        if not rdo:
            return -1
        else:
            return rdo
    except Exception as error:
        raise("Error obteniendo los datos de un indicador..." + error)

def getIndicadorVariables(l_indicadorId):
    try:
        indi = dbEjecutar("select formula from indicadores where id = ?",(l_indicadorId,) )
        print(indi)
        vars = getVariableList(indi[0][0])
        lista = ""
        stmt = "select * from variables where id in ("
        for v in vars:
            if lista != "":
                lista = lista + ", "
            lista = lista +  "'" + v + "'"
        print(lista)
        stmt = stmt + lista + ")"
        rdo = dbEjecutar(stmt)
        if not rdo:
            return -1
        else:
            return rdo
    except Exception as error:
        raise("Error obteniendo las variables asociadas para un indicador:" + error)

def getPonderacionIndicador(l_indicadorId, l_fecha=datetime.today(), l_valorHasta=-1):
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
        # data_tuple = (l_indicadorId, l_indicadorId, l_fecha.strftime("%Y-%m-%d"), l_valorHasta)
        data_tuple = (l_indicadorId, l_indicadorId, l_fecha, l_valorHasta)
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
        indicador = getIndicadoresAKData(l_indicadorId)
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
