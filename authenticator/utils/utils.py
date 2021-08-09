import json
import time


def get_current_time():
    return int(time.time()) * 1000


def read_config():
    with open("config.json") as fp:
        data = json.load(fp)
    return data
