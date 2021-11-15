# PETL (Personal ETL)

Today most of our data is hostage by Big Tech, although most services do offer ways to pull all your personal data, it normally takes several manual steps to do it. This project tries to automate the process of pulling all personal data into our own databases.

You probably want to fork this and adapt to your own need. If you do and need help, let me know.

## Goals

- Pull the data I'm insterested in keeping
- Save the data in a local database (no Cloud)
- Build a full text search on top of it with a proper protobuf API
- Build [checkers](https://www.github.com/era/malleable-checker) based on the data

## Tools

This project introduces a decorator to automatically save the output of a function into a table. The syntax works like:

```python

from typing import List, Any
import petl.decorator as petl

@petl.append(TABLE_NAME, [COLUMN_NAME_1, COLUMN_NAME_2])
def pull_data_from_source() -> List[List[Any]]:
    return my_data

```

If you need to know the last time the ETL run so you can avoid fetching all the data again, you can pass a third parameter to the decorator:

```python

from typing import List, Any
import petl.decorator as petl

@petl.append(TABLE_NAME, [COLUMN_NAME_1, COLUMN_NAME_2], COLUMN_WITH_UPDATED_DATE)
def pull_data_from_source(**kargs) -> List[List[Any]]:
    if kwargs[petl.COL_MAX_UPDATED_DATE] != None:
        # we just did somework so fetch only starting from kwargs[petl.COL_MAX_UPDATED_DATE]
        return fetch_data(start_time=kwargs[petl.COL_MAX_UPDATED_DATE])
    else:
        return fetch_all_data()

```

In the package you already have a twitter_etl, to run you need to copy config.ini.example to config.ini, add your twitter api token and a path for your sqlite3 database.

To run the package:

```

python3 setup.py install
CONFIG=PATH_TO_YOUR_CONFIG python3 petl/twitter_etl.py

```

To create the tables needed for the ETL job you can use the `create_tables.sql`file.