import os
import utils
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

annotadb = utils.read_config()["annotadb"]

basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Build the Sqlite ULR for SqlAlchemy
sqlite_url = "sqlite:////" + annotadb

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.app_context().push()

# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)