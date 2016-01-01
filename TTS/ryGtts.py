#!/usr/bin/python3
# coding: utf-8
import os
import glob
import re
import sys
import shutil
import logging
import subprocess

def logging_init():
    '''
    紀錄檔格式初始化
    格式：
         [ 2015 Nov 19 21:13:06 ] ryHalign.py:090 [INFO] : Generate 4 scp files: genScpFiles() Success!
         [ 2015 Nov 19 21:13:07 ] ryHalign.py:030 [DEBUG] : mkdir hmms_p
    '''
    #Log文件輸出格式定義
    logging.basicConfig(level=logging.DEBUG, format='[ %(asctime)s ] %(filename)s:%(lineno)03d [%(levelname)s] : %(message)s', datefmt='%Y %b %d %H:%M:%S', filename='ryHalign.log', filemode='w')

    #Log訊息輸出到螢幕
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(filename)s:%(lineno)03d](%(levelname)s): %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def genScpFiles(dirName):
	'''
	產生 4 個 .scp 檔案：
		spWav.scp, spLab.scp, spMfc.scp, spWav2Mfc.scp
	'''
	if os.path.exists(dirName):
		fnName = '*.wav'
		pathName = os.path.join(dirName, fnName)
		wavL = glob.glob(pathName)
		wavScp = '\n'.join(wavL)

		wavScp= wavScp.replace('\\','/')  # 寫在.scp內的path 分隔用正斜/
		labScp= re.sub('.wav','.lab', wavScp)
		mfcScp= re.sub('.wav','.mfc', wavScp)

		wmScp= ''
		if wavScp!='' and mfcScp!='':
			for w,m in zip(wavScp.split('\n'), mfcScp.split('\n')):
				wmScp += w+'\t'+m+'\n'

		lost_file = []

		if wavScp!='':
			try:
				with open('spWav.scp', 'w') as  f:
					f.write(wavScp)
			except IOError as e:
				logging.error(e)
				lost_file.append("spWav.scp")

		if labScp!='':
			try:
				with open('spLab.scp', 'w') as f:
					f.write(labScp)
			except IOError as e:
					logging.error(e)
					lost_file.append("spLab.scp")

		if wmScp!='':
			try:
				with open('spWav2Mfc.scp', 'w') as f:
					f.write(wmScp)
			except IOError as e:
					logging.error(e)
					lost_file.append("spWav2Mfc.scp")

		if mfcScp!='':
			try:
				with open('spMfc.scp', 'w') as f:
					f.write(mfcScp)
			except IOError as e:
					logging.error(e)
					lost_file.append("spMfc.scp")

		#check size of 4 files all greater than 0
		if len(lost_file) > 0:
			logging.error('Need file: '+', '.join(lost_file))
			logging.error("Missing %d files: genScpFiles() Failed ...", len(lost_file))
			return False
		else:
			logging.info("Generate 4 files: genScpFiles() Success ...")
			return True
	else:
		logging.error('No such directory as ' + dirName + '.')

def 建立Hmm原型(N=1, M=1, D=39, fileName=''):
    '''
    產生myHmmPro檔案
    '''
    hmm原型檔名='myHmmPro'
    if fileName=='':
        fileName=hmm原型檔名

    dotPosition=fileName.find('.')
    if dotPosition>=0:
        fileName=fileName[0:dotPosition]

    logging.info('CreateHProto... ' + fileName + ', N=' + str(N) + ', M=' + str(M))
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

    try:
        with open(fileName, 'w') as f:
            f.write(hProto)
    except IOError as e:
        logging.error(e)
        logging.error('建立Hmm原型() Failed ...')
        return False
    else:
        logging.info('Build ‘myHmmPro‘ file Success ...')
        logging.info('建立Hmm原型() Success ...')
        return True


