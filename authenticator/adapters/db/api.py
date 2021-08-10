from pymongo import MongoClient
from flask import jsonify

from authenticator.utils import utils


class MongoAdapters(object):
    def __init__(self, host, port):
        self.client = MongoClient(host, int(port))
        self.db = self.client["authenticator"]

    def get_all_users(self):
        collection = self.client.db["users"]
        output = []
        for user in collection.find():
            output.append({"name": user["name"], "email": user["email"]})
        return jsonify({"result": output})

    def is_valid_user(self, token):
        if self.db["users"].count_documents({"auth_token": token}) == 1:
            data = self.db["users"].find_one({"auth_token": token})
            if utils.check_user_longevity(data["expiration_time"]):
                response = {"name": data["name"], "email": data["email"]}
                return response
        else:
            return False

    def add_users(
        self,
        name,
        email,
        creation_time,
        user_type="user",
        provider=None,
        provider_id=None,
    ):
        collection = self.db["users"]
        auth_token = utils.generate_auth_token()
        count = collection.count_documents({"email": email})
        if count == 0:
            collection_id = collection.insert(
                {
                    "name": name,
                    "email": email,
                    "provider": provider,
                    "provider_id": provider_id,
                    "creation_time": creation_time,
                    "user_type": user_type,
                    "expiration_time": utils.get_expiration_time(creation_time),
                    "auth_token": auth_token,
                }
            )
            return jsonify({"result": str(auth_token)})
        else:
            return jsonify({"result": "User already signed up"})
