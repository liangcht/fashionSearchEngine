import os
import glob
import cv2
import numpy as np
from scipy.fftpack import dct
# from matplotlib import pyplot as plt

def doDCT_natural (filename):
	# Another way: img = Image.open(filename).convert('L')
	img = cv2.imread(filename,0)
	dct_ = dct(dct(img.T, norm='ortho').T, norm='ortho')
	return dct_

def doDFT():
	# read as gray image.
	img = cv2.imread('1.jpg', 0)
	# cv2.imwrite('gray.jpg', img)

	# t1 = dct(dct(img.T, norm='ortho').T, norm='ortho')
	dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
	dft_shift = np.fft.fftshift(dft)

	magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))


	rows, cols = img.shape
	crow,ccol = rows/2 , cols/2

	# create a mask first, center square is 1, remaining all zeros
	mask = np.zeros((rows,cols,2),np.uint8)
	mask[crow-5:crow+5, ccol-5:ccol+5] = 1

	# apply mask and inverse DFT
	fshift = dft_shift*mask
	print fshift[:, :, 0]
	print fshift[:, :, 0].shape
	f_ishift = np.fft.ifftshift(fshift)
	img_back = cv2.idft(f_ishift)
	img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])

	plt.subplot(121),plt.imshow(img, cmap = 'gray')
	plt.title('Input Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(img_back, cmap = 'gray')
	plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
	plt.show()
	return

def zigzagRead(matrix):
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
		

			
	return zig_mat

def doDCT (filename):
	DCTSlot = 30
	img = cv2.imread(filename,0)
	img = cv2.resize(img, (200,200))
	dct_ = dct(dct(img.T, norm='ortho').T, norm='ortho')
	# dct_ = np.matrix([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])

	# read as dct, return as a list
	list_ = zigzagRead(dct_)
	list_ = np.abs(list_)
	# print dct_
	# print list_

	slotLen = len(list_) / DCTSlot + 1
	# print slotLen
	dct_result = np.zeros((DCTSlot,1))

	# get into each slot
	for i in range(len(list_)):
		dct_result[(i+1) / slotLen] += list_[i]

	# normalization
	base = np.linalg.norm(dct_result)
	dct_result /= base
	dct_result = np.transpose(dct_result)

	return dct_result

def store_dct_model (directory=""):
	"Store DCT model."
	nFiles = 28583
	# The number of dimension in DCT of an image.
	val_num = 30

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

def getDist(target, query):
	return np.linalg.norm(query - target)

def DCTDistance(query_path):
	"compute DCT distance."
	query_dct = doDCT(query_path)
	query_array = np.array(query_dct)

	dct_model = np.load("dct_model(no crop).npy")
	dist = np.apply_along_axis(getDist, 1, hist, query_array)

	return dist

# store_dct_model()

