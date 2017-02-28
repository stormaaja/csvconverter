#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

class CsvConverter:

    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.rows = []
        self.source_product_code = "product_code"
        self.source_quantity = "quantity"
        self.debug = False

    def set_debug(self, debug):
        self.debug = debug

    def clear(self):
        self.rows = []

    def addRow(self, row):
        self.rows.append(row)

    def getRow(self, index):
        return self.rows[index]

    def setSourceColumns(self, source_product_code, source_quantity):
        self.source_product_code = source_product_code
        self.source_quantity = source_quantity

    def convertRow(self, row):
        if not row[self.source_product_code]:
            raise ValueError
        if self.debug:
            print row
        return {
            'product_code': row[self.source_product_code],
            'quantity': int(row[self.source_quantity])
        }

    def read_csv(self, file_object):
        reader = csv.DictReader(file_object)
        for row in reader:
            self.addRow(self.convertRow(row))

    def read_file(self):
        with open(self.csv_file_path, 'rb') as csvfile:
            self.read_csv(csvfile)
