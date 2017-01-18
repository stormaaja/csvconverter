#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

class CsvConverter:

    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.lines = []

    def clear(self):
        self.lines = []

    def addRow(self, row):
        self.lines.append(row)

    def convertRow(self, row):
        return {
            'product_code': int(row['tuotekoodi']),
            'quantity': int(row['qty'])
        }

    def read_file(self):
        with open(self.csv_file_path, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.addRow(convertRow(row))
