# pythonを使った音声合成

## 環境構築
これ以降プロジェクトファイルのディレクトリ下のターミナルで作業
### Python仮想環境

Pythonのバージョン確認

Python3.9以上が必要

```
python3 -V
```

venvで仮想環境構築
```
python3 -m venv env
```

venvを起動
```
source env/bin/activate
```

pipでパッケージのインストール

pipを最新状態にする
```
pip install --upgrade pip
```

pipでrequirements.txtよりパッケージをインストール
```
pip install -r requirements.txt

# M1, M2 Macの場合
pip install --no-binary :all: -r requirements.txt
```

## OpenJtalkを用意
### OpenJtalkのインストール
Mac
```
brew install open-jtalk
```

## 形態素解析辞書NEologdのインストール
参考：https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md

手順
```
brew install mecab mecab-ipadic git curl xz
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd
./bin/install-mecab-ipadic-neologd -n
# yesと入力
```

インストール先の確認
```
echo `mecab-config --dicdir`"/mecab-ipadic-neologd"
```

jtalker.pyにインストール先を書き加える
```
mecab_dic_dir = "mecab-ipadic-neologdのインストール先"
```

## Python環境を閉じる
作業が終わった際にvenvで作ったPython環境を閉じます
```
deactivate
```

再度、Python環境を開く場合
```
source env/bin/activate
```

## 実行の仕方
```
python jtalker.py 合成したいテキスト

ex.
python jtalker.py りんご

音響モデルを変える場合
python jtalker.py りんご --htsvoice ./models/mei/mei_normal.htsvoice

話速を変える場合（デフォルトは1.0）
python jtalker.py りんご --speed 0.5
```

## テストスクリプトの使い方
WIP