import sqlite3
DBNAME = "indicadores.db"

def openDb():
    try:
        sqliteConnection = sqlite3.connect(DBNAME)
        print("Database connected successfully")

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
        raise Exception("error en la conexión de la base de datos")

    return sqliteConnection

def closeDb(conn):
    try:
        conn.close()
        print("Database successfully closed")

    except sqlite3.Error as error:
        print("Error while closing", error)
        raise Exception("error en el cierre de la base de datos")

    return True

def dbEjecutar(stmt):
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()
        sqlite_select_Query = stmt
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print("Resultado de la consulta: ", record)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if dbConn:
            closeDb(dbConn)
            print("The SQLite connection is closed")
    return record


def getDbVersion():
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()
        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print("SQLite Database Version is: ", record)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if dbConn:
            closeDb(dbConn)
            print("The SQLite connection is closed")



def getVariables():
    try:
        dbConn = openDb()
        cursor = dbConn.cursor()
        sqlite_select_Query = "select * from variables;"
        cursor.execute(sqlite_select_Query)


        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row", records[0])
        for row in records:
            print("Id: ", row[0])
            print("descripcion: ", row[1])
            print("formula: ", row[2])
            stmt = row[2]
            rdo = dbEjecutar(stmt)
            print("resultado de la formula:",rdo[0][0])
            print("agruparpor: ", row[3])
            print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to variables", error)
    finally:
        if dbConn:
            closeDb(dbConn)
            print("The SQLite connection is closed")










