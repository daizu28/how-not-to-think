# 環境設定
import sys
env_path = '/Users/sunada.norihiro/Documents/GitHub/soundtest/env/lib/python3.9/site-packages'
base_path = '/Users/sunada.norihiro/Documents/GitHub/soundtest'
brew_path = '/opt/homebrew/bin'
for path in [env_path, base_path, brew_path]:
    if path not in sys.path:
        sys.path.insert(0, path)

from jtalker import JTalkWrapper

jtalk = JTalkWrapper(
	base_path=base_path,
    hts_path=f"{base_path}/models/takumi/takumi_normal.htsvoice",
    speed=0.2, 
    out_dir=f"{base_path}/out/",
    play=False,
)

def onSynthesized(path):
    """ 
    音声合成完了時のコールバック
    引数:
    path: 合成音声の保存先パス
    """
    print("onSynthesized", path)
    op("outputPath").text = path
    mod("callback").run()

input = op('input_text').text
jtalk.synthesize(input, callback=onSynthesized)
