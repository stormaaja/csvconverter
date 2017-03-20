#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime
from flask import Flask

from update_wrapper import UpdateWrapper

LOG_FILE = "{}.log".format(datetime.now().strftime("%Y%m%d%H%M%S%f"))
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

app = Flask(__name__)

@app.route('/log', methods=['GET'])
def get_log():
    with open(FULL_LOG_PATH, 'r') as f:
        read_data = f.read()
    f.closed
    return read_data

if __name__ == "__main__":
    app.run()
