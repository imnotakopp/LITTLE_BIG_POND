
from tornado import web
from api.views.main import MainAPIHandler

patterns = [
    (r"/?", MainAPIHandler),
    (r"/new?", MainAPIHandler)
]