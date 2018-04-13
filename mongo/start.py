"""
@author: Alan Kopp
@created 9/24/2017
"""

from sys import platform

import os
import sys
from bson import json_util

if __name__ == "__main__":
    # load instance configuration
    try:
        config = open("{0}/config.json".format(os.getcwd())).read()
        cjson = json_util.loads(config)
        print(json_util.dumps(cjson, indent=2))
        os.system("{0} --config {1}".format(cjson["DATABASE"]["EXECUTABLE"], cjson["DATABASE"]["CONFIGURATION"]))
    except Exception as e:
        print("ERROR: {0}".format(e))
