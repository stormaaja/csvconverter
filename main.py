#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import Request, urlopen, HTTPError, URLError
from csv_converter import CsvConverter
from stock_updater import StockUpdater
import sqlite3
import psycopg2
import os
import json

import database_helper

with open("config.json") as f:    
    config = json.load(f)

request = Request(config["source"]["url"])

try:
    response = urlopen(request)
except HTTPError as e:
    print "The server returned error {}".format(e.code)
    exit
except URLError as e:
    print "Failed to reach server: {}".format(e.reason)
    exit

converter = CsvConverter("")
converter.setSourceColumns(
    config["source"]["product_code_column"],
    config["source"]["quantity_column"])
converter.read_csv(response)

if config["database"]["type"] == "sqlite3":
    conn = sqlite3.connect(config["database"]["url"])
elif config["database"]["type"] == "psql":
    conn = psycopg2.connect(config["database"]["connection"])
else:
    raise "Please, define database"

if config["testing"]:
    database_helper.initialize(conn)
    database_helper.add_test_products(conn)

updater = StockUpdater(conn)
updater.set_perform_check_product(config["database"]["check_products"])
updater.set_destination_colums(
    config["database"]["product_code_column"],
    config["database"]["quantity_column"])
updater.set_table(config["database"]["products_table"])
updater.set_items(converter.rows)
updater.update()