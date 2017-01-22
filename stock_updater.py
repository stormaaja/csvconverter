#!/usr/bin/env python
# -*- coding: utf-8 -*-

class StockUpdater:

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def set_items(self, items):
        self.items = items

    def set_table(self, table):
        self.table = table

    def set_destination_colums(self, product_code, quantity):
        self.product_code_column = product_code
        self.quantity_column = quantity

    def update(self):
        # cursor.execute_many?
        for item in self.items:
            self.update_quantity(item['product_code'], item['quantity'])

    def update_quantity(self, product_code, quantity):
        query = "UPDATE {} SET {} = ? WHERE {} LIKE ?".format(
            self.table, self.quantity_column, self.product_code_column)
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(query, (quantity, product_code))
            self.db_connection.commit()
        except Exception as err:
            raise err
        finally:
            cursor.close()
