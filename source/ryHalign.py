#!/usr/bin/python3
# coding: utf-8
import os
import glob
import re
import shutil

globalCmdNum = 0
def os_system(cmd):
    global globalCmdNum
    
    #收集一下 htk 的 error 或 warning 訊息
    if globalCmdNum==0:
        os.system(' echo > _h01.dbg')
        os.system(' echo > _h02.dbg')
    cmd += ' 1>> _h01.dbg 2>> _h02.dbg'
    
    #真正執行命令在此！
    status= os.system(cmd)
    os.system('echo "(globalCmdNum, status, cmd)= %03d, %d,----> %s"'%(globalCmdNum, status, cmd))

    #後端繼續蒐集 error 或 warning 訊息
    print( '(globalCmdNum, status, cmd)= %03d, %d,----> %s '%(globalCmdNum, status, cmd))
    globalCmdNum +=1
    
    return status

def genScpFiles(dirName):
	#產生 4 個 .scp ----> spWav.scp, spLab.scp, spMfc.scp, spWav2Mfc.scp
	fnName= '*.wav'
	pathName= os.path.join(dirName, fnName)
	wavL= glob.glob(pathName)
	wavScp= '\n'.join(wavL)
	
	wavScp= wavScp.replace('\\','/') # 寫在.scp內的path 分隔用正斜/
	labScp= re.sub('.wav','.lab', wavScp)
	mfcScp= re.sub('.wav','.mfc', wavScp)
	
	wmScp= ''
	for w,m in zip(wavScp.split('\n'), mfcScp.split('\n')):
		wmScp += w+'\t'+m+'\n'
	
	completed_file = 0
	
	try:
		f=open('spWav.scp','w')
	except:
		print("echo 'open \'spWav.scp\'file fail' > _h02.dbg")
	else:
		f.write(wavScp)
		f.close()
		if os.stat('spWav.scp').st_size > 0:
			completed_file += 1
	
	try:
		f=open('spLab.scp','w')
	except:
		print("echo 'open \'spLab.scp\'file fail' > _h02.dbg")
	else:
		f.write(labScp)
		f.close()
		if os.stat('spLab.scp').st_size > 0:
			completed_file += 1
	
	try:
		f=open('spWav2Mfc.scp','w')
	except:
		print("echo 'open \'spWav2Mfc.scp\'file fail' > _h02.dbg")
	else:
		f.write(wmScp)
		f.close()
		if os.stat('spWav2Mfc.scp').st_size > 0:
			completed_file += 1
	
	try:
		f=open('spMfc.scp','w')
	except:
		print("echo 'open \'spMfc.scp\'file fail' > _h02.dbg")
	else:
		f.write(mfcScp)
		f.close()
		if os.stat('spMfc.scp').st_size > 0:
			completed_file += 1
	
	#check size of 4 files all greater than 0 
	if completed_file == 4:
		return True
	else:
		return False
    
#genScpFiles('en01_womanright')

def 建立Hmm原型(N=1, M=1, D=39, fileName=''):
    '''
    ----> myHmmPro (沒延伸檔名的) hmm 原型 檔
    '''
    
    #global hmm原型檔名
    hmm原型檔名='myHmmPro'   #  這一行是在此新加的，原先是設定為global變數
    
    if fileName=='':    fileName=hmm原型檔名
    
    dotPosition=fileName.find('.')
    if dotPosition>=0:    fileName=fileName[0:dotPosition]
    
    print ('\n\nCreateHProto....\n',fileName,'\nN = ',N,',M = ',M,'\n\n')
    hProto= '~h '+ '"'+fileName +'"'+'\n'             + '~o <VecSize> '+str(D) +'\n'             +'<MFCC_0_D_A> <StreamInfo> 1 '+ str(D)+'\n'             +'\n<BeginHMM>'+'\n'

    
    hProto += '<NumStates> '+ str(N+2) +'\n'
    
    for state in range(2,N+2): # 2...(N+1)
        hProto +='\n'
        hProto += ' <State> '+ str(state) +' '+' <NumMixes> '+str(M) +' <Stream> 1 '+'\n'
        
        for mixture in range(1, M+1): # 1...M
            hProto += '  <Mixture> '+str(mixture) + ' ' +str(1.0/M) +'\n'
            
            hProto += '   <Mean> '+str(D) +'\n'
            hProto += '    '
            for i in range(D):
                hProto += str(0)+' '
            hProto += '\n'
            
            hProto += '   <Variance> '+str(D) +'\n'
            hProto += '    '
            for i in range(D):
                hProto += str(1)+' '
            hProto += '\n'
    
    hProto += '\n<TransP> '+str(N+2) +'\n'

    
    for i in range(0,1):
        hProto +=' '
        for j in range(0,N+2):
            if j==1: aij=1.0
            else: aij=0.0
            hProto += str(aij)+' '
        hProto += '\n'
    for i in range(1,N+1):
        hProto +=' '
        for j in range(0,N+2):
            if j==i: aij=0.6
            elif j==(i+1): aij=0.4
            else: aij=0.0
            hProto += str(aij)+' '
        hProto += '\n'
    for i in range(N+1,N+2):
        hProto +=' '
        for j in range(0,N+2):
            aij=0.0
            hProto += str(aij)+' '
        hProto += '\n'
    
    hProto += '\n'+'<EndHMM>'+'\n'

   
    #fileName= 'hProto.hmm' 檔名似乎得和 ~h "..." 中一致，否則會出錯, .hmm 沒關係 
    f=open(fileName, 'w')
    #f=open(fileName,'w',encoding='utf-8-sig')
    f.write(hProto)
    f.close()
    
    return hProto


