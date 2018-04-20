#!/env/python
#coding: utf-8

"""
There will be used components: python-socketio, eventlet, pymysql, flask-mysql. 
And the Flask framework is needed also.

All above components and framwork can be install by pip.
"""

import socketio
import eventlet
from flask import Flask, jsonify, render_template
from ioSpaces.MyCustomNamespace import sio, MyCustomNamespace
from flaskext.mysql import MySQL
import pymysql
from configs.database import dbConfig


sio = socketio.Server(async_mode = 'eventlet')
app = Flask(__name__)
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)
app.config['SECRET_KEY'] = 'secret!'
app.config['JSON_SORT_KEYS'] = False

for key,val in dbConfig.items():
    app.config[key] = val

mysql = MySQL( cursorclass = pymysql.cursors.DictCursor )
mysql.init_app(app)


mysql.connect()
mysql_cursor = mysql.get_db().cursor()

@app.route("/")
def hello():
    from model.UserModel import UserModel
    dbmodel = UserModel(app)
    data = dbmodel.user_list()
    return jsonify({'code': 200, 'message': '', 'data': data})
    # return render_template('index.html')

sio.register_namespace(MyCustomNamespace('/test'))
sio.register_namespace(MyCustomNamespace('/buyGrab'))

if __name__ == '__main__':
    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)