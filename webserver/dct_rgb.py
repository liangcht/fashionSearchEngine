import os
import glob
import cv2
import numpy as np
from scipy.fftpack import dct

def zigzagRead_half(matrix):
	### Read the upper left matrix.
	rows, cols = matrix.shape
	freqNum = rows * cols
	zig_mat = [matrix[0,0]]

	###
	num_ = min(rows,cols)
	for i in range(1, num_):
		# print "i "+str(i)
		if i%2 == 1:
			for j in range(i+1):
				# print "j "+ str(j)
				zig_mat.append(matrix[j, i-j])
		else:
			for j in range(i, -1, -1):
				# print "j "+ str(j)
				zig_mat.append(matrix[j, i-j])
		

			
	return zig_mat[:2000]

def zigzagRead(matrix):
	### Read the all values in matrix.
	rows, cols = matrix.shape
	freqNum = rows * cols
	zig_mat = [matrix[0,0]]

	###
	num_ = min(rows,cols)
	# print num_-1
	for i in range(1, num_):
		# print "i "+str(i)
		if i%2 == 1:
			for j in range(i+1):
				# print "j "+ str(j)
				zig_mat.append(matrix[j, i-j])
		else:
			for j in range(i, -1, -1):
				# print "j "+ str(j)
				zig_mat.append(matrix[j, i-j])

	for i in range(num_, 2*(num_ - 1)+1):
		# print "i "+str(i)
		if i%2 == 0:
			for j in range(num_-1, i-(num_-1)-1, -1):
				# print "j "+ str(j)
				zig_mat.append(matrix[j, i-j])
		else:
			for j in range(i-(num_-1), num_, 1):
				# print "j "+ str(j)
				zig_mat.append(matrix[j, i-j])
		

			
	return zig_mat

def doDCT (filename):
	DCTSlot = 30
	dct_result = np.zeros((DCTSlot*3,1))
	img = cv2.imread(filename,1)
	img = cv2.resize(img, (200,200))
	for j in range(3):
		# print j
		channel = img[:,:,j]
		imf = np.float32(channel)
		dct_ = dct(dct(imf.T, norm='ortho').T, norm='ortho')

		# read as dct, return as a list
		list_ = zigzagRead_half(dct_)
		list_ = np.abs(list_)
		# print dct_
		# print list_

		# first 10 slots x, next 10 slots 2x, the third 10 slots 4x
		slotLen = len(list_) / 70 + 1
		# slotLen = len(list_) / DCTSlot + 1
		# print slotLen
		channel_result = np.zeros((DCTSlot,1))

		# get into each slot
		for i in range(len(list_)):
			if i+1 < 10*slotLen:
				channel_result[(i+1) / slotLen] += list_[i]
			elif i+1 >=10*slotLen and i+1 < 30 * slotLen:
				channel_result[10 + (i+1-10*slotLen) / (2*slotLen)] += list_[i]
			else:
				channel_result[20 + (i+1-30*slotLen) / (4*slotLen)] += list_[i]

		# normalization
		base = np.linalg.norm(channel_result)
		channel_result /= base
		dct_result[j*DCTSlot:(j+1)*DCTSlot, ] = channel_result
		# print dct_result
	
	dct_result = np.transpose(dct_result)

	return dct_result

def store_dct_model (directory=""):
	"Store DCT model."
	nFiles = 28583
	# The number of dimension in DCT of an image.
	val_num = 90

	files = []
	# directory for read files.
	directory = "/Users/cyan/Desktop/color_hist_py/cropImage_large/"
	for infile in glob.glob(os.path.join(directory,'*.jpg')):
		files.append(infile)
		# print "current file is " + infile

	result_idx = np.empty([nFiles, val_num])
	print "There are " + str(len(files)) +  " images."
	for i in range(len(files)):
		print i
		id1 = files[i].rfind('/')
		id2 = files[i].rfind('.')
		idx = int(files[i][id1+1:id2])
		dct_vec = doDCT(files[i])
		result_idx[idx-1, ] = dct_vec

	# delete all-zeros rows.
	result = result_idx[~(result_idx==0).all(1)]
	print "final size " + str(result.shape[0])
	np.save(open("dct_model.npy", 'wb'), result)
	return


# doDCT('1.jpg')
store_dct_model()