#coding: utf-8
import argparse
import csv
import os
import re
import subprocess

import MeCab as mecab

mecab_dic_dir = "/opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd"

class YomiParser:
    def __init__(self, base_path = "."):
        self.base_path = base_path
        self.eng_kana_dict = self.load_dict(f"{self.base_path}/dictionary/bep-eng.dic") | self.load_dict(f"{self.base_path}/dictionary/user.dic")
        self.mecab_dict = mecab_dic_dir
        self.yomi_tagger = mecab.Tagger(f"-O yomi -d {self.mecab_dict}")
        self.match_alpha = re.compile(r'^[a-zA-Z0-9]+$')

    def load_dict(self, dict_file = 'user.dic'):
        dict = {}
        with open(dict_file, mode='r', encoding='utf-8') as f:
            lines = csv.reader(f, delimiter=' ')
            for row in lines:
                if row[0] == '#': continue
                dict[row[0]] = row[1]
        return dict
    
    def set_dict_path(self, base_path):
        self.base_path = base_path

    def set_dict(self, dict):
        self.eng_kana_dict = dict

    def get_kana(self, eng):
        return self.eng_kana_dict[eng.upper()]

    def get_yomi(self, phrase):
        yomi = self.yomi_tagger.parse(phrase).strip()
        if phrase == yomi and self.match_alpha.match(phrase):
            yomi = self.get_kana(phrase)
        return yomi


def jtalk(t, htsvoice='./models/takumi/takumi_normal.htsvoice', speed=1.0, out='./out/open_jtalk.wav', callback=None):
    input = ['echo', t.encode(), '|']
    open_jtalk=['/opt/homebrew/bin/open_jtalk']
    mech = ['-x', mecab_dic_dir]
    htsvoice=['-m',htsvoice]
    speed=['-r',str(speed)]
    outwav=['-ow',out]
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    # c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    # c.stdin.write(t.encode())
    # c.stdin.close()
    # c.wait()
    subprocess.run(cmd, input=t, capture_output=True, text=True)
    callback(out)

#  音源再生
def play(out):
    afplay = ['afplay', out]
    wr = subprocess.Popen(afplay)

def main():
    parser = argparse.ArgumentParser(description='OpenJtalkで音声合成')
    parser.add_argument('phrase', type=str, help='合成する音声のテキスト')
    parser.add_argument('--htsvoice', type=str, default='./models/takumi/takumi_normal.htsvoice', help='HTS音響モデル')
    parser.add_argument('--speed', type=float, default=1.0, help='話速')
    # parser.add_argument('--out', type=str, default='out/open_jtalk.wav', help='出力ファイル名')
    args = parser.parse_args()

    yomi_parser = YomiParser()
    phrase_yomi = yomi_parser.get_yomi(args.phrase)
    print(f"{phrase_yomi=}")
    dirname = os.path.dirname(f"out/{phrase_yomi}.wav")
    os.makedirs(dirname, exist_ok=True)
    jtalk(phrase_yomi, htsvoice=args.htsvoice, speed=args.speed, out=f"out/{phrase_yomi}.wav", callback=play)

if __name__ == '__main__':
    main()
