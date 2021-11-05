"""
usage:
@append(table="tableName", columns=['user', 'text'])
def my_function():
    my_array_of_data = grab_data()

    return my_array_of_data

"""

import sqlite3
import os
from configparser import ConfigParser


config_object = ConfigParser()

config_object.read(os.environ['CONFIG'])

PATH_TO_DB = config_object['SQLITE']['PATH']

def insert_into(table, columns, data):
    sqlite_conn = sqlite3.connect(PATH_TO_DB)
    cur = sqlite_conn.cursor()

    print(PATH_TO_DB)

    columns_str = ', '.join(columns)
    placeholders = ', '.join(['?'] * len(columns))
    sql = 'INSERT INTO {table} ({columns_str}) VALUES ({placeholders})'.format(table=table, 
                                                                                    columns_str=columns_str,
                                                                                    placeholders=placeholders)

    for d in data: 
        cur.execute(sql, d)

    sqlite_conn.commit()
    sqlite_conn.close()


def append(table, columns):
    def wrapper(func):
        def wraps_appender(*args, **kwargs):
            print('what')
            data = func(*args, **kwargs)
            insert_into(table, columns, data)
            return data
        return wraps_appender
    return wrapper
