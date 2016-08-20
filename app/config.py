"""
Appliction configuration settings
"""
import os

from tornado.options import define

define("debug", default=True, help="Debug settings")
define("port", default=9000, help="Port to run the server on")

APP_DIR = os.path.dirname(os.path.realpath(__file__))

settings = {
    "template_path": os.path.join(APP_DIR, "templates"),
    "static_path": os.path.join(APP_DIR, "static")
}