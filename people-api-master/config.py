import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask

base_dir = os.path.abspath(os.path.dirname(__file__))

# create connexion app instance
connex_app = connexion.App(__name__, specification_dir=base_dir)

# Get underlying flask app
app = connex_app.app

# Configure SQLAlchemy part of the app instance
# Echo SQL statements it executes to console (useful to debug db programs)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'people.db')
# Below is typically on in event driven programs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Init marshmallow
# Used to person serialization and deserialization of SQLAlchemy models
ma = Marshmallow(app)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'  # Adjust the database URL as needed
db = SQLAlchemy(app)

BASE_URI='http://127.0.0.1:8000/api/people'
COVID_TRACKER_HOST = 'http://127.0.0.1:3000'