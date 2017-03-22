#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiple_products_found_error import MultipleProductsFoundError
from product_not_found_error import ProductNotFoundError

class StockUpdater:

    def __init__(self, db_connection, query_format="%s"):
        self.db_connection = db_connection
        self.query_format = query_format

    def set_table(self, table):
        self.table = table

    def set_destination_colums(self, product_code, quantity):
        self.product_code_column = product_code
        self.quantity_column = quantity

    def check_product(self, product_code):
        cursor = self.db_connection.cursor()

        check_query = "SELECT COUNT(*) FROM {} WHERE {} LIKE {}".format(
            self.table, self.product_code_column, self.query_format)

        cursor.execute(check_query, (product_code,))
        product_count = cursor.fetchone()[0]
        cursor.close()

        if product_count == 0:
            raise ProductNotFoundError(
                "No product found with product code {}"
                .format(product_code))
        elif product_count > 1:
            raise MultipleProductsFoundError(
                "Multiple products found with product code {}"
                .format(product_code))

    def update_quantity(self, product_code, quantity):
        self.check_product(product_code)

        cursor = self.db_connection.cursor()
        query = "UPDATE {} SET {} = {} WHERE {} LIKE {}".format(
            self.table, self.quantity_column, self.query_format,
            self.product_code_column, self.query_format)
        try:
            cursor.execute(query, (quantity, product_code))
            self.db_connection.commit()
        except Exception as err:
            raise err
        finally:
            cursor.close()
