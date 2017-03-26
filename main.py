#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import logging
from datetime import datetime
from threading import Thread, Lock

from flask import Flask, request, session, json

from update_wrapper import UpdateWrapper

LOG_FILE = "{}.log".format(datetime.now().strftime("%Y%m%d%H%M%S%f"))
LOG_DIR = "log"
FULL_LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

LINE_TYPE_INFO = "INFO"
LINE_TYPE_WARNING = "WARNING"
LINE_TYPE_ERROR = "ERROR"
LINE_TYPE_UNDEFINED = ""

PUBLIC_PATHS = { "/session": [ 'POST' ],
                    "/index-min.js": ['GET'],
                    "/": ['GET'] }

line_type_pattern = re.compile('^(ERROR|WARNING|INFO):')

if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

logging.basicConfig(
    filename=FULL_LOG_PATH,
    level=logging.DEBUG)

logging.captureWarnings(True)

wrapper = UpdateWrapper()
wrapper.read_config("config.json")

if len(sys.argv) > 1 and sys.argv[1] == "--run-update":
    logging.info("Running update")
    wrapper.run()
    logging.info("Update finished")
    sys.exit()

app = Flask(__name__)
app.secret_key = os.urandom(24)

status = { "code": 0, "message": "idle" }

class Unauthorized(Exception):
    status_code = 401

    def __init__(self, message="", payload=None):
        Exception.__init__(self)
        self.message = message
        self.payload = payload

def get_line_type(line):
    if line_type_pattern.match(line) != None:
        return line[:line.index(':')]
    return LINE_TYPE_UNDEFINED

def read_file(file):
    with open(file, 'r') as f:
        read_data = f.read()
    f.closed
    return read_data

def set_status(code, message):
    lock = Lock()
    with lock:
        status["code"] = code
        status["message"] = message

def run_update():
    try:
        logging.info("Update started")
        set_status(1, "Update started {}".format(datetime.now()))
        wrapper.run()
        set_status(1, "Update finished {}".format(datetime.now()))
        logging.info("Update finished")
    except Exception as e:
        set_status(-1, "Error occurred")
        logging.exception(e)

@app.errorhandler(Unauthorized)
def custom_401(error):
    return "Unauthorized", error.status_code

@app.before_request
def before_req():
    if "username" in session:
        return

    if request.path in PUBLIC_PATHS and \
        request.method in PUBLIC_PATHS[request.path]:
        return

    raise Unauthorized()

@app.route('/session', methods=['DELETE'])
def logout():
    session.pop('username', None)
    app.secret_key = os.urandom(24)
    return "Ok", 200

@app.route('/session', methods=['POST'])
def login():
    if request.form['username'] == wrapper.config['username'] \
            and request.form['password'] == wrapper.config['password']:
        session['username'] = request.form['username']
        return session['username'], 200
    return "Invalid password or username", 401

@app.route('/session', methods=['GET'])
def get_session():
    return session['username'], 200

@app.route('/status', methods=['GET'])
def get_status():
    return json.jsonify(status), 200

@app.route('/', methods=['GET'])
def get_index():
    return read_file("public/index.html")

@app.route('/index-min.js', methods=['GET'])
def get_index_js():
    if wrapper.config['development']:
        return read_file("public/index.js")
    return read_file("public/index-min.js")

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

@app.route('/update', methods=['POST'])
def perform_update():
    thread = Thread(target = run_update)
    thread.start()
    return "Update started", 200

if __name__ == "__main__":
    app.run()
