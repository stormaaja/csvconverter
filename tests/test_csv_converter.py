import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(1, os.path.dirname(".."))

import unittest
import warnings

from csv_converter import CsvConverter

class TestCsvConverter(unittest.TestCase):

    def test_parse_csv(self):
        converter = CsvConverter("tests/data/data_1.csv")
        converter.setSourceColumns("tuotekoodi", "qty")
        converter.read_file()

    def test_parse_invalid_csv(self):
        converter = CsvConverter("tests/data/data_2.csv")
        converter.setSourceColumns("tuotekoodi", "qty")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            converter.read_file()

            assert len(w) == 3
            assert issubclass(w[-1].category, UserWarning)
            assert "Invalid row" in str(w[-1].message)

    def test_convert_row_success(self):
        converter = CsvConverter("")
        row = converter.convertRow({
            "product_code": "some_code",
            "quantity": "50"
        })
        self.assertEqual("some_code", row["product_code"])

    def test_convert_row_invalid_quantity(self):
        converter = CsvConverter("")

        with self.assertRaises(ValueError):
            row = converter.convertRow({
                "product_code": "23",
                "quantity": "error"
            })

    def test_convert_row_invalid_product_code(self):
        converter = CsvConverter("")
        with self.assertRaises(ValueError):
            row = converter.convertRow({
                "product_code": "",
                "quantity": "error"
            })

    def test_convert_row_invalid_values(self):
        converter = CsvConverter("")
        with self.assertRaises(ValueError):
            row = converter.convertRow({
                "product_code": "sd",
                "quantity": ""
            })



if __name__ == '__main__':
    unittest.main()
