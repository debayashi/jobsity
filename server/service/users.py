from server.util.mongodb import Mongodb
from server.exceptions import UserNotFound


class Users:

    def __init__(self):
        mongo_db = Mongodb()
        self.db = mongo_db.db
        self.users = self.db.users

    def register_user(self, user, password, email):
        from server.app import bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.users.insert_one({
            "user": user,
            "password": hashed_password,
            "email": email
        })

    def authenticate_user(self, email, password):
        from server.app import bcrypt
        user = self.users.find_one({'email': email})
        if bcrypt.check_password_hash(user['password'], password):
            return user
        raise UserNotFound
