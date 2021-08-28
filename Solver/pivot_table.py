import sqlite3
import os

import pandas as pd


def create_pivot_table(data):
    # Diccionarios para nombres de columnas
    def change_column_names(data_frame, relative=False):
        cols_shape = data_frame.shape[1]
        if relative:
            names_changes = {i: "grupo{}".format(i+1+(10 - cols_shape)) for i in range(cols_shape)}
        else:
            names_changes = {i: "grupo{}".format(i + 1) for i in range(cols_shape)}
        data_frame.rename(columns=names_changes, inplace=True)
        return data_frame

    group_column = data["grupo"].str.split(";", expand=True)
    change_column_names(group_column)
    if group_column.shape[1] < 10:
        _rows = group_column.shape[0]
        _cols = 10 - group_column.shape[1]
        temp_df = pd.DataFrame([[None]*_cols]*_rows)
        change_column_names(temp_df, True)
        group_column = pd.concat([group_column, temp_df], axis=1)
    pivot_table = pd.concat([data, group_column], axis=1)
    return pivot_table


if __name__ == "__main__":
    indicadores_file = "indicadoresValoresTest.csv"

    data = pd.read_csv(indicadores_file)
    data = data[data["esSimulacion"] == 0]
    data.dropna(axis=0, inplace=True)

    pivot_table_test = create_pivot_table(data)
    breakpoint()
