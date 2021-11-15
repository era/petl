"""
usage:
@append(table="tableName", columns=['user', 'text'])
def my_function():
    my_array_of_data = grab_data()

    return my_array_of_data


# If you pass last_updated_column, it will will introduce in your **kwargs
the parameter 'updated_at' which contains the date of the last time the table was updated

@append(table="tableName", columns=['user', 'updated'], 'updated')
def my_function():
    my_array_of_data = grab_data()

    return my_array_of_data

"""

import sqlite3
import os
from configparser import ConfigParser


config_object = ConfigParser()

config_object.read(os.environ["CONFIG"])

PATH_TO_DB = config_object["SQLITE"]["PATH"]

COL_MAX_UPDATED_DATE = 'updated_at'


def insert_into(table, columns, data):
    sqlite_conn = sqlite3.connect(PATH_TO_DB)
    cur = sqlite_conn.cursor()

    columns_str = ", ".join(columns)
    placeholders = ", ".join(["?"] * len(columns))
    sql = "INSERT INTO {table} ({columns_str}) VALUES ({placeholders})".format(
        table=table, columns_str=columns_str, placeholders=placeholders
    )

    for d in data:
        cur.execute(sql, d)

    sqlite_conn.commit()
    sqlite_conn.close()

def last_updated(table, column):
    sql = 'SELECT max({column}) from {table}'.format(table=table, column=column)

    sqlite_conn = sqlite3.connect(PATH_TO_DB)
    cur = sqlite_conn.cursor()
    cur.execute(sql)
    date = cur.fetchone()
    sqlite_conn.close()
    return date[0]

def append(table, columns, last_updated_column = None):
    def wrapper(func):
        def wraps_appender(*args, **kwargs):
            if last_updated_column != None:
                kwargs[COL_MAX_UPDATED_DATE] = last_updated(table, last_updated_column)

            data = func(*args, **kwargs)
            insert_into(table, columns, data)
            return data

        return wraps_appender

    return wrapper
