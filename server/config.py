from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = b'\x0e\xf3\xb5\xf8\xfe\xd5\x18\xcc\xbb\x99\xcc\xb17;N\xcb'

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

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}},)


