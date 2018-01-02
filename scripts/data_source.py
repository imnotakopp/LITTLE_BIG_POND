
import requests
from AdvancedHTMLParser import Parser
from scripts.client import MongoDB
from bson import json_util


class DataSource:

    def __init__(self, config_id, handler=None):
        self._id = config_id
        self.client = MongoDB()
        self.handler = handler
        self.config = self._get_config()

    def _get_config(self):
        return {"URL": "https://www.crossfit.com/workout/"}

    def get(self):
        response = requests.get(
            url=self.config["URL"],
            headers={
                "accept": "application/json;odata=verbose"
            }
        )

        if response.status_code != 200:
            print(json_util.dumps(response.json(), indent=4))
        else:
            re = response.json()["wods"]
            # print(json_util.dumps(re, indent=4))
            self.client.insert(db="CROSSFIT", coll="WODS", docs=re)

    def _default_handler(self, records):
        self.client.insert(db="DATA", coll="SOURCES", docs=records)


if __name__ == "__main__":
    source = DataSource(1)
    source.get()