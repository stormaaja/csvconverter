#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from datetime import datetime

from update_wrapper import UpdateWrapper

if not os.path.isdir("log"):
    os.mkdir("log")

logging.basicConfig(
    filename="log/{}.log".format(datetime.now().strftime("%Y%m%d%H%M%S%f")),
    level=logging.DEBUG)

logging.captureWarnings(True)

wrapper = UpdateWrapper()
wrapper.read_config("config.json")
wrapper.run()