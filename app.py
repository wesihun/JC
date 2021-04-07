# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, send_from_directory, jsonify
from flask import request
from flask_cors import *
from Token import Token
from PostgreSQL import PostgreSQLService
import json
from api import api  # 导入蓝本的文件

app = Flask(__name__)

CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'hello'
app.config['JSON_AS_ASCII'] = False  # json中文
# app.config.from_object(Config)  # 指定配置文件从一个类
app.config.from_pyfile('./config.py')  # 指定配置文件
app.register_blueprint(api)  # 注册蓝本，请求路径在蓝本文件中定义。也可以在此方法中定义。


@app.before_request
def beforeRequest():
    if request.path == '/apiv1.0/login':
        return

    token = request.values.get('token')  # get，post两种类型

    if token is None:
        return {'errorcode': '10000', 'message': 'token none error'}
    if Token().verify_auth_token(token) is None:  # return 有值则终止后面程序的执行. return后面无值则继续向后执行
        return {'errorcode': '10001', 'message': 'token expire error'}


@app.route('/apiv1.0/login', methods=['get', 'post'])
def login():
    if request.values.get('username') is None or request.values.get('password') is None:
        return {'errorcode': '10002', 'message': 'requie user and pass'}

    username = request.values.get('username')
    password = request.values.get('password')

    data = PostgreSQLService().get_user_by_name_pass(username, password)
    if data:
        user_list = eval(json.dumps(data))  # 将PG返回字典转列表
        id = user_list[0].get('id')

        token = Token().generate_token(id, 60 * 60)  # 秒
        user_list[0]['token'] = token

        return jsonify(user_list)
    else:
        return {'errorcode': '10003', 'message': 'login error'}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=32768)
