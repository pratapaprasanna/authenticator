from flask_pymongo import PyMongo
from flask import jsonify


class MongoAdapters(object):
    def __init__(self, app):
        self.client = PyMongo(app)
        self.db = self.client.db['nomad']

    def get_all_users(self):
        collection = self.client.db['users']
        output = []
        for user in collection.find():
            output.append({'name': user['name'], 'email': user['email']})
        return jsonify({'result': output})

    def add_users(self, name, email):
        try:
            collection = self.client.db['users']
            collection_id = collection.insert({'name': name, 'email': email})
            return jsonify({'result': collection_id})
        except Exception:
            print("ISSUE")
