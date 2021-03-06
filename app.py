###########################################################
#         _                       _                       #
#        | |                     (_)                      #
#   _ __ | |_ __ _ _ __ _ __ ___  _  __ _  __ _ _ __      #
#  | '_ \| __/ _` | '__| '_ ` _ \| |/ _` |/ _` | '_ \     #
#  | |_) | || (_| | |  | | | | | | | (_| | (_| | | | |    #
#  | .__/ \__\__,_|_|  |_| |_| |_|_|\__, |\__,_|_| |_|    #
#  | |                               __/ |                #
#  |_|                              |___/                 #
#                                                         #
# Copyright (C) 2019, Vilhelm Prytz <vilhelm@prytznet.se> #
# https://github.com/VilhelmPrytz/ptarmigan               #
#                                                         #
###########################################################

from flask import Flask, render_template
from flask_minify import minify
from datetime import timedelta
import redis

from version import version

from routes.client import client_routes
from routes.admin import admin_routes

from components.core import read_configuration
from components.exceptions import StandardException, PageException

print(f"Running ptarmigan version {version}")

# Session
from flask_session.__init__ import Session

# flask app
app = Flask(__name__)

# minify
minify(app=app)

# read configuration
config = read_configuration()

# SQL
mysql_password = ":" + config["mysql"]["password"]
if config["mysql"]["password"] == "":  # if password is empty
    mysql_password = ""

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f'mysql+pymysql://{config["mysql"]["username"]}{mysql_password}@{config["mysql"]["host"]}/{config["mysql"]["database"]}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from components.models import db

db.init_app(app)

with app.app_context():
    db.create_all()

# Session Management
SESSION_TYPE = "redis"
SESSION_REDIS = redis.Redis(host=config["redis"]["host"], port=config["redis"]["port"])
SESSION_PERMANENT = True
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

app.config.from_object(__name__)
Session(app)

# variables available across all templates
@app.context_processor
def inject_version():
    return dict(version=version, name=config["settings"]["name"])


# error handlers
@app.errorhandler(StandardException)
def handle_standard_exception(error):
    return (
        render_template(
            "errors/custom.html",
            title=error.status_code,
            message=error.to_dict()["message"],
        ),
        error.status_code,
    )


@app.errorhandler(PageException)
def handle_page_exception(error):
    return error.response


@app.errorhandler(400)
def error_400(e):
    return render_template("errors/400.html"), 400


@app.errorhandler(404)
def error_404(e):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def error_500(e):
    return render_template("errors/500.html"), 500


# register routes
app.register_blueprint(client_routes)
app.register_blueprint(admin_routes)

# run app
if __name__ == "__main__":
    app.run(host="0.0.0.0")
