# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import current_app, request  # 在蓝本中使用配置文件引入当前环境
from MySQL import MySQLService
from flask import jsonify
from PostgreSQL import PostgreSQLService
from tree import tree
from flask_httpauth import HTTPTokenAuth

api = Blueprint('api', __name__, url_prefix='/apiv1.0')

auth = HTTPTokenAuth(scheme='Bearer')

@api.route('/myfun1', methods=['get', 'post'])
def myfun1():
    print('~~~~~~%s,%s' % (current_app.config['USER'], current_app.config['USER']))
    return '@@@@myfun1'


@api.route('/myfun2', methods=['get', 'post'])
def myfun2():
    print('myfun2')
    return 'myfun2'


@api.route('/MySQL', methods=['get', 'post'])
def MySQL():
    mySQLService = MySQLService()

    return jsonify(mySQLService.getData())


@api.route('/PostgreSQL', methods=['get', 'post'])
def PostgreSQL():
    postgreSQLService = PostgreSQLService()

    return jsonify(postgreSQLService.getData())


@api.route('/tree', methods=['get', 'post'])
def mytree():
    tr = tree()
    return jsonify(tr.get_root_department())


@api.route('/get_device', methods=['get', 'post'])
def get_device():
    """分页取得设备列表"""
    pageSize = request.values.get('pageSize')
    currentPage = request.values.get('currentPage')

    if pageSize is None or currentPage is None: return {'error': 'no pageSize currentPage'}

    postgreSQLService = PostgreSQLService()
    return jsonify(postgreSQLService.get_device_by_page(int(pageSize), int(currentPage)))


@api.route('/get_total_record', methods=['get', 'post'])
def get_total_record():
    """取得总记录数，根据表明，where条件"""
    where_sql = ''
    table_name = 'tb_device'
    postgreSQLService = PostgreSQLService()
    return jsonify(postgreSQLService.get_total_record_ether_table(table_name, where_sql))
