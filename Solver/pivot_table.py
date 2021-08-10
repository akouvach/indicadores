import sqlite3

import pandas as pd
import db


cnx = sqlite3.connect("C:\\Users\\asanz\\git\\indicadores\\DataModel\\indicadores.db")
data = pd.read_sql_query("SELECT * FROM indicadoresValores", cnx)
data = data[data["esSimulacion"] == 0]
data.dropna(axis=0, inplace=True)

def create_pivot_table(data=data):
    group_column = data["grupo"]
    pivot_table = pd.concat([data, group_column.str.split(";", expand=True)], axis=1)
    return pivot_table


if __name__ == "__main__":
    pivot_table_test = create_pivot_table()
    breakpoint()
