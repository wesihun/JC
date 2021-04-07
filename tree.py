import pymysql

class MySQL(object):
    def __init__(self, host='127.0.0.1',user='root',password='123!@#',db='xx', port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port

    def getConnection(self):
        connection = pymysql.connect(self.host, self.user, self.password, self.db, self.port)
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

            cursor.execute("select * from tb_department")

            data = cursor.fetchall()
            print(data)
        except Exception as error:
            print(error.with_traceback())
        finally:
            mySQL.closeConnection(connection)

        return data

    def get_root_department(self):
        mySQL = MySQL()

        try:
            connection = mySQL.getConnection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            cursor.execute("select departmentid,departmentname,parentid from tb_department where parentid is null ")

            data = cursor.fetchall()
        except Exception as error:
            print(error.with_traceback())
        finally:
            mySQL.closeConnection(connection)

        return data

    def get_sub_department(self, departmentid=0):
        mySQL = MySQL()

        try:
            connection = mySQL.getConnection()
            cursor = connection.cursor(pymysql.cursors.DictCursor)

            cursor.execute("select departmentid,departmentname,parentid from tb_department where parentid=%d" %departmentid)

            data = cursor.fetchall()
        except Exception as error:
            print(error.with_traceback())
        finally:
            mySQL.closeConnection(connection)

        return data




class menue:
    def __init__(self, departmentid, departmentname, parentid, submenue):
        self.departmentid = departmentid
        self.departmentname = departmentname
        self.parentid = parentid
        self.submenue = submenue



class tree:
    """树形菜单"""
    def __init__(self):
        pass

    def get_root_department(self):
        """根"""
        mysqlService = MySQLService()
        root_list = []
        data = mysqlService.get_root_department()

        for menue_obj in data:
            root_menue = menue(menue_obj.get('departmentid'), menue_obj.get('departmentname'), menue_obj.get('parentid'), menue_obj.get('submenue'))

            root_menue.submenue = self.get_sub_department(root_menue.departmentid)
            root_list.append(root_menue.__dict__)

        return root_list

    def get_sub_department(self, departmentid=0):
        """叶子"""
        mysqlService = MySQLService()
        sub_list = []
        data = mysqlService.get_sub_department(departmentid=departmentid)

        if not data: #空元组
            return None
        else:
            for menue_obj in data:
                sub_menue = menue(menue_obj.get('departmentid'), menue_obj.get('departmentname'), menue_obj.get('parentid'), menue_obj.get('submenue'))

                sub_menue.submenue = self.get_sub_department(departmentid=sub_menue.departmentid)
                sub_list.append(sub_menue.__dict__)

        return sub_list
