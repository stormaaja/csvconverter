#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import Request, urlopen, HTTPError, URLError
from csv_converter import CsvConverter
from stock_updater import StockUpdater, ProductNotFoundError, MultipleProductsFoundError
import sqlite3
import mysql.connector
import os
import json
import logging
from datetime import datetime

import database_helper

class UpdateWrapper:

    def read_config(self, file):
        with open(file) as f:
            self.config = json.load(f)

    def run(self):
        request = Request(self.config["source"]["url"])

        try:
            response = urlopen(request)
        except HTTPError as e:
            logging.error("The server returned error %d", e.code)
            raise e
        except URLError as e:
            logging.error("Failed to reach server: %s", e.reason)
            raise e

        converter = CsvConverter("")

        converter.setSourceColumns(
            self.config["source"]["product_code_column"],
            self.config["source"]["quantity_column"])
        converter.read_csv(response)

        if self.config["database_connection"]["type"] == "sqlite3":
            conn = sqlite3.connect(self.config["database_connection"]["database"])
        elif self.config["database_connection"]["type"] == "mysql":
            conn = mysql.connector.connect(
                user=self.config["database_connection"]["username"],
                password=self.config["database_connection"]["password"],
                host=self.config["database_connection"]["host"],
                database=self.config["database_connection"]["database"])
        else:
            raise "Please, define database"

        if self.config["testing"]:
            database_helper.initialize(conn)
            database_helper.add_test_products(conn)

        updater = StockUpdater(conn)
        updater.set_destination_colums(
            self.config["database_connection"]["product_code_column"],
            self.config["database_connection"]["quantity_column"])
        updater.set_table(self.config["database_connection"]["products_table"])

        for item in converter.rows:
            try:
                updater.update_quantity(item['product_code'], item['quantity'])
            except ProductNotFoundError as e:
                logging.warning("Product {} not found".format(item['product_code']))
            except MultipleProductsFoundError as e:
                logging.error("Multiple products found with product id {}".format(item['product_code']))
