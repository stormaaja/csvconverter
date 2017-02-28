#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import Request, urlopen, HTTPError, URLError
from csv_converter import CsvConverter
from stock_updater import StockUpdater
import sqlite3
import mysql.connector
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

if config["database_connection"]["type"] == "sqlite3":
    conn = sqlite3.connect(config["database_connection"]["database"])
elif config["database_connection"]["type"] == "mysql":
    conn = mysql.connector.connect(
        user=config["database_connection"]["username"],
        password=config["database_connection"]["password"],
        host=config["database_connection"]["host"],
        database=config["database_connection"]["database"])
else:
    raise "Please, define database"

if config["testing"]:
    database_helper.initialize(conn)
    database_helper.add_test_products(conn)

updater = StockUpdater(conn)
updater.set_perform_check_product(config["database_connection"]["check_products"])
updater.set_destination_colums(
    config["database_connection"]["product_code_column"],
    config["database_connection"]["quantity_column"])
updater.set_table(config["database_connection"]["products_table"])
updater.set_items(converter.rows)
updater.update()