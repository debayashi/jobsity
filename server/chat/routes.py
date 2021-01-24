from flask import (render_template, Blueprint)
from server.models import ChatHistory

chat = Blueprint('chat', __name__)


@chat.route('/chat')
def initial_chat():
    chat_history = ChatHistory()
    old_messages = chat_history.get_room_messages()
    return render_template('chat.html', messages=old_messages)
