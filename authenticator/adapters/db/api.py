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

    def add_users(self, name, email, provider):
        try:
            collection = self.client.db['users']
            count = collection.count_documents({'email': email})
            if count == 0:
                collection_id = collection.insert(
                    {'name': name, 'email': email, 'provider': provider})
                return jsonify({'result': str(collection_id)})
            return jsonify({'result': "User already signed up"})
        except Exception:
            print("ISSUE")
