import unittest
from file_handler.file_reader import read_file

class TestFileReader(unittest.TestCase):
    def test_read_json(self):
        data = read_file("sample.json")
        self.assertIsInstance(data, dict)

    def test_read_yaml(self):
        data = read_file("sample.yaml")
        self.assertIsInstance(data, dict)

    def test_read_csv(self):
        data = read_file("sample.csv")
        self.assertIsInstance(data, list)
        self.assertTrue(all(isinstance(row, dict) for row in data))

    def test_read_txt(self):
        data = read_file("sample.txt")
        self.assertIsInstance(data, list)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_file("nonexistent.file")

    def test_unsupported_format(self):
        with self.assertRaises(ValueError):
            read_file("unsupported.format")