def htk00_製造各個HtkTool所需的參數檔():

    # also need create file list, *.scp
    '''
    f=open('spWav.scp','w')
    f.write(spWav_scp)
    f.close()
    f=open('spLab.scp','w')
    f.write(spLab_scp)
    f.close()
    f=open('spWav2Mfc.scp','w')
    f.write(spWav2Mfc_scp)
    f.close()
    f=open('spMfc.scp','w')
    f.write(spMfc_scp)
    f.close()
    '''
    
    hLed_led='''
    #### hLed.led
    EX    # expand word into phone
    '''
    
    hLed00_led='''
    #### hLed00.led
    #EX    # expand word into phone
    '''
    
    hCopy_conf='''
     SOURCEKIND     = WAVEFORM
     TARGETKIND     = MFCC_0     #12d(MFCC)+1d(E) = 13d
     SOURCEFORMAT   = WAV #NIST    #TIMIT
     SOURCERATE     = 625        # T=625e-7 sec ==> Fs = 16KHz
     TARGETRATE     = 100000      # 10 ms
     
     ENORMALISE=F   # for realtime test
        
    '''
    
    hInit_conf='''

    TARGETKIND = MFCC_0_D_A
    SAVEGLOBOPTS = TRUE
    
    KEEPDISTINCT=F
        
    '''
    
    hRest_conf='''

    TARGETKIND = MFCC_0_D_A
    SAVEGLOBOPTS = TRUE
    
    KEEPDISTINCT=F
        
    '''
    
    hErest_conf='''

    TARGETKIND = MFCC_0_D_A
    SAVEGLOBOPTS = TRUE
    
    KEEPDISTINCT=T
    BINARYACCFORMAT=T
        
    '''
    
    hVite_conf='''

    TARGETKIND = MFCC_0_D_A
    SAVEGLOBOPTS = TRUE
    
    KEEPDISTINCT=F
    BINARYACCFORMAT=F
        
    '''

    f=open('hLed.led','w')
    f.write(hLed_led)
    f.close()
    
    f=open('hLed00.led','w')
    f.write(hLed00_led)
    f.close()
    
    f=open('hCopy.conf','w')
    f.write(hCopy_conf)
    f.close()

    f=open('hInit.conf','w')
    f.write(hInit_conf)
    f.close()

    f=open('hRest.conf','w')
    f.write(hRest_conf)
    f.close()
    
    f=open('hErest.conf','w')
    f.write(hErest_conf)
    f.close()
    
    f=open('hVite.conf','w')
    f.write(hVite_conf)
    f.close()
    
    建立Hmm原型(N=3, M=6)

def htk01_處裡語音標籤及詞典():
	os_system('HLEd -A -i spLab00.mlf -n spLab00.lst -S spLab.scp  hLed00.led')
	os_system('HLEd -A -i spLab.mlf -n spLab.lst -S spLab.scp  hLed.led')
	lst2dic()
	os_system('HLEd -A -i spLab_p.mlf -n spLab_p.lst -S spLab.scp -I spLab.mlf -d spLab_p.dic hLed.led')


