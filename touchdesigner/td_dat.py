# 環境設定
import sys
#env_path = '/Users/shima/Desktop/howtonotthink/enviroment/env/lib/python3.11/site-packages'
env_path = "'"+op("ENV_PATH").text+"'"
base_path = '/Users/shima/Desktop/howtonotthink/how-not-to-think-main'
for path in [env_path, base_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

from jtalker import YomiParser
from jtalker import jtalk

yomi_parser = YomiParser(base_path)

# 音声合成完了時のコールバック
def onSynthesized(path):
    print("onSynthesized", path)
    mod("callback").run()

# 音声合成
def synthesize(input, callback):
    phrase_yomi = yomi_parser.get_yomi(input)
    hts_path = f"{base_path}/models/takumi/takumi_normal.htsvoice"
    voice_speed = 0.2
    out_path = f"{base_path}/out/{phrase_yomi}.wav"
    jtalk(phrase_yomi, htsvoice=hts_path, speed=voice_speed, out=out_path, callback=callback)

input = op('input_text').text
synthesize(input, onSynthesized)
