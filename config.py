import os

# used by Flask to encrypt session cookies.
SECRET_KEY = '\xca\xbc>\x95\x85+h\x0e\xb9!\x05\xff\xf3@6\xf2\x9b9\xabm\x85\xbd\xf2j'

DATA_BACKEND = 'cloudsql'

# Google Cloud Project ID.
PROJECT_ID = 'bellow-garrison'

# CloudSQL & SQLAlchemy configuration
CLOUDSQL_USER = 'erik'
CLOUDSQL_PASSWORD = 'sucks'
CLOUDSQL_DATABASE = 'buttons'

# Must also be updated in app.yaml.
CLOUDSQL_CONNECTION_NAME = 'bellow-garrison:us-central1:porygon'

# The CloudSQL proxy is used locally to connect to the cloudsql instance.
# To start the proxy, use:
#
#   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
#
# Port 3306 is the standard MySQL port. If you need to use a different port,
# change the 3306 to a different port number.

# When running a local MySQL instance for testing.
LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{database}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE)

# When running on App Engine using a unix socket 
LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

if os.environ.get('GAE_INSTANCE'):
    SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
else:
    SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI

# Google Cloud Storage and upload settings.
CLOUD_STORAGE_BUCKET = 'bellow-garrison'

# OAuth2 configuration.
# This can be generated from the Google Developers Console at
# https://console.developers.google.com/project/_/apiui/credential.
# Note that you will need to add all URLs that your application uses as
# authorized redirect URIs. For example, typically you would add the following:
#
#  * http://localhost:8080/oauth2callback
#  * https://<your-app-id>.appspot.com/oauth2callback.
#
# If you receive a invalid redirect URI error review you settings to ensure
# that the current URI is allowed.
GOOGLE_OAUTH2_CLIENT_ID = \
    '536569692554-9phesnj7lvv161fbmua7r5r6jcshl2ut.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'wWK-Bxa3w7qGYrVPaRBBbjDQ'