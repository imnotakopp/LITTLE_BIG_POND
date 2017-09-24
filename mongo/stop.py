"""
@author: Alan Kopp
@created 9/24/2017
"""

import os


if __name__ == "__main__":
    try:
        command = "taskkill /f /im mongod.exe"
        print("Executing: {0}".format(command))
        os.system(command)
    except Exception as e:
        print("mongod did not shutdown: {0} \n check the config.json file and that mongod is up before continuing".format(command))
        print("ERROR: {0}".format(e))
