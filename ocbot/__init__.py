import logging
import os

from flask import Flask
from config.all_config_loader import configs
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from ocbot.external.route_airtable import AirTableBuilder
from ocbot.log_manager import setup_logging

logger = logging.getLogger(__name__)
app = Flask(__name__,
            template_folder="web/templates",
            static_folder="web/static")

if configs['DB_DIALECT'] == 'sqlite':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://dev.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f"{configs['DB_DIALECT']}://{configs['DB_USERNAME']}:{configs['DB_PASSWORD']}@{configs['DB_ADDR']}/{configs['DB_NAME']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join('ocbot', 'web', 'imageStore')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if 'test-oc' not in os.environ:
    setup_logging()


if os.environ['CONFIG_FILE'] == 'development.py':
    from flask_debug import Debug
    Debug(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from ocbot.web import routes_slack
from ocbot.web import routes_web
from ocbot.database import models
