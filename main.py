#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime

from update_wrapper import UpdateWrapper

if not os.path.isdir("log"):
    os.mkdir("log")

LOG_FILE = datetime.now().strftime("%Y%m%d%H%M%S%f")

logging.basicConfig(
    filename="log/{}.log".format(LOG_FILE),
    level=logging.DEBUG)

logging.captureWarnings(True)

wrapper = UpdateWrapper()
wrapper.read_config("config.json")
wrapper.run()
