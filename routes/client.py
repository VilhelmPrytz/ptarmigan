###########################################################
#    __ _           _           _   _      _        _     #
#   / _| |         | |         | | (_)    | |      | |    #
#  | |_| | __ _ ___| | ________| |_ _  ___| | _____| |_   #
#  |  _| |/ _` / __| |/ /______| __| |/ __| |/ / _ \ __|  #
#  | | | | (_| \__ \   <       | |_| | (__|   <  __/ |_   #
#  |_| |_|\__,_|___/_|\_\       \__|_|\___|_|\_\___|\__|  #
#                                                         #
# Copyright (C) 2019, Vilhelm Prytz <vilhelm@prytznet.se> #
# https://github.com/VilhelmPrytz/flask-ticket            #
#                                                         #
###########################################################

from flask import Blueprint, render_template, request

import sys
sys.path.append('..')

from components.database import get_database_objects

client_routes = Blueprint('client_routes', __name__, template_folder='../templates')

Tickets, Messages, Admins = get_database_objects()

@client_routes.route('/')
def index():
    return render_template("client/index.html")

@client_routes.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        data = request.form

        for key, value in data.items():
            if key != "name" and key != "email" and key != "message":
                return "at least one invalid key", 400
        
            if len(value) < 3:
                return f"{key} is too short", 400
            
            if key == "name":
                if len(value) > 50:
                    return f"value {value} of key {key} is too long", 400
                
            if key == "email":
                if len(value) > 50:
                    return f"value {value} of key {key} is too long", 400
                if "@" not in value:
                    return f"value {value} of key {key} is missing @", 400
                if "." not in value:
                    return f"value {value} of key {key} is missing .", 400
            
            if key == "message":
                if len(value) > 500:
                    return f"value {value} of key {key} is too long", 400
        
        # create object

    if request.method == "GET":
        return render_template("client/submit.html")