import socketio
import re
from bot_server.bot import Bot


sio = socketio.Client()
print('Created socketio client')


@sio.on('connect', namespace='/test')
def on_connect():
    print('connected to server')


@sio.on('chat_message', namespace='/test')
def message(msg):
    if msg['data'].startswith("/"):
        bot = Bot()
        if re.search('^\/stock=', msg['data']):
            bot.handle_stock_command(msg['data'])


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('http://0.0.0.0:5000', namespaces=['/test'])
sio.wait()
