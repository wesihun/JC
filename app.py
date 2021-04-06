# -*- coding: utf-8 -*-
from flask import Flask, render_template, session, send_from_directory
from flask import request
from flask import make_response
from flask import redirect
from flask import abort, url_for
from flask import json
from flask import jsonify
from MySQL import MySQLService
from flask_cors import *
from tree import tree
from PostgreSQL import PostgreSQLService
from user import user#导入蓝本的文件
from myroute import myroute
import config
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

app = Flask(__name__)

CORS(app,supports_credentials=True)

app.config['SECRET_KEY'] = 'hello'

app.config['JSON_AS_ASCII'] = False#json中文

# app.config.from_object(Config)  # 指定配置文件从一个类
app.config.from_pyfile('./config.py')  # 指定配置文件

app.register_blueprint(user)#注册蓝本，请求路径在蓝本文件中定义。也可以在此方法中定义。
app.register_blueprint(myroute)#注册蓝本，请求路径在蓝本文件中定义。也可以在此方法中定义。


@app.before_request
def beforeRequest():
    print('每次请求前都执行', request.path)
    # print('%s,%s,%s' %(app.config['NAME'], app.config['AGE'], app.config['TELEPHONE']))
    # print(request.cookies)#session id

    if request.path == '/login':
        return

    #token = request.args.get('token')#get请求
    #token = request.form.get('token')#post请求
    token = request.values.get('token')#get，post两种类型

    if token is None:
        return {'errorcode': '10000', 'message': 'token none error'}
    if verify_auth_token(token) is None: #return 有值则终止后面程序的执行. return后面无值则继续向后执行
        return {'errorcode': '10001', 'message': 'token expire error'}


@app.route('/login')
def login():
    # print('进入login', request.path)
    # session['name'] = 'tom'
    # print("~~~",session.get('name'))
    # return '进入login'
    if request.args.get('username') is None or request.args.get('id') is None:
        return {'errorcode': '10002', 'message': 'requie user and pass'}

    username = request.args.get('username')
    id = int (request.args.get('id'))

    if username == 'tom' and id == 1:
        token = generate_token(id, 60*30)#秒
        return {'username':'tom', 'id': 1, 'token': token}
    else:
        return {'errorcode': '10003', 'message': 'login error'}


@app.route('/', methods=['get', 'post'])
def hello_world():
    mySQLService = MySQLService()
    data = mySQLService.getData()

    return jsonify(data)
    # return 'hello world!'
    print("@@@@@@@@@@@@" ,request.path)
    return redirect(url_for('static', filename='htmls20200908/pages/jxx/index.html', _external=True))

@app.route('/getPostgreSQL', methods=['get', 'post'])
def getPostgreSQL():
    postgreSQLService = PostgreSQLService()
    data = postgreSQLService.getData()
    return jsonify(data)

@app.route('/mytree', methods=['get', 'post'])
def mytree():   #树形菜单
    tr = tree()
    root = tr.get_root_department()
    return jsonify(root)


@app.route('/sayHello/<name>')
def sayHello(name):
    return 'hello, %s' % name



@app.route('/requestFun')
def requestFun():
    user_agent = request.headers.get('User-Agent')
    return user_agent



@app.route('/fun400')
def fun400():
    return 'error', 400

@app.route('/responseFun')
def responseFun():
    response = make_response('create a cookie')
    response.set_cookie('answer', '42')
    return response


@app.route('/redirectFun')
def redirectFun():
    return redirect('http://www.baidu.com')

@app.route('/abortFun')
def abortFun():
    abort(404)
    return 'hello'


@app.errorhandler(404)
def errorPage(e):
    return render_template('404.html')

@app.errorhandler(500)
def errorPage500(e):
    return render_template('404.html'), 500


@app.route('/render_templateFun', methods=['GET','POST'])
def render_templateFun():
    return redirect(url_for('static', filename='404.html', _external=True))

@app.route('/url_for')
def url_forFun():
    # return url_for('hello_world', _external=True)
    # print('##############',url_for('static', filename='xx.js', _external=False))

    return url_for('static',filename='1594889183610.pdf' ,_external=True)



@app.route('/setsession')
def setsession():
    session['name'] = 'tom'
    return session.get('name')

@app.route('/getsession')
def getsession():
    return session.get('name')


@app.route('/getJsonData', methods=['GET','POST'])
def getJsonData():
    data = request.form['jsonTree']
    newdata = json.loads(data)

    print(type(newdata))
    print(newdata)
    #print(newdata['role_name'])

    dic = {'name': 'zhangsan', 'age': 123}

    return jsonify({'class':[dic,dic]})


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    file = request.files['file']
    file.save('c:/ff/' + file.filename)

    return 'upload success!'


@app.route('/download')
def download():
    return send_from_directory('c:/','xxx.mxd',as_attachment=True)


@app.route('/test')
def test():
    print(request.args['name'], request.args.get('password'))

    return 'sdfsdfdsf'

def generate_token(id=1, expiration=60*10):# 生成token
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'id': id}).decode('ascii')
    return token

def verify_auth_token(token):# token验证
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token,but expired
    except BadSignature:
        return None  # invalid token

    return data['id']


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=32768)





