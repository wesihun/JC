# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, send_from_directory
from flask import request
from flask_cors import *

from api import api  # 导入蓝本的文件
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

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
    if verify_auth_token(token) is None:  # return 有值则终止后面程序的执行. return后面无值则继续向后执行
        return {'errorcode': '10001', 'message': 'token expire error'}


@app.route('/apiv1.0/login', methods=['get', 'post'])
def login():
    if request.values.get('username') is None or request.values.get('password') is None:
        return {'errorcode': '10002', 'message': 'requie user and pass'}

    username = request.values.get('username')
    password = request.values.get('password')

    if username == 'tom' and password == '123':
        token = generate_token(password, 60 * 60)  # 秒
        return {'username': 'tom', 'password': '123', 'token': token}
    else:
        return {'errorcode': '10003', 'message': 'login error'}


def generate_token(password='123', expiration=60 * 10):  # 生成token
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'password': password}).decode('ascii')
    return token


def verify_auth_token(token):  # token验证
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token,but expired
    except BadSignature:
        return None  # invalid token

    return data['password']


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=32768)
