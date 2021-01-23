from server.util.mongodb import Mongodb


class ChatHistory:

    def __init__(self):
        mongo_db = Mongodb()
        self.db = mongo_db.db
        self.chat_coll = self.db.chat_history

    def save_message(self, message):
        self.chat_coll.insert_one({
            "message": message
        })

    def get_messages(self):
        return self.chat_coll.find({})
