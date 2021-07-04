DATABASE = "nomad"
DB_HOST = "localhost"
DB_PORT = 27017
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "************************.apps.googleusercontent.com")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "***********************")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
