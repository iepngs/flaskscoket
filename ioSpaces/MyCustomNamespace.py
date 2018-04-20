
import socketio
import json

sio = socketio.Server(async_mode = 'eventlet')

class MyCustomNamespace(socketio.Namespace):
    def __background_thread(self):
        """Example of how to send server generated events to clients."""
        sio.sleep(10)
        self.emit('reply', {'data': 'Server generated event'})


    # 监听客户端连接
    def on_connect(self, sid, environ):
        print('New client connected - {sid} '.format(sid = sid))
        self.emit('reply', {'data': 'Connected', 'count': 0}, room = sid)

    # 监听客户端断连
    def on_disconnect(self, sid):
        print('Client disconnected [ {sid} ]'.format(sid = sid))

    # ---------------------------------------------------------------------------
    # 处理给客户端ping请求
    def on_ping_from_client(self, sid):
        self.emit('pong_from_server', room = sid)

    # 处理系统消息请求
    def on_message(self, sid, message):
        print(self.namespace)
        if self.namespace == u'/buyGrab':
            try:
                requsetData = json.loads(message['data'])
            except:
                pass
            else:
                neededArgs = {
                    'uid': None,
                    'auid': None,
                    'grabid': None,
                    'num': None,
                    'sp': None,
                }
                for key, val in neededArgs.items():
                    val = requsetData.get(key)
                    if val is None:
                        self.emit('reply', {'code':400, 'message': 'Lack Of Param Or Invalid[%s]' % (key), 'data':{}})
                        return
                    neededArgs[key] = val
                from model.UserModel import UserModel
                dbmodel = UserModel(app)
                data = dbmodel.buy_grab(neededArgs)
                print(data)
                
        else:
            print('message ', message)
            if message['data'] == 'backgroud':
                sio.start_background_task(self.__background_thread)
                self.emit('reply', {'data': 'backgroud function will be trigger an event'})
                # 当前所在房间号
                # print(self.rooms(sid))
                # 当前namespace
                # print(self.namespace)
            else:
                self.emit('reply', {'data': message['data']}, room = sid)

    # 处理广播消息请求
    def on_broadcastMsg(self, sid, message):
        self.emit('reply', {'data': message['data']})

    # 处理加入房间请求
    def on_join(self, sid, message):
        self.enter_room(sid, message['room'])
        self.emit('reply', {'data': 'Entered room: ' + message['room']}, room = sid)

    # 处理离开房间请求
    def on_leave(self, sid, message):
        self.leave_room(sid, message['room'])
        self.emit('reply', {'data': 'Left room: ' + message['room']}, room = sid)

    # 处理解散房间请求
    def on_closeRoom(self, sid, message):
        self.emit('reply', 
            {'data': 'Room ' + message['room'] + ' is closing.'}, 
            room = message['room'])
        self.close_room(message['room'])

    # 处理房间消息请求
    def on_roomMsg(self, sid, message):
        self.emit('reply', {'data': message['data']}, 
            room = message['room'])

    # 处理断开连接请求
    def on_disconnectRequest(self, sid):
        self.disconnect(sid)