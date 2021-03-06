#!/usr/bin/env python3

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

import sys
from pathlib import Path

# add parent folder
sys.path.append(str(Path(__file__).parent.parent.absolute()))

from app import db, app
from components.models import Admin

new_name = input("Enter name: ")
new_email = input("Enter email: ")
new_password = input("Enter password: ")

admin = Admin(
    name=new_name,
    email=new_email,
    hashed_password=Admin.hash_password(Admin, new_password),
)

with app.app_context():
    db.session.add(admin)
    db.session.commit()
