import os

from flask import Flask
from flask import jsonify
from flask import request, url_for, redirect, session
from flask_login import logout_user

from authenticator.adapters.db import api as db_api
from authenticator.adapters.login import loginmanager
from authenticator.utils import utils

database = os.environ.get("db", "authenticator")
host = os.environ.get("db_host", "mongo")
port = os.environ.get("db_port", "27017")

app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb://{host}:{port}/{database}"
app.config["SECRET_KEY"] = "b9dd1b2f"
app.config["GOOGLE_CLIENT_ID"] = os.environ.get("GOOGLE_CLIENT_ID", None)
app.config["GOOGLE_CLIENT_SECRET"] = os.environ.get("GOOGLE_CLIENT_SECRET", None)


db_obj = db_api.MongoAdapters(app)
login_obj = loginmanager.loginManager(app)


@app.route("/users", methods=["GET"])
def get_users():
    return db_obj.get_all_users()


@app.route("/", methods=["GET"])
def index():
    return "Welcome to nomad Authenticator."


def add_users(name, email, provider):
    if email == "pratapagoutham@gmail.com":
        print("HELOO")
        return db_obj.add_users(
            name, email, utils.get_current_time(), provider, "admin"
        )
    return db_obj.add_users(name, email, utils.get_current_time(), provider, "user")


@app.route("/login/google")
def google_login():
    login_obj.auth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        access_token_url="https://accounts.google.com/o/oauth2/token",
        access_token_params=None,
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        authorize_params=None,
        api_base_url="https://www.googleapis.com/oauth2/v1/",
        userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
        client_kwargs={"scope": "openid email profile"},
    )
    google = login_obj.auth.create_client("google")
    redirect_uri = url_for("google_authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/login/google/authorize")
def google_authorize():
    google = login_obj.auth.create_client("google")
    try:
        token = google.authorize_access_token()
        resp = google.get("userinfo").json()
        return add_users(resp["name"], resp["email"], "google")
    except Exception:
        return redirect("/login/google")


@app.route("/logout")
def user_logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
