from flask import Blueprint
from flask import current_app, request# 在蓝本中使用配置文件引入当前环境

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/myfun1')
def myfun1():
    request.args.get('token')
    print('~~~~~~%s,%s' %(current_app.config['NAME'], current_app.config['TELEPHONE']))
    return '@@@@myfun1'

@user.route('/myfun2')
def myfun2():
    print('myfun2')
    return 'myfun2'