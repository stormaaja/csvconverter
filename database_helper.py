#!/usr/bin/env python
# -*- coding: utf-8 -*-

def add_product(conn, product_code):
    cursor = conn.cursor()
    cursor.execute(
        ("INSERT INTO products (product_code, quantity)"
        "VALUES (?, 0)"), (product_code,))
    conn.commit()
    cursor.close()

def initialize(conn):
    cursor = conn.cursor()
    cursor.execute((
        "CREATE TABLE products"
        "(product_code text, quantity integer)"))
    conn.commit()
    cursor.close()

def add_test_products(conn):
    add_product(conn, "10004")
    add_product(conn, "10005")
    add_product(conn, "10006111")
    add_product(conn, "10008")
    add_product(conn, "10010101")