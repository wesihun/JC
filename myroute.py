from flask import Blueprint

myroute = Blueprint('myroute', __name__, url_prefix='/myroute')

@myroute.route('/myfun1')
def myfun1():
    return 'myroute1'

@myroute.route('/myfun2')
def myfun2():
    print('myroute1')
    return 'myroute1'