def htk00_製造各個HtkTool所需的參數檔():
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

    lost_file = []
    try:
        with open('hLed.led','w') as f:
            f.write(hLed_led)
    except IOError as e:
        logging.error(e)
        lost_file.append('hLed.led')

    try:
        with open('hLed00.led','w') as f:
            f.write(hLed00_led)
    except IOError as e:
        logging.error(e)
        lost_file.append('hLed00.led')

    try:
        with open('hCopy.conf','w') as f:
            f.write(hCopy_conf)
    except IOError as e:
        logging.error(e)
        lost_file.append('hCopy.conf')

    try:
        with open('hInit.conf','w') as f:
            f.write(hInit_conf)
    except IOError as e:
        logging.error(e)
        lost_file.append('hInit.conf')

    try:
        with open('hRest.conf','w') as f:
            f.write(hRest_conf)
    except IOError as e:
        logging.error(e)
        lost_file.append('hRest.conf')

    try:
        with open('hErest.conf','w') as f:
            f.write(hErest_conf)
    except IOError as e:
        logging.error(e)
        lost_file.append('hErest.conf')

    try:
        with open('hVite.conf','w') as f:
            f.write(hVite_conf)
    except IOError as e:
        logging.error(e)
        lost_file.append('hVite.conf')

    if len(lost_file) > 0:
        logging.error('Need file: ' + ', '.join(lost_file))
        logging.error("Missing %d files: htk00() Failed ...", len(lost_file))
        return False
    else:
        if 建立Hmm原型(N=3, M=6):
            logging.info("Generate 7 files: htk00() Success ...")
            return True
        else:
            return False

def htk01_處裡語音標籤及詞典():
	if os.path.exists('spLab.scp') and os.path.exists('hLed00.led') and os.path.exists('hLed.led'):
		try:
			cmd = 'HLEd -A -i spLab00.mlf -n spLab00.lst -S spLab.scp  hLed00.led >> HLEd.log'
			subprocess.check_call( [cmd], shell=True )
			logging.debug(cmd)

			cmd = 'HLEd -A -i spLab.mlf -n spLab.lst -S spLab.scp  hLed.led >> HLEd.log'
			subprocess.check_call( [cmd], shell=True )
			logging.debug(cmd)
		except Exception as e:
			logging.error(e)
		else:
			if lst2dic():
				try:
					cmd = 'HLEd -A -i spLab_p.mlf -n spLab_p.lst -S spLab.scp -I spLab.mlf -d spLab_p.dic hLed.led >> HLEd.log'
					subprocess.check_call( [cmd], shell=True )
					logging.debug(cmd)
				except Exception as e:
					logging.error(e)
				else:
					logging.info('htk01() Success ...')
					return True
	else:
		lost_file = []
		for f in ['spLab.scp', 'hLed00.led', 'hLed.led']:
			if not os.path.exists(f):
				lost_file.append(f)
		if len(lost_file) > 0:
			logging.error('Need file: ' + ', '.join(lost_file))
	logging.error('htk01() Failed ...')
	return False

def lst2dic():
	lost_file = []
	try:
		with open('spLab.lst') as f:
			lines = f.readlines()
	except IOError as e:
		logging.error(e)
		logging.error('spLab.lst sort Failed ...')
	else:
		if lines!='':
			lines.sort()  # htk.dic 需要 sort
		try:
			with open('spLab.lst','w') as f:
				for l in lines:
					f.write(l)
		except IOError as e:
			logging.error(e)
			logging.error('spLab.lst sort Failed ...')

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

	try:
		with open('spLab.dic','w') as f:
			f.write(D)
	except IOError as e:
		logging.error(e)
		lost_file.append('spLab.dic')

	try:
		with open('spLab_p.dic','w') as f:
			f.write(Dp)
	except IOError as e:
		logging.error(e)
		lost_file.append('spLab_p.dic')

	if len(lost_file) > 0:
		logging.error('Need file: ' + ', '.join(lost_file))
		logging.error("Missing %d files: lst2dic() Failed ...", len(lost_file))
		logging.error('lst2dic() Failed ...')
		return False
	else:
		logging.info('Generate 3 files: lst2dic() Success ...')
		return True

