from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
import os
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
def generate_secret_key():
    return secrets.token_hex(32)
app.config['SECRET_KEY'] = generate_secret_key()

#Cloudinary config
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME', 'dzqt3usfp')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY', '618183139173486')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET', '6oUAsFqSzho3xOjxebi3SIUps9U')

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
bcrypt = Bcrypt(app)

# CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}},)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "https://spaces-client.onrender.com"}})

