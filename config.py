import os

# used by Flask to encrypt session cookies.
SECRET_KEY = '\xca\xbc>\x95\x85+h\x0e\xb9!\x05\xff\xf3@6\xf2\x9b9\xabm\x85\xbd\xf2j'

DATA_BACKEND = 'cloudsql'

# Google Cloud Project ID.
PROJECT_ID = 'people-are-pigeons'

# CloudSQL & SQLAlchemy configuration
CLOUDSQL_USER = 'erik'
CLOUDSQL_PASSWORD = 'sucks'
CLOUDSQL_DATABASE = 'buttons'

# Must also be updated in app.yaml.
CLOUDSQL_CONNECTION_NAME = 'people-are-pigeons:us-central1:my-instance'

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
