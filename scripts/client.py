"""
@author: Alan Kopp
@created: 9/24/2017
"""
from scripts import exceptions
from pymongo import MongoClient
from bson import json_util, ObjectId
import re
import ast
from datetime import datetime
import time


class Client:

    def __init__(self):
        # todo: create setup file
        self.host = "127.0.0.1"
        self.port = 30000
        self.client = self._connect()
        self.database = None
        self.collection = None

    def _connect(self):
        return MongoClient(self.host, self.port)

    def insert(self, db, coll, docs):
        """

        :param db: database to use
        :param coll: collection to insert
        :param docs: documents to be inserted, can be type 'dict' or 'list'
        :return: boolean status of insert
        """
        self.database = db
        self.collection = coll
        if type(docs) is list:
            self._insert_list(docs)
        elif type(docs) is dict:
            self._insert_dict(docs)
        else:
            raise Exception("was expecting 'list' or 'dict' type but found '{}'".format(type(docs)))

    def _insert_dict(self, doc):
        clean_docs = self.clean_doc(doc, keys=True)
        self.client = self._connect()  # need to recreate connection since this function is threaded
        self.client[self.database][self.collection].insert(clean_docs)

    def _insert_list(self, docs):
        clean_docs = self.clean_list(docs, keys=True)
        self.client = self._connect()  # need to recreate connection since this function is threaded
        self.client[self.database][self.collection].insert_many(clean_docs)

    def update(self, db, coll, filter, doc, upsert=True):
        """

        :param db: database to use
        :param coll: collection of the data to modify
        :param kwargs: supported arguments include find, documents,
        :return:
        """
        self.database = db
        self.collection = coll
        self.client[self.database][self.collection].update(
            filter,
            doc,
            upsert=upsert
        )

    def aggregate(self, database, collection=None, pipeline=None, file_id=None):
        """

        :param database: database to use in pipeline
        :param collection: base collection to use for aggregation
        :param pipeline: mongo aggregate pipeline
        :param file_id: a reference a aggregation javascript file
        :return:
        """

        if file_id:
            path = 'C:/LITTLE_BIG_POND/aggregates/{db}/{id}.js'.format(db=database, id=file_id)
            content = None
            try:
                with open(path, 'r') as f:
                    content = f.read()
            except exceptions.FileNotFound as e:
                raise exceptions.FileNotFound(path=path, error=e)

            collection, pipeline = self.parse_aggregate(content)

        if not pipeline or not collection:
            raise exceptions.AggregateException(error="collection or pipeline not defined")
        pipeline = json_util.loads(pipeline)
        pipeline = self.clean_list(pipeline)
        print(json_util.dumps(pipeline, indent=4))

        # docs = list(self.client[database][collection].aggregate(pipeline))

    def parse_aggregate(self, content):

        re_coll = re.compile(r'db[\.\[\"\']+([\w\d\s\.]*)[\]\'\"]*.aggregate')
        re_commments = re.compile(r'\/\/.*|\/\*[\w\d\s\n]*\*\/')
        re_fluff = re.compile(r'\s\s|\n|\t|\r')
        re_iso = re.compile(r'ISODate\([\'\"]?([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z)?[\'\"]?\)')
        re_bson = re.compile(r'ObjectId\([\'\"](.*)[\'\"]\)')
        re_commas = re.compile(r',(]|})')
        re_pipe = re.compile(r'db[\.\[\"\']+([\w\d\s\.]*)[\]\'\"]*.aggregate\((.*)\);')

        # remove single line and multi-line comments
        pipeline = re.sub(re_commments, '', content)
        # remove extra white spaces, tabs, new lines, etc.
        pipeline = re.sub(re_fluff, '', pipeline)
        # wrap ISODate() in single quotes
        pipeline = re.sub(re_iso, r'"ISODate(\1)"', pipeline)
        # wrap ObjectId() in single quotes
        pipeline = re.sub(re_bson, r'"ObjectId(\1)"', pipeline)
        # convert boolean true / false to True and False
        pipeline = re.sub('true', '"True"', pipeline)
        pipeline = re.sub('false', '"False"', pipeline)
        # wrap all keys with single quotes
        pipeline = re.sub(r'(\$?[^:\{\[\'\",]+?):\s', r'"\1": ', pipeline)
        # remove extra commas
        pipeline = re.sub(re_commas, r'\1', pipeline)
        # extract stages and collection
        parts = re.search(re_pipe, pipeline)
        return parts.group(1), parts.group(2)

    def clean_list(self, document, keys=False):
        clean_doc = []
        for i, value in enumerate(document):
            if type(value) is dict:
                clean_doc.append(self.clean_doc(value, keys=keys))
            elif type(value) is list:
                clean_doc.append(self.clean_list(value, keys=keys))
        return clean_doc

    def clean_doc(self, document, keys=False):
        clean_doc = {}
        for key, value in document.items():
            clean_key = self._clean_key(key) if keys else key
            if type(value) is dict:
                clean_doc.update({clean_key: self.clean_doc(value, keys=keys)})
            elif type(value) is list:
                clean_doc.update({clean_key: self.clean_list(value, keys=keys)})
            else:
                clean_doc.update({clean_key: self.clean_value(value)})
        return clean_doc

    def clean_value(self, val):
        if type(val) is not str:
            return val
        if 'ObjectId' in val:
            return ObjectId(re.search(r'ObjectId\((.+?)\)', val).group(1))
        elif 'ISODate' in val:
            try:
                return datetime.strptime(val, 'ISODate(%Y-%m-%dT%H:%M:%S.%fZ)')
            except ValueError as e:
                return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            return ast.literal_eval(val)

    def _clean_key(self, k):
        regex = re.compile(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))')
        return re.sub(regex, r'_\1', k).upper()


if __name__ == "__main__":

    client = Client()
    try:
        client.aggregate(database='SYSTEM', file_id='aggregate')
    except exceptions.Exceptions as e:
        print(e.message)
