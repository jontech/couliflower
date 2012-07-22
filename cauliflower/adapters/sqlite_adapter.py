# -*- coding: utf-8 -*-
import sqlite3


class Adapter(object):

    def __init__(self, database=None):
        if '.db' not in database:
            database += '.db'
        self.conn = sqlite3.connect(database)

    def sync(self, fields):
        # TODO: register created tables and columns or try to get
        #       from db if there is API
        self._create_table('bla', fields)

    def save(self, values):
        query = "INSERT INTO bla VALUES {}".format(tuple(values))
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def _create_table(self, name, fields, **options):
        columns = []
        for field_name, field in fields.items():
            field_type = field.field_type
            columns.append('{0} {1}'.format(field_name, field_type))
        columns = ','.join(columns)
        query = "CREATE TABLE IF NOT EXISTS bla ({0})".format(columns)
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
