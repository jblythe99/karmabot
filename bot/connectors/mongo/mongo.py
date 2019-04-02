from pymongo import MongoClient
from bot.base import connector

@connector.register("MONGO")
class Mongo(object):

    def get_connection(self):
        client = MongoClient('mongodb://localhost:27017')

        if not client:
            print('Mongo Database not started')
            sys.exit(1)

        return client.local

    def get_karmas(self, conn, table="karma"):
        return conn.get_collection(table)

    def pos_karma(self, karmas, user):
        karmas.update_one({"user": user}, {"$inc": {"karma": 1}})

    def neg_karma(self, karmas, user):
        karmas.update_one({"user": user}, {"$inc": {"karma": -1}})

    def add_user(self, karmas, user, username):
        karmas.insert_one({"user": user, "username": username, "karma": 0})

    def get_user(self, karmas, user):
        return karmas.find_one({"user":user})

    def get_karma(self, karmas, user):
        rec = karmas.find_one({"user": user})
        return rec['karma']




