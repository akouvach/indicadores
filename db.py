import sqlite3
from datetime import date
from datetime import datetime


DBNAME = "indicadores.db"

def openDb():
    try:
        sqliteConnection = sqlite3.connect(DBNAME)
        #print("Database connected successfully")

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        raise Exception("error en la conexión de la base de datos")

    return sqliteConnection

def closeDb(conn):
    try:
        conn.close()
        #print("Database successfully closed")

    except sqlite3.Error as error:
        print("Error while closing", error)
        raise Exception("error en el cierre de la base de datos")

    return True

def crearYcargarDb():
    try:
        print("creando y cargando datos en bd...")
        dbConn = openDb()
        cursor = dbConn.cursor()
        sql_file = open("populate.sql")
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)
        print("se terminó de cargar los datos..")
    except sqlite3.Error as error:
        print("Error while crearYCargarDB", error)
    finally:
        if dbConn:
            closeDb(dbConn)
            #print("The SQLite connection is closed")

def dbEjecutar(stmt, data_tuple=()):
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()
        if len(data_tuple) == 0:
            cursor.execute(stmt)
        else:
            cursor.execute(stmt,data_tuple)
        record = cursor.fetchall()
        #print("Resultado de la consulta: ", stmt, data_tuple, "--->", record)
        cursor.close()
        return record

    except sqlite3.Error as error:
        print("Error while dbEjecutar", error)
    finally:
        if dbConn:
            closeDb(dbConn)
            #print("The SQLite connection is closed")


def getDbVersion():
    try:
        record = dbEjecutar("select sqlite_version();")
        print("SQLite Database Version is: ", record)
        return record
    except sqlite3.Error as error:
        print("error obtainin de version")



def getVariables():
    try:
        records = dbEjecutar("select * from variables;")
        return records

    except :
        print("Error al recuperar las variables")



def getIndicadores():
    try:
        records = dbEjecutar("select * from indicadores;")
        return records

    except :
        print("Error al recuperar los indicadores")


def variablesValoresInsert(l_variableId,l_fecha, l_valor, l_essimulacion=0):
    try:
        print("inserting in valoresVariables...\n")
        dbConn = openDb()
        cursor = dbConn.cursor()

        sqlite_insert_query = """INSERT INTO variablesValores
                            (variableId, fecha, valor, essimulacion) 
                            VALUES (?,?,?,?);"""
        data_tuple = (l_variableId, l_fecha, l_valor, l_essimulacion)
        count = cursor.execute(sqlite_insert_query,data_tuple )
        dbConn.commit()

        print("Insert Total rows are:  ", count)
        cursor.close()
        
    except sqlite3.Error as error:
        print("Error while inserting to  variablesValores", error)
    finally:
        if dbConn:
            closeDb(dbConn)
            #print("The SQLite connection is closed")


def indicadoresValoresInsert(l_indicadorId,l_fecha, l_valor, l_essimulacion=0):
    try:
        print("inserting in IndicadoresVariables...\n")
        dbConn = openDb()
        cursor = dbConn.cursor()

        sqlite_insert_query = """INSERT INTO indicadoresValores
                            (indicadorId, fecha, valor, essimulacion) 
                            VALUES (?,?,?,?);"""
        data_tuple = (l_indicadorId, l_fecha, l_valor, l_essimulacion)
        count = cursor.execute(sqlite_insert_query,data_tuple )
        dbConn.commit()

        print("Insert indicadores are:  ", count)
        cursor.close()
        
    except sqlite3.Error as error:
        print("Error while inserting to  indicadoresValores", error)
    finally:
        if dbConn:
            closeDb(dbConn)
            #print("The SQLite connection is closed")



def getValorIndicador(l_indicadorId, l_fecha = datetime.today(),l_essimulacion=0):
    stmt = """
        select vv.valor 
        from 
        (select * from variablesValores where variableId = ?) vv
        inner join (select max(fecha) as maxFecha from variablesValores 
        where variableId = ? and fecha<=?) ult
        on (vv.fecha = ult.maxFecha)"""
    data_tuple = (l_indicadorId, l_indicadorId, l_fecha)
    rdo = dbEjecutar(stmt, data_tuple)
    print("resultado:",rdo)
    return rdo[0][0]
