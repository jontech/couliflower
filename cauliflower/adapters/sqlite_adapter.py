"""SQLite Adapter module

Here we define our sqlite back-end as Adapter which is used to store and
to manage data on sqlite database.

"""
import sqlite3


class Adapter(object):
    """SQLite Adapter implementation

    provides methods for managing data on SQLite database:
        - insert new data as record
        - select all records or using basic conditions

    TODO: Adapter class should be defined as abstract interface
          which would be subclassed by SqliteAdapter which would
          implement IO with actual SQLite.

    """

    def __init__(self, database=None):
        """Creates connection to SQLite database

        :param: database - string name of database

        """
        if '.db' not in database:
            # TODO this check should be moved to StorageForge
            database += '.db'
        self.conn = sqlite3.connect(database)

        def as_dictionary(cursor, record):
            """SQLite row representation as dict with column names as keys

            where ``cursor.description`` gets passed for every row and used
            to extract column names for record values and build dict of the
            record: {<column-name>: <record-value>}

            """
            retval = {}
            for i, col in enumerate(cursor.description):
                retval[col[0]] = record[i]
            return retval

        # set our record represented during database session
        self.conn.row_factory = as_dictionary

    def sync(self, table_name, fields):
        """Creates database table according to Model fields

        :param: table_name - string name of table
        :param: fields - list of model.Field instances

        """
        self._create_table(table_name, fields)

    def flush(self, table_name):
        """Deletes ALL table records by table name

        :param: table_name - string name of table

        """
        query = "DELETE FROM {0}".format(table_name)
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def save(self, table_name, fields):
        """Inserts new record into table

        :param: table_name - string name of table
        :param: fields - list of model.Field instances

        """
        values = [field.value for field in fields]
        query = "INSERT INTO {0} VALUES {1}".format(table_name,
                                                    tuple(values))
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def filter(self, table_name, **query_args):
        """Select records from database table

        :param: table_name - string name of table
        :param: query_args - dict representing conditions as:

            {id: 123} would be equivalent to 'where id=123' in SQL query

        :returns: list with record as column:value dict representation,
                  for more see constructor.

        """
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
        """Creates new database table

        :param: table_name - string name of table
        :param: fields - list of model.Field instances
        :param: options - dict holding options on how to create table

        """
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
