import os
import sys
import unittest
import csv

class TestFunc(unittest.TestCase):
    def test_func(self):
        from jtalker import YomiParser
        yomi_parser = YomiParser()
        phrase_arr = [
            ["すもももももももものうち","スモモモモモモモモノウチ"],
            ["new york","ニューヨーク"],
            ["newspaper","ニュースペーパー"],
            # ["こんにちは","コンニチワ"], 
            ["3.11","サンテンイチイチ"],
            ["8月3日","ハチガツミッカ"],
            ["python","パイソン"],
            ["YCAM","ワイカム"],
            ["hello","ハロー"],
            ["helllo","helllo"],
        ]

        for (phrase, expected) in phrase_arr:
            actual = yomi_parser.get_yomi(phrase)
            print(f"{expected = }, \t{actual = }")
            self.assertEqual(expected, actual)

    def test_words(self):
        from jtalker import YomiParser
        yomi_parser = YomiParser()

        with open('test/words.csv') as f:
            for row in csv.reader(f):
                input = row[0]
                expected = row[1]
                actual = yomi_parser.get_yomi(input)
                print(f"{input = }, \t{expected = }, \t{actual = }")
                self.assertEqual(expected, actual)

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    unittest.main()
