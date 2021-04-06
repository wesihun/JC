import pymysql

class MySQL(object):
    def __init__(self, host='127.0.0.1',user='root',password='123!@#',db='oa'):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def getConnection(self):
        connection = pymysql.connect(self.host, self.user, self.password, self.db)
        return connection

    def closeConnection(self, connection):
        connection.close()


class MySQLService(object):
    def __init__(self): pass

    def getData(self):
        mySQL = MySQL()

        try:
            connection = mySQL.getConnection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            cursor.execute("select * from tb_role")

            data = cursor.fetchall()
            print(data)
        except Exception as error:
            print(error.with_traceback())

        finally:
            mySQL.closeConnection(connection)

        return data


