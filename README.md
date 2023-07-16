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

## TouchDesigner上でうまくいかないときに試してみること
pyenvのインストール 下記をターミナルに入れる
```
curl -L https://github.com/yyuu/pyenv-installer/raw/master/bin/pyenv-installer | bash
```
remove〜って出たら~~~/.pyenvってのを消せって書いてると思うのでそれをパスの場所を辿って消す。または、
```
rm -rf /Users/〜〜〜/.pyenv
```

3.9.1のインストール
```
pyenv install 3.9.1
```
pyenvでエラーが出たら下記
```
eval "$(pyenv init -)"
```

3.9.1で仮想環境の作成
```
pyenv virtualenv 3.9.1 venv_3.9
```

仮想環境のActivate
```
pyenv activate venv_3.9
```

バージョンの確認　3.9.1じゃなかったらどこかおかしい
```
python --version
```

mecabを入れる
```
pip install mecab
```

requirements.txtの中身をもう一度入れる
pipでrequirements.txtよりパッケージをインストール
```
pip install -r requirements.txt

# M1, M2 Macの場合
pip install --no-binary :all: -r requirements.txt
```

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
