import logging
from logging.config import dictConfig

from flask.logging import default_handler
from flask import Flask

from config import LOGGING

dictConfig(LOGGING)
app = Flask(__name__)

app.logger = logging.getLogger('CurrencyEye')
app.logger.removeHandler(default_handler)

import views