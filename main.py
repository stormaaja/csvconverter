#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from update_wrapper import UpdateWrapper

if not os.path.isdir("log"):
    os.mkdir("log")

wrapper = UpdateWrapper()
wrapper.read_config("config.json")
wrapper.run()