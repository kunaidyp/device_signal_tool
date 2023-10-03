import unittest

import project1
import read_file
import devices
from pathlib import Path


class TestProject1(unittest.TestCase):
    def test_read_input_file_exists(self):
        filename = '/Users/priskakndy/PycharmProjects/Project1/samples/sample_input.txt'
        filename = Path(filename)
        results = read_file.read_input_file(filename)
        self.assertIsNotNone(results)

    def test_read_input_file_not_exists(self):
        filename = '/Users/priskakndy/PycharmProjects/Project1/non_existent.txt'
        filename = Path(filename)
        results = read_file.read_input_file(filename)
        self.assertIsNone(results)