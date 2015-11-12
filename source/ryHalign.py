#!/usr/bin/python3
# coding: utf-8
import os
import glob
import re
import shutil
import logging
import subprocess

def logging_init():
	#Log文件輸出格式定義
	logging.basicConfig(level=logging.DEBUG, format='[ %(asctime)s ] %(filename)s:%(lineno)03d [%(levelname)s] : %(message)s', datefmt='%Y %b %d %H:%M:%S', filename='ryHalign.log', filemode='w')
	
	#Log訊息輸出到螢幕
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('[ %(asctime)s ] %(filename)s:%(lineno)03d [%(levelname)s] : %(message)s')
	console.setFormatter(formatter)
	logging.getLogger('').addHandler(console)

globalCmdNum = 0	
def os_system(cmd):
    global globalCmdNum
    
    #真正執行命令在此！
    status= os.system(cmd)
    logging.debug(cmd)
    #os.system('echo "(globalCmdNum, status, cmd)= %03d, %d,----> %s"'%(globalCmdNum, status, cmd))

    #後端繼續蒐集 error 或 warning 訊息
    #print( '(globalCmdNum, status, cmd)= %03d, %d,----> %s '%(globalCmdNum, status, cmd))
    #globalCmdNum +=1
    
    return status

def genScpFiles(dirName):
	#產生 4 個 .scp ----> spWav.scp, spLab.scp, spMfc.scp, spWav2Mfc.scp
	fnName= '*.wav'
	pathName= os.path.join(dirName, fnName)
	wavL= glob.glob(pathName)
	wavScp= '\n'.join(wavL)
	
	wavScp= wavScp.replace('\\','/')  # 寫在.scp內的path 分隔用正斜/
	labScp= re.sub('.wav','.lab', wavScp)
	mfcScp= re.sub('.wav','.mfc', wavScp)
	
	wmScp= ''
	if wavScp!='' and mfcScp!='':
		for w,m in zip(wavScp.split('\n'), mfcScp.split('\n')):
			wmScp += w+'\t'+m+'\n'
	
	completed_file = 0
	
	if wavScp!='':
		try:
			with open('spWav.scp', 'w') as  f:
				f.write(wavScp)
		except IOError as e:
			logging.error(e)
		else:
			completed_file += 1

	if labScp!='':
		try:
			with open('spLab.scp', 'w') as f:
				f.write(labScp)
		except IOError as e:
				logging.error(e)
		else:
			completed_file += 1
	
	if wmScp!='':
		try:
			with open('spWav2Mfc.scp', 'w') as f:
				f.write(wmScp)
		except IOError as e:
				logging.error(e)
		else:
			completed_file += 1
	
	if mfcScp!='':
		try:
			with open('spMfc.scp', 'w') as f:
				f.write(mfcScp)
		except IOError as e:
				logging.error(e)
		else:
			completed_file += 1
	
	#check size of 4 files all greater than 0 
	if completed_file == 4:
		logging.info("Generate 4 scp files: genScpFiles() Success!")
		return True
	else:
		logging.error("Generate %d scp files: genScpFiles() Failed!", completed_file)
		return False

def 建立Hmm原型(N=1, M=1, D=39, fileName=''):
	#myHmmPro (沒延伸檔名的) hmm 原型 檔
	
	#global hmm原型檔名
	hmm原型檔名='myHmmPro' 
	if fileName=='':
		fileName=hmm原型檔名
		
	dotPosition=fileName.find('.')
	if dotPosition>=0: 
		fileName=fileName[0:dotPosition]
	
	logging.info('\n\nCreateHProto....\n',fileName,'\nN = ',N,',M = ',M,'\n\n')
	hProto= '~h ' + '"' + fileName + '"' + '\n' + '~o <VecSize> ' + str(D) + '\n<MFCC_0_D_A> <StreamInfo> 1 ' + str(D) + '\n\n<BeginHMM>\n'
	
	hProto += '<NumStates> ' + str(N+2) + '\n'
	
	for state in range(2,N+2): # 2...(N+1)
		hProto += '\n'
		hProto += ' <State> ' + str(state) + '  <NumMixes> ' + str(M) + ' <Stream> 1 \n'
		
		for mixture in range(1, M+1): # 1...M
			hProto += '  <Mixture> '+str(mixture) + ' ' +str(1.0/M) +'\n'
			hProto += '   <Mean> '+str(D) +'\n'
			hProto += '    '
			for i in range(D):
				hProto += str(0)+' '
			hProto += '\n'
			hProto += '   <Variance> ' + str(D) + '\n'
			hProto += '    '
			for i in range(D):
				hProto += str(1) + ' '
			hProto += '\n'
			
	hProto += '\n<TransP> ' + str(N+2) + '\n'

	for i in range(0,1):
		hProto += ' '
		for j in range(0,N+2):
			if j==1: 
				aij=1.0
			else: 
				aij=0.0
			hProto += str(aij) + ' '
		hProto += '\n'
	for i in range(1,N+1):
		hProto += ' '
		for j in range(0,N+2):
			if j==i:
				aij=0.6
			elif j==(i+1):
				aij=0.4
			else:
				aij=0.0
			hProto += str(aij)+' '
		hProto += '\n'
	for i in range(N+1,N+2):
		hProto += ' '
		for j in range(0,N+2):
			aij=0.0
			hProto += str(aij) + ' '
		hProto += '\n'
		
	hProto += '\n<EndHMM>\n'

	#fileName= 'hProto.hmm' 檔名似乎得和 ~h "..." 中一致，否則會出錯, .hmm 沒關係
	try:
		with open(fileName, 'w') as f:
			f.write(hProto)
	except IOError as e:
		logging.error(e)
		return False
	else:
		logging.info('Build \'myHmmPro\' file success')
		return True


