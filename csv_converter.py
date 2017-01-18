#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv

class CsvConverter:

    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.lines = []
