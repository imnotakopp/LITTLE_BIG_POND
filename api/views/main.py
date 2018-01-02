from tornado.web import RequestHandler
from scripts.client import MongoDB


class MainAPIHandler(RequestHandler):

    def __init__(self):
        if not self.is_authorized():
            self.set_status(401, "Unauthorized")
            self.finish()
            return
        self.client = MongoDB()
        super(RequestHandler).__init__(self)

    def get(self):
        self.write("hello world!   !")

    def is_authorized(self):
        return True
