from flask import render_template, Blueprint, request, url_for
from server.service.users import Users
from server.exceptions import UserNotFound
from server.service.chat_history import ChatHistory

users = Blueprint('/', __name__)


@users.route('/')
def index():
    return render_template('index.html')


@users.route('/register', methods=['POST'])
def register_new_user():
    users = Users()
    users.register_user(
        request.form.get('name'),
        request.form.get('password'),
        request.form.get('email')
    )
    return render_template('index.html')


@users.route('/login', methods=['POST'])
def login_user():
    users = Users()
    if users.authenticate_user(
        request.form.get('email'),
        request.form.get('password')
    ):
        chat_history = ChatHistory()
        old_messages = chat_history.get_room_messages()
        return render_template('chat.html', messages=old_messages)
