# pythonを使った音声合成

# 環境構築

## 動作環境
- M1 Mac

### 準備
[brew](https://brew.sh/)がない場合はあらかじめインストールしてください

**brewがない場合**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## ダウンロード
ターミナルで以下を実行してください
```
git git@github.com:daizu28/how-not-to-think.git
cd how-not-to-think/
```

## Python仮想環境構築
pyenvを用いてPythonのバージョン管理

### インストール
```
brew update
brew pyenv
eval "$(pyenv init -)"
pyenv install 3.9.1
pyenv local 3.9.1
```

正しくインストールできたか確認
以下を実行

```
python -V
```
`Python 3.9.1` と出力されたらOK

### venvで仮想環境構築
仮想環境の構築と起動
```
python -m venv env
source env/bin/activate
```

pipでパッケージのインストール

**M1, M2 Macの場合**
```
pip install --upgrade pip
pip install mecab-python3 --no-binary :all:
pip install -r requirements.txt
```

## OpenJtalk, mecab, 形態素解析
### インストール
```
brew install open-jtalk mecab mecab-ipadic xz ffmpeg
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd
./bin/install-mecab-ipadic-neologd -n -a
cd ../
```
途中`yes`と入力して進む

## 動作確認：音声合成を試す
```
python jtalker.py "合成したいテキスト"

例：
python jtalker.py りんご

音響モデルを変える場合
python jtalker.py りんご --htsvoice ./models/mei/mei_normal.htsvoice

話速を変える場合（デフォルトは1.0）
python jtalker.py りんご --speed 0.5
```

## 2回目以降に利用するとき
### Python環境を閉じる
作業が終わった際にPython仮想環境を閉じる
```
deactivate
```

再度、Python環境を開く
```
source env/bin/activate
```

## テストスクリプトの使い方
WIP

# TouchDesignerを実行する際の手順

作った仮想環境のパッケージ類がどこにあるか知りたいので、仮想環境のディレクトリを探す
```
python -m site
```

↓ターミナルの出力の中の一部
```
sys.path = [
  '/Users/ユーザー名/Desktop/howtonotthink/enviroment',
  '/Users/ユーザー名/.pyenv/versions/3.9.1/lib/python39.zip',
  '/Users/ユーザー名/.pyenv/versions/3.9.1/lib/python3.9',
  '/Users/ユーザー名/.pyenv/versions/3.9.1/lib/python3.9/lib-dynload',
  '/Users/ユーザー名/.pyenv/versions/venv_3.9_1/lib/python3.9/site-packages',　←これがほしいのでここだけコピーする
]
```

コピーしたものをTouchDesigner上のコード内のenv_pathに入れる


## トラブルシューティング
### pyenvのインストール
#### remove〜って出たら~~~/.pyenvってのを消せって書いてると思うのでそれをパスの場所を辿って消す。
```
rm -rf /Users/〜〜〜/.pyenv
```

# 参考
- 形態素解析辞書NEologd : https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md