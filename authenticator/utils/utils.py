import json
import time
import uuid


def get_current_time():
    return int(time.time()) * 1000


def generate_auth_token():
    return str(uuid.uuid4()).split("-")[0]


def read_config():
    with open("config.json") as fp:
        data = json.load(fp)
    return data


def get_expiration_time(creation_time):
    with open("config.json") as fp:
        data = json.load(fp)
    expiration_time = int(data["default"]["expiration_time"])
    return creation_time + expiration_time


def check_user_longevity(expiration_time):
    if expiration_time <= int(time.time()) * 1000:
        return False
    else:
        return True
