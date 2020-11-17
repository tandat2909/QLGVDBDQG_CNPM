from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from .config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
admin = Admin(app,name='Quản lý giải vô địch bóng đá quốc gia',template_mode='bootstrap4')
