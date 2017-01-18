#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

class CsvConverter:

    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.lines = []
        self.source_product_code = "product_code"
        self.source_quantity = "quantity"

    def clear(self):
        self.lines = []

    def addRow(self, row):
        self.lines.append(row)

    def getRow(self, index):
        return self.lines[index]

    def setSourceColumns(source_product_code, source_quantity):
        self.source_product_code = source_product_code
        self.source_quantity = source_quantity

    def setTargetColumns(target_product_code, target_quantity):
        self.target_product_code = target_product_code
        self.target_quantity = target_quantity

    def convertRow(self, row):
        return {
            'product_code': int(row[self.source_product_code]),
            'quantity': int(row[self.source_quantity])
        }

    def read_file(self):
        with open(self.csv_file_path, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.addRow(convertRow(row))
