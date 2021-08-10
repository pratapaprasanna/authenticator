import requests
import google.auth.transport.requests

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from cachecontrol import CacheControl

from authenticator.utils import utils


class GoogleLoginAdapter(object):
    def __init__(self):
        self.google_obj = utils.read_config()["auth"]["google"]
        self.flow = Flow.from_client_secrets_file(
            client_secrets_file=self.google_obj["secrets_file"],
            scopes=self.google_obj["scopes"],
            redirect_uri=self.google_obj["redirect_uri"],
        )

    def get_basic_info(self, request, session):
        self.flow.fetch_token(authorization_response=request.url)
        if not session["state"] == request.args["state"]:
            abort(500)  # State does not match!

        credentials = self.flow.credentials
        request_session = requests.session()
        cached_session = CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)
        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=self.google_obj["google_client_id"],
        )
        return id_info
