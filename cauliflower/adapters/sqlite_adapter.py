# -*- coding: utf-8 -*-
import sqlite3


class Adapter(object):

    def __init__(self, database=None):
        if '.db' not in database:
            database += '.db'
        self.conn = sqlite3.connect(database)

    def sync(self, table_name, fields):
        # TODO: register created tables and columns or try to get
        #       from db if there is API
        self.table_name = table_name
        self._create_table(table_name, fields)

    def save(self, fields):
        values = [field.value for field in fields]
        query = "INSERT INTO {0} VALUES {1}".format(self.table_name,
                                                    tuple(values))
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def _create_table(self, name, fields, **options):
        columns = []
        for field_name, field in fields.items():
            field_type = field.field_type
            columns.append('{0} {1}'.format(field_name, field_type))
        columns = ','.join(columns)
        query = ("CREATE TABLE IF NOT EXISTS {0} ({1})".format(self.table_name,
                                                               columns))
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
