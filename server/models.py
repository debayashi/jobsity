from server.util.mongodb import Mongodb
from datetime import datetime
from server.exceptions import (
    UserNotFound, EmailAlreadyRegistered, WrongPassword
)


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
        if self.chat_coll.find({
            "room": '/test'
        }).count() < 50:
            return list(self.chat_coll.find({
                "room": '/test'
            }))
        return list(self.chat_coll.find({
            "room": '/test'
        }).skip(self.db.chat_history.count() - 50))


class Users:

    def __init__(self):
        mongo_db = Mongodb()
        self.db = mongo_db.db
        self.users = self.db.users

    def find_user(self, query):
        return self.users.find_one(query)

    def register_user(self, user, password, email):
        if self.find_user({'email': email}):
            raise EmailAlreadyRegistered
        from server.app import bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.users.insert_one({
            "user": user,
            "password": hashed_password,
            "email": email
        })

    def authenticate_user(self, email, password):
        from server.app import bcrypt
        user = self.find_user({'email': email})
        if not user:
            raise UserNotFound
        if bcrypt.check_password_hash(user['password'], password):
            return user
        raise WrongPassword
