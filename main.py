#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from update_wrapper import UpdateWrapper

wrapper = UpdateWrapper()
wrapper.read_config("config.json")
wrapper.run()