#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import logging
from datetime import datetime
from flask import Flask, request

from update_wrapper import UpdateWrapper

LOG_FILE = "{}.log".format(datetime.now().strftime("%Y%m%d%H%M%S%f"))
LOG_DIR = "log"
FULL_LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

LINE_TYPE_INFO = "INFO"
LINE_TYPE_WARNING = "WARNING"
LINE_TYPE_ERROR = "ERROR"
LINE_TYPE_UNDEFINED = ""

line_type_pattern = re.compile('^(ERROR|WARNING|INFO):')

if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

logging.basicConfig(
    filename=FULL_LOG_PATH,
    level=logging.DEBUG)

logging.captureWarnings(True)

wrapper = UpdateWrapper()
wrapper.read_config("config.json")

app = Flask(__name__)

def get_line_type(line):
    if line_type_pattern.match(line) != None:
        return line[:line.index(':')]
    return LINE_TYPE_UNDEFINED

@app.route('/log', methods=['GET'])
def get_log():
    include = []
    log_lines = []

    if request.args.get('info', '') == 'true':
        include.append(LINE_TYPE_INFO)
    if request.args.get('warning', '') == 'true':
        include.append(LINE_TYPE_WARNING)
    if request.args.get('error', '') == 'true':
        include.append(LINE_TYPE_ERROR)

    with open(FULL_LOG_PATH, 'r') as f:
        including = True
        for line in f:
            line_type = get_line_type(line)

            if line_type in include:
                including = True
            elif line_type != LINE_TYPE_UNDEFINED:
                including = False

            if including and len(line) > 0:
                log_lines.append(line)
    f.closed

    return "".join(log_lines)

if __name__ == "__main__":
    app.run()
