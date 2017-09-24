"""
@author: Alan Kopp
@created: 9/24/2017
"""

from scripts.client import MongoDB

import os
import json


def mongod_start(auth=False):
    # load mongod config
    try:
        conf_file = open("{0}/config.json".format(os.getcwd())).read()
        config = json.loads(conf_file)
        # start mongo database
        command = "{0} --config {1}/{2}".format(config["MONGOD"]["EXECUTABLE"], os.getcwd(), config["MONGOD"]["CONFIGURATION"])
        if auth:
            command += " --auth"
        os.system(command)
    except Exception as e:
        print("ERROR: {0}".format(e))


def mongod_stop():
    try:
        command = "taskkill /f /im mongod.exe"
        print("Executing: {0}".format(command))
        os.system(command)
    except Exception as e:
        print("mongod did not shutdown: {0} \n check the config.json file and that mongod is up before continuing".format(command))
        print("ERROR: {0}".format(e))


def mongod_restart(auth=False):
    mongod_stop()
    mongod_start(auth=auth)


if __name__ == "__main__":
    # TODO: standardize setup
    """
        start mongod without authentication on
            --host localhost (127.0.0.1)
            --port 27017
        create initial user / pass with ability to 
            -- CRUD users in db admin
            -- CRUD roles in db admin
            then
            -- create default users role
            -- create default power_user role
            -- create default admin role 
        restart mongod instance using authenticated user created in ladder
        prompt user to create an additional admin *required*
            --allow user to define new role *optional* - can be done later
            --allow user to define new users *optional* - can be done later
    """
    mongod_start()

    # create a connection to new instance
    client = MongoDB()

    # create temporary users
    user_conf = open("{0}/temp.users.json".format(os.getcwd())).read()
    user_json = json.loads(user_conf)
    for user in user_json:
        client.create_user(user)

    # create default roles defined in default.roles.json
    role_conf = open("{0}/default.roles.json".format(os.getcwd())).read()
    role_json = json.loads(role_conf)
    for role in role_json:
        client.create_role(role)

    # restart mongod and require authentication
    mongod_restart(auth=False)
    pass
