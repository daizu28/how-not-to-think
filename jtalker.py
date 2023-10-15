#coding: utf-8
import argparse
import csv
import os
import re
import subprocess
from subprocess import PIPE
import MeCab as mecab
from pydub import AudioSegment
from pydub.silence import split_on_silence
from scipy.io.wavfile import read, write
import numpy as np

#getMecabDir = subprocess.run(["mecab-config", "--dicdir"], stdout=PIPE, text=True)
#getMecabDir = '/opt/homebrew/lib/mecab/dic' 
#mecab_dic_dir = getMecabDir.stdout.replace("\n", "") + "/mecab-ipadic-neologd"

# "/opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd"

#getMecabDir = subprocess.run(["mecab-config", "--dicdir"], stdout=PIPE, text=True, shell=True)
#mecab_dic_dir = getMecabDir.stdout.replace("\n", "") + "/mecab-ipadic-neologd"

mecab_dic_dir ='/opt/homebrew/lib/mecab/dic/mecab-ipadic-neologd'

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
            try:
                yomi = self.get_kana(phrase)
            except Exception as e:
                yomi
        return yomi


def jtalk(t, htsvoice='./models/takumi/takumi_normal.htsvoice', speed=1.0, out='./out/open_jtalk.wav'):
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
    removeSilence(out)

def removeSilence(audio_path):
    rate, audio = read(audio_path)
    aud = AudioSegment(
        audio.tobytes(),
        frame_rate = rate,
        sample_width = audio.dtype.itemsize,
        channels = 1)
    audio_chunks = split_on_silence(
        aud,
        min_silence_len = 1000,
        silence_thresh = -45,
        keep_silence = 500,)
    audio_processed = sum(audio_chunks)
    audio_processed = np.array(audio_processed.get_array_of_samples())
    write(audio_path, rate, audio_processed)

#  音源再生
def play(out):
    afplay = ['afplay', out]
    wr = subprocess.Popen(afplay)

def main():
    parser = argparse.ArgumentParser(description='OpenJtalkで音声合成')
    parser.add_argument('phrase', type=str, help='合成する音声のテキスト')
    parser.add_argument('--htsvoice', type=str, default='./models/takumi/takumi_normal.htsvoice', help='HTS音響モデル')
    parser.add_argument('--speed', type=float, default=1.0, help='話速')
    parser.add_argument('--outdir', type=str, default='./out/', help='出力先ディレクトリ')
    args = parser.parse_args()

    jtalk = JTalkWrapper(
        hts_path=args.htsvoice,
        speed=args.speed, 
        out_dir=args.outdir,
        play=True
    )
    jtalk.synthesize(input=args.phrase)


class JTalkWrapper:
    yomi_parser = None
    hts_path = None
    voice_speed = None
    out_dir = None

    def __init__(self, base_path = ".", model_path='./models',voice='takumi', voice_mood='normal', hts_path='./models/takumi/takumi_normal.htsvoice', speed=1.0, out_dir='./out/', play=False) -> None:
        hts_model_path=model_path
        if voice=='takumi':
            if voice_mood=='normal':
                hts_model_path+='/takumi/takumi_normal.htsvoice'
            elif voice_mood=='happy':
                hts_model_path+='/takumi/takumi_happy.htsvoice'
            elif voice_mood=='sad':
                hts_model_path+='/takumi/takumi_sad.htsvoice'
            elif voice_mood=='angry':
                hts_model_path+='/takumi/takumi_angry.htsvoice'
            else:
                hts_model_path+='/takumi/takumi_normal.htsvoice'
        elif voice=='mei':
            if voice_mood=='normal':
                hts_model_path+='/mei/mei_normal.htsvoice'
            elif voice_mood=='happy':
                hts_model_path+='/mei/mei_happy.htsvoice'
            elif voice_mood=='sad':
                hts_model_path+='/mei/mei_sad.htsvoice'
            elif voice_mood=='angry':
                hts_model_path+='/mei/mei_angry.htsvoice'
            else:
                hts_model_path+='/mei/mei_normal.htsvoice'
        else:
            hts_model_path=hts_path
            
        self.yomi_parser = YomiParser(base_path)
        self.hts_path = hts_model_path
        self.voice_speed = speed
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)
        self.play = play
    
    def synthesize(self, input, callback=None):
        phrase_yomi = self.yomi_parser.get_yomi(phrase=input)
        out_path = f"{self.out_dir}/{phrase_yomi}.wav"
        jtalk(phrase_yomi, htsvoice=self.hts_path, speed=self.voice_speed, out=out_path)

        if self.play:
            play(out_path)
        
        if callable(callback):
            callback(out_path)

if __name__ == '__main__':
    main()
