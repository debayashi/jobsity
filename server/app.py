from flask import (
    Flask, render_template, session, copy_current_request_context, request,
    jsonify
)
from flask_socketio import SocketIO, emit, disconnect
from flask_login import (
    LoginManager, UserMixin, current_user, login_user, logout_user
)
from flask_session import Session
from server.users.routes import users
from server.chat.routes import chat
from server.service.chat_history import ChatHistory
from flask_bcrypt import Bcrypt


async_mode = 'gevent'
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
app.register_blueprint(chat)
app.register_blueprint(users)
login = LoginManager(app)
Session(app)
bcrypt = Bcrypt()
bcrypt.init_app(app)
socket_ = SocketIO(app, async_mode='gevent')


class User(UserMixin, object):
    def __init__(self, id=None):
        self.id = id


@login.user_loader
def load_user(id):
    return User(id)


@socket_.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socket_.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1

    chat_svc = ChatHistory()
    chat_svc.save_message(message['data'], current_user.id, '/test')

    emit('my_response',
         {'data': message['data'], 'user': current_user.id},
         broadcast=True)


@app.route('/session', methods=['GET', 'POST'])
def session_access():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return jsonify({
                'session': session.get('value', ''),
                'user': current_user.id
            })
        else:
            return None
    data = request.get_json()
    if 'session' in data:
        session['value'] = data['session']
    if 'user' in data:
        if data['user']:
            login_user(User(data['user']))
        else:
            logout_user()
    return '', 204


@socket_.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


def run_server():
    socket_.run(app, debug=True)