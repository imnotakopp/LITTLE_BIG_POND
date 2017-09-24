"""
@author: Alan Kopp
@created: 9/24/2017
"""

from pymongo import MongoClient

import os
import json


class MongoDB:

    def __init__(self):
        f = open("{0}/config.json".format(os.getcwd())).read()
        config = json.loads(f)
        self.host = config["CLIENT"]["HOST"]
        self.port = config["CLIENT"]["PORT"]
        self.client = self._connect()

    def _connect(self):
        if self.client is None:
            return MongoClient(self.host, self.port)

    def insert(self, db, coll, docs):
        """

        :param db: database to use
        :param coll: collection to insert
        :param docs: documents that bill inserted
        :return: boolean status of insert
        """
        # TODO: handle import
        pass

    def update(self, db, coll, **kwargs):
        """

        :param db: database to use
        :param coll: collection of the data to modify
        :param kwargs: supported arguments include find, documents,
        :return:
        """
        # TODO: handle update
        pass

    def aggregate(self, pipeline, **kwargs):
        """

        :param db: database to use in pipeline
        :param coll: base collection to use for aggregation
        :param pipeline: mongo aggregate pipeline
        :param kwargs: supported arguments include database, collection, list_coll (list of datasets that aren't stored
        in MongoDB), cursor, disk, out_db, out_coll if not defined in pipeline, doc_modifier, predecessors->aggregation .
        :return:
        """
        # TODO: handle aggregate
        # TODO: incorporate custom pipeline keywords for (this might be removed by fn_modifier
        #   $project dates
        #   $
        pass

    def create_user(self, config):
        try:
            self.client.admin.add_user(config["USER"], config["PASSWORD"], roles=config["ROLES"])
        except Exception as e:
            print("ERROR: {0}".format(e))

    def create_role(self, config):
        # TODO: standardize creating role
        pass