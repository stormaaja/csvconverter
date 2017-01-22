import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(1, os.path.dirname(".."))

import unittest
from csv_converter import CsvConverter

class TestCsvConverter(unittest.TestCase):

    def test_parse_csv(self):
        converter = CsvConverter("tests/data/data_1.csv")
        converter.setSourceColumns("tuotekoodi", "qty")
        converter.read_file()

    def test_convert_row(self):
        converter = CsvConverter("")
        row = converter.convertRow({
            "product_code": "some_code",
            "quantity": "50"
        })
        self.assertEqual("some_code", row["product_code"])

        with self.assertRaises(ValueError):
            row = converter.convertRow({
                "product_code": "23",
                "quantity": "error"
            })

        with self.assertRaises(ValueError):
            row = converter.convertRow({
                "product_code": "",
                "quantity": "error"
            })

        with self.assertRaises(ValueError):
            row = converter.convertRow({
                "product_code": "sd",
                "quantity": ""
            })



if __name__ == '__main__':
    unittest.main()
