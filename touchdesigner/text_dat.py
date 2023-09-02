# 環境設定
import sys
env_path = '/Users/sunada.norihiro/Documents/GitHub/soundtest/env/lib/python3.9/site-packages'
base_path = '/Users/sunada.norihiro/Documents/GitHub/soundtest'
for path in [env_path, base_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

from jtalker import JTalkWrapper

hts_path = f"{base_path}/models/takumi/takumi_normal.htsvoice"
voice_speed = 0.2
out_dir = f"{base_path}/out/"
jtalk = JTalkWrapper(
    hts_path=hts_path,
    speed=voice_speed, 
    out_dir=out_dir,
    play=False,
)

def onSynthesized(path):
    """ 
    音声合成完了時のコールバック
    引数:
    path: 合成音声の保存先パス
    """
    print("onSynthesized", path)
    mod("callback").run()

input = op('input_text').text
jtalk.synthesize(input, callback=onSynthesized)
