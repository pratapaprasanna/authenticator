import os
import oauthlib

from flask import Flask, session, url_for, abort, redirect, request

from authenticator.adapters.db import api as db_api
from authenticator.adapters.login import google_adapter
from authenticator.utils import utils


app = Flask(__name__)

host = os.environ.get("db_host", "mongo")
port = os.environ.get("db_port", "27017")

app.config["SECRET_KEY"] = "b9dd1b2f"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
app.config["GOOGLE_CLIENT_ID"] = os.environ.get("GOOGLE_CLIENT_ID", None)
app.config["GOOGLE_CLIENT_SECRET"] = os.environ.get("GOOGLE_CLIENT_SECRET", None)


db_obj = db_api.MongoAdapters(host, port)
google_adapter_obj = google_adapter.GoogleLoginAdapter()


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/")
def index():
    return "Hello World <a href='/googlelogin'><button>Sign Up with google</button></a>"


def add_users(name, email, provider=None, provider_id=None):
    if email == "pratapagoutham@gmail.com":
        return db_obj.add_users(
            name,
            email,
            utils.get_current_time(),
            "admin",
            provider,
            provider_id,
        )
    return db_obj.add_users(
        name,
        email,
        utils.get_current_time(),
        "user",
        provider,
        provider_id,
    )


@app.route("/googlelogin")
def login():
    authorization_url, state = google_adapter_obj.flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/googlecallback")
def googlecallback():
    try:
        id_info = google_adapter_obj.get_basic_info(request, session)
    except oauthlib.oauth2.rfc6749.errors.InvalidGrantError:
        return redirect("/")

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    name = id_info.get("name")
    email = id_info.get("email")
    google_id = id_info.get("sub")

    session["google_id"] = google_id
    session["name"] = name
    session["email"] = email
    return add_users(name, email, "google", google_id)


@app.route("/fetch", methods=["GET"])
def validate_users():
    token = request.args.get("token")
    result = db_obj.is_valid_user(token)
    if isinstance(result, dict):
        return result
    else:
        abort(401, "unauthorized")


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
