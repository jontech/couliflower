# -*- coding: utf-8 -*-
import sqlite3


class Adapter(object):

    def __init__(self, database=None):
        if '.db' not in database:
            database += '.db'
        self.conn = sqlite3.connect(database)

    def sync(self, table_name, fields):
        self._create_table(table_name, fields)

    def save(self, table_name, fields):
        values = [field.value for field in fields]
        query = "INSERT INTO {0} VALUES {1}".format(table_name,
                                                    tuple(values))
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def filter(self, table_name, **query_args):
        cur = self.conn.cursor()
        if query_args:
            param_arg = lambda x: "{0}='{1}'".format(x[0], x[1])
            where_query = ','.join(map(param_arg, query_args.items()))
            query = "SELECT * FROM {0} WHERE {1}".format(table_name,
                                                         where_query)
            cur.execute(query)
        else:
            cur.execute("SELECT * FROM {0}".format(table_name))
        recs = cur.fetchall()
        return recs

    def _create_table(self, table_name, fields, **options):
        columns = []
        for field_name, field in fields.items():
            field_type = field.field_type
            columns.append('{0} {1}'.format(field_name, field_type))
        columns = ','.join(columns)
        query = ("CREATE TABLE IF NOT EXISTS {0} ({1})".format(table_name,
                                                               columns))
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