def htk00_製造各個HtkTool所需的參數檔():
	# also need create file list, *.scp
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
	
	try:
		with open('hLed.led','w') as f:
			f.write(hLed_led)
	except IOError as e:
		logging.error(e)
	
	try:
		with open('hLed00.led','w') as f:
			f.write(hLed00_led)
	except IOError as e:
		logging.error(e)
		
	try:
		with open('hCopy.conf','w') as f:
			f.write(hCopy_conf)
	except IOError as e:
		logging.error(e)
	
	try:
		with open('hInit.conf','w') as f:
			f.write(hInit_conf)
	except IOError as e:
		logging.error(e)
	
	try:
		with open('hRest.conf','w') as f:
			f.write(hRest_conf)
	except IOError as e:
		logging.error(e)
		
	try:		
		with open('hErest.conf','w') as f:
			f.write(hErest_conf)
	except IOError as e:
		logging.error(e)
		
	try:		
		with open('hVite.conf','w') as f:
			f.write(hVite_conf)
	except IOError as e:
		logging.error(e)
	
	if 建立Hmm原型(N=3, M=6):
		logging.info('htk00() success')
		return True
	else:
		logging.error('建立Hmm原型() failed')
		return False

def htk01_處裡語音標籤及詞典():
	if os.path.exists('spLab.scp') and os.path.exists('hLed00.led') and os.path.exists('hLed.led'):
		try:
			subprocess.check_call( ['HLEd -A -i spLab00.mlf -n spLab00.lst -S spLab.scp  hLed00.led'], shell=True )
			subprocess.check_call( ['HLEd -A -i spLab.mlf -n spLab.lst -S spLab.scp  hLed.led'], shell=True )
		except Exception as e:
			logging.error(e)
		else:
			if lst2dic():
				logging.info('lst2dic() success')
				try:
					subprocess.check_call( ['HLEd -A -i spLab_p.mlf -n spLab_p.lst -S spLab.scp -I spLab.mlf -d spLab_p.dic hLed.led'], shell=True )
				except Exception as e:
					logging.error(e)
				else:
					logging.info('htk01() success')
			else:
				logging.error('lst2dic() failed')
	else:
		lost_file = []
		if not os.path.exists('spLab.scp'):
			lost_file.append('spLab.scp')
		if not os.path.exists('hLed00.led'):
			lost_file.append('hLed00.led')
		if not os.path.exists('hLed.led'):
			lost_file.append('hLed.led')
			
		logging.error('need file: '+','.join(lost_file))

def lst2dic():
	try:
		f = open('spLab.lst')
		lines = f.readlines()
		f.close()
	except IOError as e:
		logging.error(e)
	
	if lines!='':	
		lines.sort()  # htk.dic 需要 sort
	
	try:
		f = open('spLab.lst','w')
	except IOError as e:
		logging.error(e)
	else:
		for l in lines:
			f.write(l)
		f.close()

	D = ''
	Dp = ''
	for l in lines:
		d=l.rstrip('\n')
		D += d + ' ' + d + '\n'
		
		if d=='sil' or len(d)<2:
			ps = d
		else:
			ps = ''
			for n in range(len(d)-1):
				ps += d[n] + d[n+1] + ' '
		
		Dp += d + ' ' + ps + '\n'

	f= open('spLab.dic','w')#,encoding='utf8')
	f.write(D)
	f.close()

	f= open('spLab_p.dic','w')#,encoding='utf8')
	f.write(Dp)
	f.close()
	return True

def htk02_擷取語音特徵及訓練語音模型():
	os_system('HCopy -A -C hCopy.conf -S spWav2Mfc.scp')
	os_system('mkdir hmms_p')
	
	f= open('spLab_p.lst')
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
    
    logging_init()
    genScpFiles(dirName)
    htk00_製造各個HtkTool所需的參數檔()
    htk01_處裡語音標籤及詞典()
    
    htk02_擷取語音特徵及訓練語音模型()
    htk03_語音文字對齊() #----> 'spLab_aligned.mlf'
    
    保存結果(dirName)
    清理垃圾(dirName)

def 保存結果(dirName):
	# moving alignedFile
	try:
		shutil.copy( "spLab_aligned.mlf", dirName+".align" )
	except IOError as e:
		logging.error(e)
	
	#moving  _all.mp3 file	
	try:
		shutil.copy( os.path.join(dirName,"_all.mp3"), dirName+".mp3" )
	except IOError as e:
		logging.error(e)

	#moving _all.txt file	
	try:
		shutil.copy( os.path.join(dirName,"_all.txt"), dirName+".txt" )
	except IOError as e:
		logging.error(e)

def 清理垃圾(dirName):
	#remove "myHmmPro" file
	try:
		os.remove("myHmmPro")
	except IOError as e:
		logging.debug(e)
		
	#remove file with extension in rm_extension_list
	rm_extension_list = ['.mlf', '.conf', '.lst', '.scp', '.led', '.dic']  
	for file in os.listdir(os.getcwd()):
		if os.path.splitext(file)[1] in rm_extension_list:
			try:
				os.remove(file)
			except IOError as e:
				logging.debug(e)
			
	#remove "hmms_p" folder and it's child
	try:
		shutil.rmtree('hmms_p')
	except IOError as e:
		logging.debug(e)
	
	#remove "dirName" folder and it's child
	try:
		shutil.rmtree(dirName)
	except IOError as e:
		logging.debug(e)

if __name__=='__main__':
    主程式()
