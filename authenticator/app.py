from flask import Flask
from flask import jsonify
from flask import request

from authenticator.adapters.db import api as db_api
from authenticator import config

app = Flask(__name__)

app.config['MONGO_DBNAME'] = config.DATABASE
app.config['MONGO_URI'] = f'mongodb://{config.DB_HOST}:{config.DB_PORT}/{config.DATABASE}'

db_obj = db_api.MongoAdapters(app)


@app.route('/users', methods=['GET'])
def get_users():
    return db_obj.get_all_users()


@app.route('/add', methods=['POST'])
def add_users():
    name = request.json['name']
    email = request.json['email']
    return db_obj.add_users(name, email)


if __name__ == '__main__':
    app.run(debug=True)
