import unittest
import moduleParser
import csv, os

class TestModuleParser(unittest.TestCase):
    def setUp(self):
        self.path = os.path.abspath(os.path.dirname(__file__))
    def test_zeroString(self):
        self.assertEqual(moduleParser.getInstance(''), 'Введена пустая строка')
    def test_csv(self):
        with open(f'{self.path}' + '\stringTests.csv', encoding='utf-8') as r_file:
            # Создаем объект reader, указываем символ-разделитель ","
            file_reader = csv.reader(r_file, delimiter=";")
            for i, row in enumerate(file_reader):
                if i != 0:
                    self.assertEqual(moduleParser.getInstance(row[0]), row[1])


if __name__ == "__main__":
    unittest.main()