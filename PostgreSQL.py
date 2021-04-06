import json
import psycopg2, psycopg2.extras

class PostgreSQL(object):
    def __init__(self):
        pass

    def getConnection(self):
        connection = psycopg2.connect(database="my_testdb", user="postgres", password="postgres", host="127.0.0.1", port="5432")
        return connection

    def closeConnection(self, connection):
        connection.close()


class PostgreSQLService(object):
    def __init__(self): pass

    def getData(self):
        postgreSQL = PostgreSQL()

        try:
            connection = postgreSQL.getConnection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)#字典

            cursor.execute("select id, name, to_char(time, 'yyyy-MM-dd hh24:mm:ss') as time from student")
            data = cursor.fetchall()

            print(data)
            print(json.dumps(data))
        except Exception as error:
            print(error.with_traceback())
        finally:
            postgreSQL.closeConnection(connection)

        return data