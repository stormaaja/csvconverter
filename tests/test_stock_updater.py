import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(1, os.path.dirname(".."))

import unittest
import sqlite3

from stock_updater import StockUpdater
from multiple_products_found_error import MultipleProductsFoundError
from product_not_found_error import ProductNotFoundError

DATABASE_FILE = "test_stock_updater.db"

class TestStockUpdater(unittest.TestCase):

    def tearDown(self):
        os.remove(DATABASE_FILE)

    def create_database(self, conn):
        cursor = conn.cursor()
        cursor.execute((
            "CREATE TABLE products"
            "(product_code text, quantity integer)"))
        cursor.execute(
            ("INSERT INTO products (product_code, quantity)"
            "VALUES ('123', 0)"))
        cursor.execute(
            ("INSERT INTO products (product_code, quantity)"
            "VALUES ('456', 0)"))
        conn.commit()
        cursor.close()

    def create_updater(self, conn):
        updater = StockUpdater(conn)
        updater.set_destination_colums("product_code", "quantity")
        updater.set_table("products")
        return updater

    def test_update_single(self):
        conn = sqlite3.connect(DATABASE_FILE)
        self.create_database(conn)

        updater = self.create_updater(conn)

        updater.update_quantity("123", 15)

        cursor = conn.cursor()
        cursor.execute(
            "SELECT quantity FROM products WHERE product_code LIKE '123'")
        row = cursor.fetchone()
        self.assertEqual(15, row[0])
        cursor.close()
        conn.close()

    def test_update_all(self):
        conn = sqlite3.connect(DATABASE_FILE)
        self.create_database(conn)

        updater = self.create_updater(conn)
        updater.set_items([
            { "product_code": "123", "quantity": 10 },
            { "product_code": "456", "quantity": 15 }
        ])
        updater.update()

        cursor = conn.cursor()
        cursor.execute(
            "SELECT quantity FROM products WHERE product_code LIKE '123'")
        row = cursor.fetchone()
        self.assertEqual(10, row[0])
        cursor.execute(
            "SELECT quantity FROM products WHERE product_code LIKE '456'")
        row = cursor.fetchone()
        self.assertEqual(15, row[0])
        cursor.close()
        conn.close()

    def test_update_multiple_hits_single(self):
        conn = sqlite3.connect(DATABASE_FILE)
        self.create_database(conn)

        cursor = conn.cursor()
        cursor.execute(
            ("INSERT INTO products (product_code, quantity)"
            "VALUES ('456', 0)"))
        conn.commit()
        cursor.close()

        updater = self.create_updater(conn)

        with self.assertRaises(MultipleProductsFoundError):
            updater.update_quantity("456", 15)

    def test_update_multiple_hits(self):
        conn = sqlite3.connect(DATABASE_FILE)
        self.create_database(conn)

        cursor = conn.cursor()
        cursor.execute(
            ("INSERT INTO products (product_code, quantity)"
            "VALUES ('456', 0)"))
        conn.commit()
        cursor.close()

        updater = self.create_updater(conn)

        updater.set_items([
            { "product_code": "123", "quantity": 10 },
            { "product_code": "456", "quantity": 15 }
        ])
        with self.assertRaises(MultipleProductsFoundError):
            updater.update()

    def test_not_found_single(self):
        conn = sqlite3.connect(DATABASE_FILE)
        self.create_database(conn)

        updater = self.create_updater(conn)

        with self.assertRaises(ProductNotFoundError):
            updater.update_quantity("1234", 15)


    def test_not_found(self):
        conn = sqlite3.connect(DATABASE_FILE)
        self.create_database(conn)

        updater = self.create_updater(conn)

        updater.set_items([
            { "product_code": "1234", "quantity": 10 },
            { "product_code": "456", "quantity": 15 }
        ])
        with self.assertRaises(ProductNotFoundError):
            updater.update()


if __name__ == '__main__':
    unittest.main()
