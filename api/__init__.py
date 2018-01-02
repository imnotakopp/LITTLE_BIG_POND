from tornado import ioloop, web
from tornado.httpserver import HTTPServer
from api.urls import patterns
import os

if __name__ == "__main__":
    # server = HTTPServer(web.Application(patterns))

    # try:
    # server.bind(8888)
    # server.start(os.cpu_count())
    ioloop.IOLoop.current().stop()
    print("process id: ", os.getpid())
    # except Exception as e:
    #     print(e)
