"""
@author: Alan Kopp
@created: 9/24/2017
"""

from pymongo import MongoClient
from scripts.multi_threading import thread

import os
import json


class MongoDB:

    def __init__(self):
        f = open("{0}/config.json".format(os.getcwd())).read()
        config = json.loads(f)
        self.host = config["CLIENT"]["HOST"]
        self.port = config["CLIENT"]["PORT"]
        self.client = self._connect()
        self.database = None
        self.collection = None

    def _connect(self):
        return MongoClient(self.host, self.port)

    def insert(self, db, coll, docs):
        """

        :param db: database to use
        :param coll: collection to insert
        :param docs: documents that bill inserted
        :return: boolean status of insert
        """
        self.database = db
        self.collection = coll
        # thread(docs, self._insert_list)
        self._insert_list(docs=docs)

    def _insert_dict(self, doc):
        clean_docs = self.clean_doc(doc)
        self.client = self._connect()  # need to recreate connection since this function is threaded
        self.client[self.database][self.collection].insert(clean_docs)

    def _insert_list(self, docs):
        clean_docs = self.clean_list(docs)
        self.client = self._connect()  # need to recreate connection since this function is threaded
        self.client[self.database][self.collection].insert_many(clean_docs)

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

    def clean_list(self, document):
        clean_doc = []
        for i, value in enumerate(document):
            if type(value) is dict:
                clean_doc.append(self.clean_doc(value))
            elif type(value) is list:
                clean_doc.append(self.clean_doc(value))
        return clean_doc

    def clean_doc(self, document):
        clean_doc = {}
        print(document)
        for key, value in document.items():
            clean_key = self._clean_key(key)
            if type(value) is dict:
                print(clean_key, value)
                clean_doc.update({clean_key: self.clean_doc(value)})
            elif type(value) is list:
                print(clean_key, value)
                clean_doc.update({clean_key: self.clean_list(value)})
            else:
                print(clean_key, value)
                clean_doc.update({clean_key: self.clean_value(value)})
        return clean_doc

    def clean_value(self, val):
        return val

    def _clean_key(self, k):
        # TODO -> to uppercase and remove special characters
        try:
            return k.upper()
        except:
            return k


if __name__ == "__main__":
    pass