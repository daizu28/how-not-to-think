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

    from jtalker import YomiParser
    from jtalker import jtalk
    import time
    
    phrase_arr = ["すもももももももものうち","new york","ニューヨーク","newspaper","こんにちは", "3.11","python","8月3日"]
    yomi_parser = YomiParser()

    start = time.perf_counter() # 開始時間

    phrase_yomi = yomi_parser.get_yomi("すもももももももものうち")
    jtalk(phrase_yomi, htsvoice='./models/takumi/takumi_normal.htsvoice', speed=0.2)

    end = time.perf_counter() - start # かかった時間
    print(f'{end}秒かかりました！')
