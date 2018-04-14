
from scripts.client import Client

from bson import ObjectId


class Worker:

    __ACTIVE__ = 'ACTIVE'
    __CLOSED__ = 'CLOSED'
    __LISTENING__ = 'LISTENING'
    __ERROR__ = 'ERROR'

    def __init__(self, _id):
        self._id = ObjectId(_id)
        self._instance = ObjectId()
        self.client = Client()
        self.status = None
        self.__setstate__(self.__LISTENING__)

    def __setstate__(self, state):
        self.status = state
        self._update(
            {
                '__state__': state
            }
        )

    def _update(self, doc):
        self.client.update(
            'SYSTEM',
            'WORKER',
            {'_id': self._id},
            {
               "$set": doc
            }
        )

    def _error(self, message):
        self.__setstate__(self.__ERROR__)
        self.client.insert(
            db='SYSTEM',
            coll='ERRORS',
            docs={
                'instance': self._instance,
                'msg': message
            }
        )

    def _close(self):
        self.__setstate__(self.__CLOSED__)

    def _next(self):
        # todo: get aggregation of self._id
        pass


if __name__ == '__main__':
    worker = Worker(ObjectId())
    print(worker.status)
    worker._error('testing error')
    print(worker.status)
    worker._close()
    print(worker.status)