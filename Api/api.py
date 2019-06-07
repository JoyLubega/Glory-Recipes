from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from config import application_config
from flask_cors import CORS, cross_origin

db = SQLAlchemy()
from .models.category import CategoryModel
from .models.recipes import RecipeModel
from .models.user import UserModel

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(application_config[config_name])
    CORS(app)
    db.init_app(app)

    return app

app = create_app('ProductionEnv')
from .views import dummy_view