from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, User, Items
from flask_jwt_extended import JWTManager

app = Flask(__name__)

#migration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///small.db'
migrate = Migrate(app, db)
db.init_app(app)

#jwt
app.config['JWT_SECRET_KEY'] = ''
jwt = JWTManager(app)
jwt.init_app(app)


