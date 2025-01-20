from flask import Flask
from flask_migrate import Migrate
from models import db
from flask_jwt_extended import JWTManager
from views import *
from datetime import timedelta
app = Flask(__name__)

#migration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///small.db'
app.config["JWT_ACCESS_TOKEN_EXPIRE"] = timedelta(hours = 2)
migrate = Migrate(app, db)
db.init_app(app)

#jwt
app.config['JWT_SECRET_KEY'] = 'kmuigyuhompkorfssdfsijobjl'
jwt = JWTManager(app)
jwt.init_app(app)


app.register_blueprint(user_bp)
app.register_blueprint(Items_bp)