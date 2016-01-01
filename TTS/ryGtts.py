#!/usr/bin/python3
# coding: utf-8
import gtts
import os
import sys
import scipy.io.wavfile as wf


def ryTTS(aText='Wikipedia is a multilingual,', aLang='en', aFn='_ryTTS'):
    tts= None
    try:
        tts= gtts.gTTS(aText, aLang)
        fp= open(aFn+'.mp3','wb')
        tts.write_to_fp(fp)
        fp.seek(0, os.SEEK_END)
        sizeMp3= fp.tell()
        fp.close()
        print('ryTTS----> %s, %d (bytes)'%(aFn+'.mp3', sizeMp3))
    except:
        sizeMp3= 0
        print('ryTTS----> %s, %d (bytes)'%(aFn+'.mp3', sizeMp3))
    return sizeMp3, tts
        
def ryMp3toWav(aFn):
    
    fp= open(aFn+'.mp3','rb')
    fp.seek(0, os.SEEK_END)
    sizeMp3= fp.tell()
    fp.close()
    if sizeMp3 == 0:
        T=0
        return T

    #
    # using ffmpeg, mp3 ----> wav
    #
    cmdDos=   'ffmpeg -y -i {0} -vn -acodec pcm_s16le -ac 1 -ar {2} -f wav {1}'.format(aFn+'.mp3',aFn+'.wav',16000)
    cmdStatus= os.system(cmdDos)
    print('cmdStatus, cmdDos=',cmdStatus, cmdDos)

    fp= open(aFn+'.wav','rb')
    fp.seek(0, os.SEEK_END)
    sizeWav= fp.tell()
    fp.close()

    fs, x= wf.read(aFn+'.wav')
    L= len(x) # number of samples 

    T= L/fs # number of seconds

    #print('T(sec), fs(Hz), tts, L(samples), sizeMp3 (bytes), sizeWav(bytes)= ', 
    #      T, fs, tts, L, sizeMp3, sizeWav)
    
    return T #, fs, tts, L, sizeMp3, sizeWav 


aText='''
Wikipedia is a multilingual, web-based, free-content encyclopedia project supported by the Wikimedia Foundation and based on a model of openly editable content. The name "Wikipedia" is a portmanteau of the words wiki (a technology for creating collaborative websites, from the Hawaiian word wiki, meaning "quick") and encyclopedia. Wikipedia's articles provide links designed to guide the user to related pages with additional information.
Wikipedia is written collaboratively by largely anonymous volunteers who write without pay. Anyone with Internet access can write and make changes to Wikipedia articles, except in limited cases where editing is restricted to prevent disruption or vandalism. Users can contribute anonymously, under a pseudonym, or, if they choose to, with their real identity.
The fundamental principles by which Wikipedia operates are the five pillars. The Wikipedia community has developed many policies and guidelines to improve the encyclopedia; however, it is not a formal requirement to be familiar with them before contributing.
'''

if len(sys.argv)>=3:
    fnText= sys.argv[2]
    fp= open(fnText, 'r', encoding='utf8')
    aText= fp.read()
    fp.close()
    
import re
def _tokenize(text, max_size=100):
    """ Tokenizer on basic roman punctuation """ 

    punc = "¡!()[]¿?.,;:—«»\n" # for en, English
    punc += '！？．。，、；：'  # for zh-tw, and ja #'－／（）［］【】「」＜＞《》'
    
    punc_list = [re.escape(c) for c in punc]
    pattern = '|'.join(punc_list)
    parts = re.split(pattern, text)

    min_parts = []
    for p in parts:
        min_parts += _minimize(p, " ", max_size)
    return min_parts

def _minimize(thestring, delim, max_size=100):
    """ Recursive function that splits `thestring` in chunks
    of maximum `max_size` chars delimited by `delim`. Returns list. """ 

    if len(thestring) > max_size:
        idx = thestring.rfind(delim, 0, max_size)
        return [thestring[:idx]] + _minimize(thestring[idx:], delim, max_size)
    else:
        return [thestring]

aTextL=  _tokenize(aText)

#
# 字串處理做注音，注意必須純粹 ascii，英文字母， A-Z, a-z，
# 給 HTK 的 .lab
#
def text2phn(text):
    '''
    英文字，直接當音標！別的語言就沒這麼好康。
    但還是得處理乾淨，不能有大小寫英文字母A-Za-z及底線_以外的字母出現，
    不然 HTK 就當給你看！！
    '''

    phn= re.sub('\s+','_',text)      # 連續空白當成底線
    phn= re.sub('\'|\"|\-','',phn)   # 消除幾個符號，',",-
    phn= re.sub('^_|_$','',phn)      # 消除頭尾底線
    
    phn= phn.lower() # 不知是否必要需全小寫？？？ ## 需要！！！
    
    phn= 'sil_'+phn+'_sil' # 最後加上頭尾特殊靜音音標 sil
    
    errPhnL= re.findall('[^a-z_]',phn) # only [A-Za-z_] are allowed in HTK 
    if errPhnL != []:
        print('errPhn: in {0},  errPhnL= {1}'.format(text, errPhnL))
        return 'errPhn' #

    return phn


#
# 語音合成取聲音，存成 .wav 給 HTK 用
#
fnL= []
fp_allmp3= open('_all.mp3','wb')
for i, txt in enumerate(aTextL):
    
    fn= 'SN%04d'%(i) # 檔名數字前有補 0，補滿 4位數。  
    
    y,tts= ryTTS(aText= txt,  aFn= fn, aLang= 'en') 
    if y== 0: continue
    
    if tts != None:
        tts.write_to_fp(fp_allmp3) # for combine 2 one mp3 file
    
    T=   ryMp3toWav(fn)  # 給 HTK 的 .wav
    
    phn= text2phn(txt)
    t0= 0
    t1= int(T*1e7) # HTK 特殊的時間單位 1e-7 sec, int
    lab= '%d %d %s'%(t0, t1, phn)
    
    fnL += [fn, T, lab]
    
    fn +=   '.lab'      # 給 HTK 的 .lab
    fp=open(fn,'w')     # must be ascii encode
    fp.write(lab)
    fp.close()
    
fp_allmp3.close()

fp_text= open('_all.txt','w', encoding='utf-8')
fp_text.write('aText= """{0}"""\n\naTextL= {1}\n\nfnL= {2}'.format(aText, aTextL, fnL))
fp_text.close()


#
# 五鬼搬運，把東西搬進 _wav/
#

dirName= 'wavDir'
if len(sys.argv)>=2:
    dirName= sys.argv[1]

import shutil

if os.path.exists(dirName):
    shutil.rmtree(dirName, ignore_errors=True)
    
try:
    os.mkdir(dirName)
except OSError:
    print('OSError')

import glob
wavL= glob.glob('*.wav')
labL= glob.glob('*.lab')


for wav, lab in zip(wavL,labL):
    wavDest= os.path.join(dirName,wav)
    labDest= os.path.join(dirName,lab)
    try:
        os.rename(wav, wavDest)
        os.rename(lab, labDest)
    except:
        print('os.rename err!!!!')
        pass

# 特殊 _all.mp3 , _all.txt保留
specialFnL= ['_all.mp3','_all.txt']
for f in specialFnL:
    fDest= os.path.join(dirName,f)
    try:
        os.rename(f, fDest)
    except:
        print('os.rename err!!!!')
        pass

# 其餘 .mp3 刪掉
mp3L= glob.glob('*.mp3')        
for mp3 in mp3L:
    try:
        os.remove(mp3)
    except:
        print('os.remove err!!!!')
        pass




