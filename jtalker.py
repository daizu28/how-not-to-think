#coding: utf-8
import csv
import re
import subprocess

import MeCab as mecab

class YomiParser:
    def __init__(self):
        self.eng_kana_dict = self.load_dict('dictionary/bep-eng.dic') | self.load_dict('dictionary/user.dic')
        self.mecab_dict = "/usr/local/lib/mecab/dic/mecab-ipadic-neologd"
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
    mech = ['-x', '/usr/local/lib/mecab/dic/mecab-ipadic-neologd']
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
    phrase="りんご"
    yomi_parser = YomiParser()
    phrase_yomi = yomi_parser.get_yomi(phrase)
    print(f"{phrase_yomi=}")
    jtalk(phrase_yomi, htsvoice='./models/takumi/takumi_normal.htsvoice', speed=1.0)

if __name__ == '__main__':
    main()
