# TTS
* Introduction
<br>&nbsp;&nbsp;&nbsp;&nbsp;
Given a text as input, get voice from Google TTS(Text to Speech). Training voice data by HTK and produce text which contain sentences and timestamp.
<br><br>
* OS
  * ubuntu 14.04 64-bit with kernel 3.19.0
<br><br>
* Requirement
  * Python 3.4.3
  * gTTS 1.0.7
  * Scipy 0.13.3
  * HTK 3.4.1
  * FFmpeg 2.8.1
  <br><br>
* Installion
  * Python 3.4.3
    <br>&nbsp;&nbsp;&nbsp;&nbsp;
    `$ sudo apt-get install python3`
  * gTTS 1.0.7
    <br>&nbsp;&nbsp;&nbsp;&nbsp;
    `$ sudo pip3 install gtts`
  * Scipy 0.13.3
    <br>&nbsp;&nbsp;&nbsp;&nbsp;
    `$ sudo pip3 install scipy
`
  * HTK 3.4.1
    1. Go to http://htk.eng.cam.ac.uk and register an account
    2. Download source code of Linux version
    3. Decompress and compile it
    <br>&nbsp;&nbsp;&nbsp;
    `$ tar -zxvf HTK*.tar.gz || cd htk`
    <br>&nbsp;&nbsp;&nbsp;
    `$ ./configure --prefix=~/HTK`
    <br>&nbsp;&nbsp;&nbsp;
    `$ make all`
    4. Add path to profile
    <br>&nbsp;&nbsp;&nbsp;
    `$ echo '#HTK PATH' >> ~/.bashrc`
    <br>&nbsp;&nbsp;&nbsp;
    `$ echo 'export PATH=$PATH:$HOME/HTK/bin' >> ~/.bashrc`
    <br>&nbsp;&nbsp;&nbsp;
    `$ source ~/.bashrc`
  * FFmpeg 2.8.1
    <br>&nbsp;&nbsp;&nbsp;&nbsp;
    `$ sudo add-apt-repository ppa:jon-severinsson/ffmpeg`
    <br>&nbsp;&nbsp;&nbsp;&nbsp;
    `$ sudo apt-get update`
    <br>&nbsp;&nbsp;&nbsp;&nbsp;
    `$ sudo apt-get install ffmpeg`
    <br>&nbsp;&nbsp;&nbsp;&nbsp;
    `$ sudo apt-get install frei0r-plugins`
<br><br>
* Usage
  1. Get voice files from gTTS
      <br>&nbsp;&nbsp;
      `$ python3 ryGtts.py`
  2. Get sentences and timestamps by HTK
      <br>&nbsp;&nbsp;
      `$ python3 ryHailgn.py` 
      <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; or<br>&nbsp;&nbsp; 
      `$ python3 ryHailgn.py -d wavDir` (given a directory of wav file)
<br><br>

* Contact
  <pre>
  Prof:   Renyuan Lyu
  E-mail: <a href='mailto:renyuan.lyu@gmail.com'>renyuan.lyu@gmail.com</a>
  
  Author: Jin Ye
  E-mail: <a href='mailto:don0910129285@gmail.com'>don0910129285@gmail.com</a>
  </pre>
