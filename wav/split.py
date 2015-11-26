import scipy.io.wavfile
import scipy.signal as signal
import pylab as pl
import numpy as np

wavFile='g01.wav'
fs, wav= scipy.io.wavfile.read(wavFile)

%pl inline 
x= pl.plot(wav)

#頻率 = 16000次/每秒
sampling_rate = 16000
#取樣頻率 16次/每秒
F = 16
#沈默間隔
H = int (F * 0.5)

S = int( sampling_rate/F )
print( "S=%d" % S )

#取樣
A= []
for i in range( 0, len(wav), S ):
    A.append( abs(wav[i]) )

#平均值，音量大小門檻
M = np.mean(A) * 0.1

#時間點
T = []

#一秒低於平均值就紀錄時間點
for i in range( 0, len(A)-F, F ):
    x = 0
    for j in range(0,F):
        if A[ i+j ] < M:
            x += 1
    if x >= H :
        T.append( i/F )

print("len(T)=%d" % len(T) )

for i in range( 0, len(T) ):
    print( int(T[i]/60), int(T[i]%60), sep=":" )
