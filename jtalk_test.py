#coding: utf-8
import subprocess
from datetime import datetime

def jtalk(t):
    open_jtalk=['open_jtalk']
    mech=['-x','/usr/local/Cellar/open-jtalk/1.11/dic/install-mecab-ipadic-neologd']
    htsvoice=['-m','/Users/kobayashireiina/Documents/soundtest/soundtest/mei/mei_normal.htsvoice']
    speed=['-r','1.0']
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(t.encode())
    c.stdin.close()
    c.wait()
    aplay = ['afplay','-q','open_jtalk.wav']
    wr = subprocess.Popen(aplay)

def say_datetime():
    d = datetime.now()
    text = 'newspaper' 
    jtalk(text)

if __name__ == '__main__':
    say_datetime()

