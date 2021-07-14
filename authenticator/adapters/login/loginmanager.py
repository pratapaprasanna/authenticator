from authlib.integrations.flask_client import OAuth


class loginManager(object):

    def __init__(self, app):
        self.auth = OAuth(app)