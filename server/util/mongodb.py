from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from os import environ as env
import logging


class Mongodb:
    def __init__(self):
        mongo_url = env.get('MONGODB_URL')
        mongo_user = env.get('MONGODB_USER')
        mongo_pass = env.get('MONGODB_PASS')
        mongo_auth_source = env.get('MONGODB_AUTH_SOURCE')
        mongo_auth_mecanism = env.get('MONGODB_AUTH_MECANISM')
        mongo_db = env.get('MONGODB_DB')

        try:
            client = MongoClient(mongo_url,
                                username=mongo_user,
                                password=mongo_pass,
                                authSource=mongo_auth_source,
                                authMechanism=mongo_auth_mecanism)
            self.db = client[mongo_db]

        except errors.ServerSelectionTimeoutError:
            logging.error("Error connecting in database")
            raise

        self.objectid = ObjectId
