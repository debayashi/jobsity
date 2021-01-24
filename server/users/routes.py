from flask import render_template, Blueprint, request
from server.models import Users
from server.exceptions import (
    UserNotFound, EmailAlreadyRegistered, WrongPassword
)
from flask_login import (
    UserMixin, login_user, current_user
)
from server.models import ChatHistory

users = Blueprint('/', __name__)


class User(UserMixin, object):
    def __init__(self, id=None):
        self.id = id


@users.route('/')
def index():
    if current_user.is_authenticated:
        chat_history = ChatHistory()
        old_messages = chat_history.get_room_messages()
        return render_template('chat.html', messages=old_messages)
    return render_template('index.html')


@users.route('/register', methods=['POST'])
def register_new_user():
    users = Users()
    try:
        users.register_user(
            request.form.get('name'),
            request.form.get('password'),
            request.form.get('email')
        )
    except EmailAlreadyRegistered:
        email = request.form.get('email')
        return f'<h3> User with email {email} already exists</h3>'
    return render_template('index.html')


@users.route('/login', methods=['POST'])
def login_chat():
    users = Users()
    try:
        user = users.authenticate_user(
            request.form.get('email'),
            request.form.get('password')
        )
        login_user(User(user['user']))
        chat_history = ChatHistory()
        old_messages = chat_history.get_room_messages()
        return render_template('chat.html', messages=old_messages)
    except UserNotFound:
        email = request.form.get('email')
        return f'<h3> User with email {email} not found </h3>'
    except WrongPassword:
        return '<h3> Wrong password</h3>'
