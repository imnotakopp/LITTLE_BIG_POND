

from pymongo import MongoClient


class DataSource:

    def __init__(self, config_id, handler=None):
        self._id = config_id
        self.config = self._get_config()
        self.client = MongoClient(host='localhost', port=30000)
        self.handler = handler

    def _get_config(self):
        return {}

    def get(self):
        pass

    def _default_handler(self, records):
        self.client['DATA']['RECORDS'].insert_many(records)
        pass

