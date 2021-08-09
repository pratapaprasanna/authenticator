import os
import requests

from flask import Flask, session, url_for, abort, redirect, request

from authenticator.adapters.db import api as db_api
from authenticator.adapters.login import google_adapter
from authenticator.utils import utils

database = os.environ.get("db", "authenticator")
host = os.environ.get("db_host", "mongo")
port = os.environ.get("db_port", "27017")

app = Flask(__name__)
app.config["MONGO_URI"] = f"mongodb://{host}:{port}/{database}"
app.config["SECRET_KEY"] = "b9dd1b2f"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
app.config["GOOGLE_CLIENT_ID"] = os.environ.get("GOOGLE_CLIENT_ID", None)
app.config["GOOGLE_CLIENT_SECRET"] = os.environ.get("GOOGLE_CLIENT_SECRET", None)


db_obj = db_api.MongoAdapters(app)
google_adapter_obj = google_adapter.GoogleLoginAdapter()


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/users", methods=["GET"])
def get_users():
    return db_obj.get_all_users()


@app.route("/")
def index():
    return "Hello World <a href='/googlelogin'><button>Sign Up with google</button></a>"


def add_users(name, email, provider=None, provider_id=None):
    if email == "pratapagoutham@gmail.com":
        return db_obj.add_users(
            name, email, utils.get_current_time(), "admin", provider, provider_id
        )
    return db_obj.add_users(
        name, email, utils.get_current_time(), "user", provider=None, provider_id=None
    )


@app.route("/googlelogin")
def login():
    authorization_url, state = google_adapter_obj.flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    id_info = google_adapter_obj.get_basic_info(request, session)
    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    name = id_info.get("name")
    email = id_info.get("email")
    google_id = id_info.get("sub")
    session["google_id"] = google_id
    session["name"] = name
    session["email"] = email
    add_users(name, email, "google", google_id)
    return redirect("/protected_area")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/protected_area")
@login_is_required
def protected_area():
    return (
        f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