def htk02_擷取語音特徵及訓練語音模型():
	if os.path.exists('spWav2Mfc.scp'):
		try:
			cmd = 'HCopy -A -C hCopy.conf -S spWav2Mfc.scp >> HCopy.log'
			subprocess.check_call( [cmd], shell=True )
			logging.debug(cmd)
		except Exception as e:
			logging.error(e)

		try:
			with open('spLab_p.lst') as f:
				lines = f.readlines()
		except IOError as e:
			logging.error(e)
		else:
			#if hmms_p folder exists, remove and create again.
			if os.path.exists('hmms_p'):
				try:
					shutil.rmtree('hmms_p')
				except Exception as e:
					logging.error(e)

			try:
				os.mkdir('hmms_p')
			except Exception as e:
				logging.error(e)
			else:
				mList = []
				for l in lines:
					m = l.strip('\n')
					mList.append(m)

				try:
					cmd = 'HCompV -A -C hInit.conf -S spMfc.scp -m -I spLab_p.mlf -M hmms_p -o myHCompV myHmmPro >> HCompV.log'
					subprocess.check_call( [cmd], shell=True )
					logging.debug(cmd)
				except Exception as e:
					logging.error(e)
				else:
					try:
						with open(os.path.join('hmms_p', 'myHCompV')) as f:
							myHCompV = f.read()
					except IOError as e:
						logging.error(e)
					else:
						for m in mList:
							myModel = myHCompV.replace('myHCompV',m)
							try:
								with open( os.path.join('hmms_p', m),'w') as f:
									f.write(myModel)
							except IOError as e:
								logging.error(e)

						repeat_time = 0
						for i in range(5):
							logging.debug('[%d]HERest '%i)
							try:
								cmd = 'HERest -A -C hErest.conf -S spMfc.scp -p 1 -t 2000.0 -w 3 -v 0.05 -I spLab_p.mlf -M hmms_p -d hmms_p spLab_p.lst >> HERest.log'
								subprocess.check_call( [cmd], shell=True )
								logging.debug(cmd)

								cmd = 'HERest -A -C hErest.conf -p 0 -t 2000.0 -w 3 -v 0.05 -I spLab_p.mlf -M hmms_p -d hmms_p spLab_p.lst ' + os.path.join('hmms_p', 'HER1.acc') + ' >> HERest.log'
								subprocess.check_call( [cmd], shell=True )
								logging.debug(cmd)
							except Exception as e:
								logging.error(e)
							else:
								repeat_time += 1
						if repeat_time == 5:
							logging.info('htk02() Success ...')
							return True
	logging.error('htk02() Failed ...')
	return False

def htk03_語音文字對齊():
	try:
		cmd = 'HVite -A -C hVite.conf  -S spMfc.scp  -a -d hmms_p/ -i spLab_aligned.mlf -I spLab.mlf spLab_p.dic spLab_p.lst >> HVite.log'
		subprocess.check_call( [cmd], shell=True )
		logging.debug(cmd)
		logging.debug('generate ‘spLab_aligned.mlf‘')
	except Exception as e:
		logging.error(e)
		logging.error('htk03() Failed ...')
		return False
	else:
		logging.info('htk03() Success ...')
		return True

def 主程式():
	try:
		f_index = sys.argv.index('-d')
	except ValueError as e:
		dirName = 'wavDir'
	else:
		if len(sys.argv) >= f_index+2 and sys.argv[f_index+1][0]!='-':
			dirName = sys.argv[f_index+1]
		else:
			print('ryHalign.py: error: missing filename after ‘-d‘')
			print('Try \'ryHalign.py -d wavDir\'.')
			exit(1)

	logging_init()
	r = genScpFiles(dirName)
	if r:
		r = htk00_製造各個HtkTool所需的參數檔()
	if r:
		r = htk01_處裡語音標籤及詞典()
	if r:
		r = htk02_擷取語音特徵及訓練語音模型()
	if r:
		#----> 'spLab_aligned.mlf'
		r = htk03_語音文字對齊()
	if r:
		保存結果(dirName)

	清理垃圾(dirName)

def 保存結果(dirName):
    save_file = 0
    # moving alignedFile
    try:
        shutil.copy( "spLab_aligned.mlf", dirName+".align" )
    except IOError as e:
        logging.error(e)
    else:
        save_file += 1

    #moving  _all.mp3 file
    try:
        shutil.copy( os.path.join(dirName,"_all.mp3"), dirName+".mp3" )
    except IOError as e:
        logging.error(e)
    else:
        save_file += 1

    #moving _all.txt file
    try:
        shutil.copy( os.path.join(dirName,"_all.txt"), dirName+".txt" )
    except IOError as e:
        logging.error(e)
    else:
        save_file += 1

    if save_file == 3:
        logging.info('保存結果() Success ...')
        return True
    else:
        logging.error('保存結果() Failed ...')
        return False

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
    '''
    try:
        shutil.rmtree(dirName)
    except IOError as e:
        logging.debug(e)
    '''

if __name__=='__main__':
    主程式()
