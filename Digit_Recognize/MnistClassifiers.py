#!/usr/bin/python3
import random
import numpy as np
import pylab as pl
import os
from sklearn import datasets,  metrics, linear_model, svm, mixture
from sklearn.externals import joblib


# The following 3 is especially important, so I make them global.
mnist  = None
data   = None
target = None

def get_data(downsample=10,plshow=False):
	global data, target, mnist

	print("get_data ...")

	# Get the MNist Database from Internet or local disk
	# This is very powerful for me (the author renyuan)
	custom_data_home = '.' # the current directory
	mnist = datasets.fetch_mldata('MNIST original', data_home= custom_data_home)

	# Downsample mnist as the training set
	# I know that there are 70000 pictures in MNist database
	# I wish sample a small fraction of the pictures
	data =   mnist.data[0:60000:downsample]
	target = mnist.target[0:60000:downsample]

	if plshow:
		n_sample = len(data)
		data_image = data.reshape(n_sample,28,28)
		image_and_target = list(zip(data_image, target))

		pl.figure()
		for i, (im, tg) in enumerate(image_and_target):
			if i>=100: break
			pl.subplot(10, 10, i+ 1)
			pl.axis('off')
			pl.imshow(im, cmap=pl.cm.gray_r)
			pl.title('tg=%d'%tg, color='blue')

		pl.show()

	return data, target

def train():
	print("training ...")

	global classifier

	classifier = svm.SVC(kernel='poly', tol=0.000000000001)
	classifier.fit(data, target)

	# save job to svm-model/svm.pkl
	if not os.path.exists('svm-model'):
		os.makedirs('svm-model')
	joblib.dump(classifier, os.path.join('svm-model','svm.pkl'))

	return classifier

def test(d,t, plshow=False, cfshow=False):
	'''
	providing the data, and the target for checking correctness
	using the global classifier to do the classification
	'''

	print("testing ...")

	n_sample = len(d)
	data_image = d.reshape(n_sample,28,28)
	print("sample=%s" % n_sample)

	# do recognition
	global classifier
	p = classifier.predict(d)

	report = metrics.classification_report(t, p)
	print("\n=== Report for classifier %s:\n%s\n"%(classifier, report))

	# show the confusion matrix
	cfmatrix=[]
	if cfshow:
		cfmatrix= metrics.confusion_matrix(t, p)
		print("\n=== Confusion matrix:\n%s" % cfmatrix)

	# visualize the results as image
	if plshow:
		# randomly choosing 100 pictures to show
		randomImg= list(zip(data_image, t, p))
		random.shuffle(randomImg)

		pl.figure()
		for i, (im, tg, pr) in enumerate(randomImg):
			if i>=100: break
			pl.subplot(10, 10, i + 1)
			pl.axis('off')
			pl.imshow(im, cmap=pl.cm.gray_r)
			if tg==pr:
				c= 'blue'
			else:
				c= 'red'
			pl.title('pr=%d'%pr, color=c)

		pl.show()

def test_outside(downsample=10):
	d= mnist.data[60000:70000:downsample]
	t= mnist.target[60000:70000:downsample]
	test(d,t)

def main():
	get_data()

	global classifier
	if os.path.isfile(os.path.join('svm-model','svm.pkl.')):
		classifier = joblib.load(os.path.join('svm-model','svm.pkl'))
	else:
		train()
	test_outside(10)

if __name__=='__main__':
	main() # this is the main procedure of this program