def lst2dic():

    f= open('spLab.lst')#,encoding='utf8')
    lines= f.readlines()
    f.close()

    lines.sort()  ## htk.dic 需要 sort
    
    f= open('spLab.lst','w')#,encoding='utf8')
    for l in lines:
        f.write(l)
    f.close()

    #global mList
    #mList=[]
    D= ''
    Dp= ''
    for l in lines:
        d=l.rstrip('\n')
        D += d+' '+d+'\n'
        
        if d=='sil' or len(d)<2:
            ps=d
        else: #(len(d))>=2:
            ps=''
            for n in range(len(d)-1):
                ps += d[n]+d[n+1]+' '
            
        Dp += d+' '+ps+'\n'
        
        #mList.append(d)
    f= open('spLab.dic','w')#,encoding='utf8')
    f.write(D)
    f.close()

    f= open('spLab_p.dic','w')#,encoding='utf8')
    f.write(Dp)
    f.close()



def htk02_擷取語音特徵及訓練語音模型():
	os_system('HCopy -A -C hCopy.conf -S spWav2Mfc.scp')
	os_system('mkdir hmms_p')
	
	f= open('spLab_p.lst')#,encoding='utf-8')
	lines=f.readlines()
	f.close()
	
	mList=[]
	for l in lines:
		m = l.strip('\n')
		mList.append(m)
	
	m = 'myHCompV'
	os_system('HCompV -A -C hInit.conf -S spMfc.scp -m -I spLab_p.mlf -M hmms_p/ -o '+m+' myHmmPro')
	
	f= open('hmms_p/'+m)
	myHCompV=f.read()
	f.close()
	
	for m in mList:
		myModel=myHCompV.replace('myHCompV',m)
		f=open('hmms_p/'+m,'w')#,encoding='utf-8')
		f.write(myModel)
		f.close()
	'''
	for m in mList:
		os_system('HInit -A -C hInit.conf -S spMfc.scp  -I spLab_p.mlf -m 1 -i 10 -l '+m+' -M hmms_p/ -o '+m+' hmms_p/'+m)
	for m in mList:
		os_system('HRest -A -C hRest.conf -S spMfc.scp -I spLab_p.mlf -m 1 -i 10 -u tmvw -w 3 -v 0.05 -l '+m+' -M hmms_p/ hmms_p/'+m)
	'''
	for i in range(5):
		print('[%d]HERest '%i)
		os_system('HERest -A -C hErest.conf -S spMfc.scp -p 1 -t 2000.0 -w 3 -v 0.05 -I spLab_p.mlf -M hmms_p -d hmms_p/ spLab_p.lst')
		os_system('HERest -A -C hErest.conf -p 0 -t 2000.0 -w 3 -v 0.05 -I spLab_p.mlf -M hmms_p/ -d hmms_p/ spLab_p.lst hmms_p/HER1.acc')


def htk03_語音文字對齊():

    os_system('HVite -A -C hVite.conf  -S spMfc.scp  -a -d hmms_p/ -i spLab_aligned.mlf -I spLab.mlf spLab_p.dic spLab_p.lst')
    print('----> spLab_aligned.mlf\n')


import sys

def 主程式():
    
    dirName= 'wavDir'
    
    if (len(sys.argv)>=2):
        dirName= sys.argv[1]
    
    #unzip(dirName+'.zip', '.')
    
    genScpFiles(dirName)
    htk00_製造各個HtkTool所需的參數檔()
    htk01_處裡語音標籤及詞典()
    htk02_擷取語音特徵及訓練語音模型()
    htk03_語音文字對齊() #----> 'spLab_aligned.mlf'
    
    保存結果(dirName)
    清理垃圾(dirName)

def 保存結果(dirName):
    # moving alignedFile
    cmd= 'cp spLab_aligned.mlf {0}.align'.format(dirName) 
    os_system(cmd)
    
    cmd= 'cp {0}/_all.mp3 {1}.mp3'.format(dirName, dirName)
    os_system(cmd)
    
    cmd= 'cp {0}/_all.txt {1}.txt'.format(dirName, dirName)
    os_system(cmd)    

def 清理垃圾(dirName):
	#remove file named "myHmmPro"
	if os.path.exists("myHmmPro"):
		os.remove("myHmmPro")
	#remove file with extension in rm_extension_list
	rm_extension_list = ['.mlf', '.conf', '.lst', '.scp', '.led', '.dic']  
	for file in os.listdir(os.getcwd()):
		if os.path.splitext(file)[1] in rm_extension_list:
			os.remove(file)
	#remove "hmms_p" folder and it's child
	if os.path.exists("hmms_p"):
		shutil.rmtree('hmms_p')
	#remove *dirName* folder and it's child
	if os.path.exists(dirName):
		shutil.rmtree(dirName)

import zipfile
def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)

if __name__=='__main__':
    主程式()









