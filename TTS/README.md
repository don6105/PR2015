* Introduction
<br>&nbsp;&nbsp;&nbsp;&nbsp;
Given a test as input, get voice from Google TTS(Text to Speech). Training voice data by HTK and produce text which contain sentences and timestamp.
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
