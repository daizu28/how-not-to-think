import os
import sys
import unittest

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
            ["YCAM","ワイカム"]
        ]

        for (phrase, expected) in phrase_arr:
            actual = yomi_parser.get_yomi(phrase)
            print(f"{expected = }, \t{actual = }")
            self.assertEqual(expected, actual)

if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    unittest.main()
