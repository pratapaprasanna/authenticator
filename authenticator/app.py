from configparser import ConfigParser

from flask import Flask
from flask import jsonify
from flask import request, url_for, redirect, session
from flask_login import logout_user

from authenticator.adapters.db import api as db_api
from authenticator.adapters.login import loginmanager

config = ConfigParser()
config.read("config.ini")

database = config.get('default', 'db')
host = config.get('default', 'db_host')
port = config.get('default', 'db_port')

app = Flask(__name__)
app.config['MONGO_URI'] = f'mongodb://{host}:{port}/{database}'
app.config['SECRET_KEY'] = "b9dd1b2f"
app.config['GOOGLE_CLIENT_ID'] = config.get('google-oauth', 'client_id')
app.config['GOOGLE_CLIENT_SECRET'] = config.get(
    'google-oauth', 'client_secret')


db_obj = db_api.MongoAdapters(app)
login_obj = loginmanager.loginManager(app)


@app.route('/users', methods=['GET'])
def get_users():
    return db_obj.get_all_users()


@app.route('/', methods=['GET'])
def index():
    return "Welcome to nomad Authenticator."


def add_users(name, email, provider):
    return db_obj.add_users(name, email, provider)


@app.route('/login/google')
def google_login():
    login_obj.auth.register(
        name='google',
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        # This is only needed if using openId to fetch user info
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        client_kwargs={'scope': 'openid email profile'},
    )
    google = login_obj.auth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/login/google/authorize')
def google_authorize():
    google = login_obj.auth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    return add_users(resp['name'], resp['email'], "google")


@app.route('/logout')
def user_logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
