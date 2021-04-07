import psycopg2
import psycopg2.extras
from flask import current_app


class PostgreSQL(object):
    def __init__(self, **args):
        self.args = args

    def getConnection(self):
        connection = psycopg2.connect(database=self.args['DATABASE'], user=self.args['USER'], password=self.args['PASSWORD'], host=self.args['HOST'], port=self.args['PORT'])
        return connection

    def closeConnection(self, connection):
        if connection: connection.close()


class PostgreSQLService(object):
    def __init__(self):
        pass

    def get_user_by_name_pass(self, username, password):
        """查询用户根据用户名和密码"""
        postgreSQL = PostgreSQL(DATABASE=current_app.config['DATABASE'], USER=current_app.config['USER'], PASSWORD=current_app.config['PASSWORD'], HOST=current_app.config['HOST'], PORT=current_app.config['PORT'])

        try:
            connection = postgreSQL.getConnection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # 字典

            cursor.execute("select id, username, password, to_char(createtime, 'yyyy-MM-dd hh24:mm:ss') as createtime from tb_user where username='%s' and password='%s'" % (username, password))
            data = cursor.fetchall()
        except Exception as error:
            print(error.with_traceback())
        finally:
            postgreSQL.closeConnection(connection)

        return data
