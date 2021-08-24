import sqlite3
import os

import pandas as pd
#from Solver.db import ...


def create_pivot_table(data):
    group_column = data["grupo"].str.split(";", expand=True)
    if group_column.shape[1] < 10:
        _rows = group_column.shape[0]
        _cols = 10 - group_column.shape[1]
        temp_df = pd.DataFrame([[None]*_cols]*_rows)
        group_column = pd.concat([group_column, temp_df], axis=1)
    pivot_table = pd.concat([data, group_column], axis=1)
    return pivot_table


if __name__ == "__main__":
    indicadores_file = "indicadores.db"
    cnx = sqlite3.connect(os.path.abspath(indicadores_file))

    data = pd.read_sql_query("SELECT * FROM indicadoresValores", cnx)
    data = data[data["esSimulacion"] == 0]
    data.dropna(axis=0, inplace=True)

    pivot_table_test = create_pivot_table(data)
    breakpoint()
