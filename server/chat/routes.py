from flask import (render_template, url_for, Blueprint)
from server.service.chat_history import ChatHistory

chat = Blueprint('chat', __name__)


@chat.route('/chat')
def initial_chat():
    print('mdlkwenfoiwfwejf')
    chat_history = ChatHistory()
    old_messages = chat_history.get_room_messages()
    return render_template('chat.html', messages=old_messages)
