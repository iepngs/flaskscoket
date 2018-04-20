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
from flaskext.mysql import MySQL
import pymysql

sio = socketio.Server(async_mode = 'eventlet')
app = Flask(__name__)
app.wsgi_app = socketio.Middleware(sio, app.wsgi_app)
app.config['SECRET_KEY'] = 'secret!'
app.config['JSON_SORT_KEYS'] = False

dbConfig = {
    'MYSQL_DATABASE_HOST': '192.168.1.150',
    'MYSQL_DATABASE_DB': 'qiyu',
    'MYSQL_DATABASE_USER': 'root',
    'MYSQL_DATABASE_PASSWORD': 'root525'
}
for key,val in dbConfig.items():
    app.config[key] = val


def background_thread():
    """Example of how to send server generated events to clients."""
    sio.sleep(10)
    sio.emit('reply', {'data': 'Server generated event'})

@app.route("/")
def hello():
    mysql = MySQL( cursorclass = pymysql.cursors.DictCursor )
    mysql.init_app(app)
    cursor = mysql.get_db().cursor()
    cursor.execute('select id uid,cellphone,nickname,sex,age,sign,user_type,init_time from qy_user limit 3')
    # executemany()方法可以一次插入多条值，执行单挑sql语句,但是重复执行参数列表里的参数,返回值为受影响的行数。
    data = cursor.fetchall()
    # rowcount: 这是一个只读属性，并返回执行execute()方法后影响的行数。
    for row in data:
        print(row)
    return jsonify({'code': 200, 'message': '', 'data': data})
    # return render_template('index.html')

    # sqli="insert into student values(%s,%s,%s,%s)"
    # cursor.execute(sqli,('3','Huhu','2 year 1 class','7'))

    # sqli="insert into student values(%s,%s,%s,%s)"
    # cur.executemany(sqli,[
    #     ('3','Tom','1 year 1 class','6'),
    #     ('3','Jack','2 year 1 class','7'),
    #     ('3','Yaheng','2 year 2 class','7'),
    #     ])

# 监听客户端连接
@sio.on('connect', namespace = '/test')
def test_connect(sid, environ):
    print('New client connected - {sid} '.format(sid = sid))
    sio.emit('reply', {'data': 'Connected', 'count': 0}, 
        room = sid, namespace = '/test')

# 监听客户端断连
@sio.on('disconnect', namespace = '/test')
def test_disconnect(sid):
    print('Client disconnected [ {sid} ]'.format(sid = sid))

# ---------------------------------------------------------------------------

# 处理给客户端ping请求
@sio.on('ping_from_client', namespace = '/test')
def ping(sid):
    sio.emit('pong_from_server', room = sid, namespace = '/test')

# 处理系统消息请求
@sio.on('message', namespace = '/test')
def test_message(sid, message):
    print('message ', message)
    if message['data'] == 'backgroud':
        sio.start_background_task(background_thread)
        sio.emit('reply', 'backgroud function will be trigger an event')
    else:
        sio.emit('reply', {'data': message['data']}, 
            room = sid, namespace = '/test')

# 处理广播消息请求
@sio.on('broadcastMsg', namespace = '/test')
def test_broadcast_message(sid, message):
    sio.emit('reply', {'data': message['data']}, namespace='/test')

# 处理加入房间请求
@sio.on('join', namespace = '/test')
def join(sid, message):
    sio.enter_room(sid, message['room'], namespace = '/test')
    sio.emit('reply', {'data': 'Entered room: ' + message['room']},
             room = sid, namespace = '/test')

# 处理离开房间请求
@sio.on('leave', namespace = '/test')
def leave(sid, message):
    sio.leave_room(sid, message['room'], namespace = '/test')
    sio.emit('reply', {'data': 'Left room: ' + message['room']},
            room = sid, namespace = '/test')

# 处理解散房间请求
@sio.on('closeRoom', namespace = '/test')
def close(sid, message):
    sio.emit('reply', 
        {'data': 'Room ' + message['room'] + ' is closing.'}, 
        room = message['room'], namespace = '/test')
    sio.close_room(message['room'], namespace = '/test')

# 处理房间消息请求
@sio.on('roomMsg', namespace = '/test')
def send_room_message(sid, message):
    sio.emit('reply', {'data': message['data']}, 
        room = message['room'], namespace = '/test')

# 处理断开连接请求
@sio.on('disconnectRequest', namespace = '/test')
def disconnect_request(sid):
    sio.disconnect(sid, namespace = '/test')

if __name__ == '__main__':
    
    # wrap Flask application with socketio's middleware
    # app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)