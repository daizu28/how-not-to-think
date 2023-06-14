#coding: utf-8
import argparse
import csv
import re
import subprocess

import MeCab as mecab

mecab_dic_dir = "/opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd"

class YomiParser:
    def __init__(self):
        self.eng_kana_dict = self.load_dict('dictionary/bep-eng.dic') | self.load_dict('dictionary/user.dic')
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
    
    def set_dict(self, dict):
        self.eng_kana_dict = dict

    def get_kana(self, eng):
        return self.eng_kana_dict[eng.upper()]

    def get_yomi(self, phrase):
        yomi = self.yomi_tagger.parse(phrase).strip()
        if phrase == yomi and self.match_alpha.match(phrase):
            yomi = self.get_kana(phrase)
        return yomi


def jtalk(t, htsvoice='./models/takumi/takumi_normal.htsvoice', speed=1.0):
    open_jtalk=['open_jtalk']
    mech = ['-x', mecab_dic_dir]
    htsvoice=['-m',htsvoice]
    speed=['-r',str(speed)]
    outwav=['-ow','out/open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(t.encode())
    c.stdin.close()
    c.wait()

    #  音源再生
    afplay = ['afplay','out/open_jtalk.wav']
    wr = subprocess.Popen(afplay)

def main():
    parser = argparse.ArgumentParser(description='OpenJtalkで音声合成')
    parser.add_argument('phrase', type=str, help='合成する音声のテキスト')
    parser.add_argument('--htsvoice', type=str, default='./models/takumi/takumi_normal.htsvoice', help='HTS音響モデル')
    parser.add_argument('--speed', type=float, default=1.0, help='話速')
    args = parser.parse_args()

    yomi_parser = YomiParser()
    phrase_yomi = yomi_parser.get_yomi(args.phrase)
    print(f"{phrase_yomi=}")
    jtalk(phrase_yomi, htsvoice=args.htsvoice, speed=args.speed)

if __name__ == '__main__':
    main()
