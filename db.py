import sqlite3
from datetime import datetime
import varios

DBNAME = "indicadores.db"

def openDb():
    try:
        sqliteConnection = sqlite3.connect(DBNAME)
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
        return record

    except sqlite3.Error as error:
        print("Error while dbEjecutar", error)
        raise Exception("error en la ejecucion en la base de datos")
    finally:
        if dbConn:
            closeDb(dbConn)


def getDbVersion():
    try:
        record = dbEjecutar("select sqlite_version();")
        print("SQLite Database Version is: ", record)
        return record
    except sqlite3.Error as error:
        print("error obtaining de version")

def getVariables():
    try:
        records = dbEjecutar("select * from variables;")
        return records

    except Exception as error:
        print("Error al recuperar las variables..",error)


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


def indicadoresValoresInsert(l_indicadorId,l_grupo="", l_fecha=datetime.today(), l_valor=-1, l_essimulacion=0):
    try:
        #print("inserting in IndicadoresVariables...\n")
        dbConn = openDb()
        cursor = dbConn.cursor()

        sqlite_insert_query = """INSERT INTO indicadoresValores
                            (indicadorId, grupo,fecha, valor, essimulacion) 
                            VALUES (?,?,?,?,?);"""
        data_tuple = (l_indicadorId, l_grupo,l_fecha, l_valor, l_essimulacion)
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
        variables = varios.getVariableList(formula)
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

        
    