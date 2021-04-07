# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import current_app, request  # 在蓝本中使用配置文件引入当前环境
from MySQL import MySQLService
from flask import jsonify
from PostgreSQL import PostgreSQLService
from tree import tree

api = Blueprint('api', __name__, url_prefix='/apiv1.0')


@api.route('/myfun1', methods=['get', 'post'])
def myfun1():
    print('~~~~~~%s,%s' % (current_app.config['USER'], current_app.config['USER']))
    return '@@@@myfun1'


@api.route('/myfun2', methods=['get', 'post'])
def myfun2():
    print('myfun2')
    return 'myfun2'


@api.route('MySQL', methods=['get', 'post'])
def MySQL():
    mySQLService = MySQLService()

    return jsonify(mySQLService.getData())


@api.route('PostgreSQL', methods=['get', 'post'])
def PostgreSQL():
    postgreSQLService = PostgreSQLService()

    return jsonify(postgreSQLService.getData())


@api.route('tree', methods=['get', 'post'])
def mytree():
    tr = tree()
    return jsonify(tr.get_root_department())
