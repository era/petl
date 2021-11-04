"""
usage:
@append(table="tableName", columns=['user', 'text'])
def my_function():
    my_array_of_data = grab_data()

    return my_array_of_data

"""

import sqlite3

PATH_TO_DB = ''

def insert_into(table, columns, data):
    sqlite_conn = sqlite3.connect(PATH_TO_DB)
    cur = sqlite_conn.cursor()

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
        data = func()
        insert_into(table, columns, data)
        return data
    
    return wrapper
