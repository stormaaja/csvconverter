#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime
from flask import Flask

from update_wrapper import UpdateWrapper

LOG_FILE = datetime.now().strftime("%Y%m%d%H%M%S%f")
LOG_DIR = "log"
FULL_LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

logging.basicConfig(
    filename=FULL_LOG_PATH,
    level=logging.DEBUG)

logging.captureWarnings(True)

wrapper = UpdateWrapper()
wrapper.read_config("config.json")
# wrapper.run()

app = Flask(__name__)

if __name__ == "__main__":
    app.run()
