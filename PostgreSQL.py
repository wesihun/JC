import psycopg2
import psycopg2.extras
from flask import current_app


class PostgreSQL(object):
    def __init__(self):
        pass

    def getConnection(self):
        connection = psycopg2.connect(database=current_app.config['DATABASE'], user=current_app.config['USER'], password=current_app.config['PASSWORD'], host=current_app.config['HOST'], port=current_app.config['PORT'])
        return connection

    def closeConnection(self, connection):
        if connection: connection.close()


class PostgreSQLService(object):
    def __init__(self):
        pass

    def get_user_by_name_pass(self, username, password):
        """查询用户根据用户名和密码"""
        postgreSQL = PostgreSQL()

        try:
            connection = postgreSQL.getConnection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # 字典

            cursor.execute('''select id, username, password, to_char(createtime, 'yyyy-MM-dd hh24:mm:ss') as createtime 
                              from tb_user 
                              where username='%s' and password='%s' ''' % (username, password))
            data = cursor.fetchall()
        except Exception as error:
            print(error.with_traceback())
        finally:
            postgreSQL.closeConnection(connection)

        return data

    def get_device_by_page(self, pageSize=1, currentPage=1):
        """分页取得设备"""
        postgreSQL = PostgreSQL()

        try:
            connection = postgreSQL.getConnection()
            cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # 字典

            cursor.execute('''select tb_device_type.name as type,tb_device.id,tb_device.number,tb_device.name,tb_device.project,tb_device.person,tb_device.state,tb_device.locate
                              from tb_device_type,tb_device
                              where tb_device_type.device_type_id=tb_device.device_type_id
                              limit %d OFFSET %d''' %(pageSize, (currentPage-1)*pageSize))
            data = cursor.fetchall()
        except Exception as error:
            print(error.with_traceback())
        finally:
            postgreSQL.closeConnection(connection)

        return data