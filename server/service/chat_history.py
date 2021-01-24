from server.util.mongodb import Mongodb
from datetime import datetime


class ChatHistory:

    def __init__(self):
        mongo_db = Mongodb()
        self.db = mongo_db.db
        self.chat_coll = self.db.chat_history

    def save_message(self, message, user, room):
        self.chat_coll.insert_one({
            "message": message,
            "user": user,
            "date": str(datetime.utcnow()),
            "room": room
        })

    def get_room_messages(self):
        return list(self.chat_coll.find({
            "room": '/test'
        }).limit(50))
