from sqlalchemy import create_engine
import pandas as pd
import scipy.io as sio
import numpy as np
import sys
import os
os.environ['GLOG_minloglevel'] = '3' 
import caffe
import color_hist_test
import dct_99
import time

######### Initialize caffe model ##########
#caffe_root = '/home/ubuntu/caffe/'
caffe.set_mode_cpu()
#caffe.set_mode_gpu()
#caffe.set_device(0)  # if we have multiple GPUs, pick the first one


#model_def = caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
#model_def = './deploy_VGG.prototxt'
model_def = './deploy_Alex.prototxt'
#model_weights = caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'
#model_def = caffe_root + 'models/bvlc_googlenet/deploy.prototxt'
#model_weights = caffe_root + 'models/bvlc_googlenet/bvlc_googlenet.caffemodel'
#model_weights = "/home/ubuntu/VDB/finetune_flickr_style_iter_7000.caffemodel"#
#model_weights = "../LR001_tune_all_iter_VGG999.caffemodel"
#model_weights = "./finetune_flickr_style_iter_7000.caffemodel"
model_weights = "../ACS_alexNet_iter_10000.caffemodel"

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

# load the mean ImageNet image (as distributed with Caffe) for subtraction
mu = np.load('./ilsvrc_2012_mean.npy')
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

def getDist(target, query):
	return np.linalg.norm(query - target)

'''
def getMatrix():
	pass
	####### Get vector of whole database ############
	# Loading Database
	#engine = create_engine('sqlite:///amazon/test.db')
	engine = create_engine('sqlite:///../amazon/test_large_no_noise.db')
	d = pd.read_sql_table('Amazon', engine)

	# Get the layer 7 feature of each picture in database
	cnn_ft = np.empty([d.shape[0], 30])

	for index, path in enumerate(d["path"].values):
		print index
		# download an image
		my_image_url = "/Users/tj474474/Development/visual_database/amazon/crawlImages_large/"

		# transform it and copy it into the net
		image = caffe.io.load_image(my_image_url + path)
		net.blobs['data'].data[...] = transformer.preprocess('data', image)

		# perform classification
		net.forward()

		# obtain the output probabilities
		cnn_ft[index, ] = net.blobs['prob'].data[0]


	np.save(open("cnn_prob_large_fine.npy", 'wb'), cnn_ft)
'''

def getCNNresult(query_path):
	###### Test Input Query #######
	image = caffe.io.load_image(query_path)
	net.blobs['data'].data[...] = transformer.preprocess('data', image)

	# perform classification
	net.forward()
	query_ft = net.blobs['prob'].data[0]

	#cnn_ft = np.load("crop_cnn_prob_large_fine_VGG999.npy")
	cnn_ft = np.load("crop_cnn_prob_large_fine_Alex_ACS_10000.npy")
	#cnn_ft = np.load("crop_cnn_prob_large_fine.npy")

	#ctg_f = open("category_label.txt")
	ctg_f = open("ACS_label.txt")
	ctg = np.array(ctg_f.readlines())
	dist = np.apply_along_axis(getDist, 1, cnn_ft, query_ft)
	query_rst= np.sort(query_ft)[::-1][:3]

	return (dist, zip(ctg[query_ft.argsort()[::-1][:3]], np.around(query_rst, decimals=2)), cnn_ft)

def getNeighbor_fine(factor = 0.5, win_size = 20, query_path=""):

	###### Test Input Query #######
	image = caffe.io.load_image(query_path)
	net.blobs['data'].data[...] = transformer.preprocess('data', image)

	# perform classification
	net.forward()
	query_ft = net.blobs['prob'].data[0]

	#cnn_ft = np.load("crop_cnn_prob_large_fine_VGG999.npy")
	cnn_ft = np.load("crop_cnn_prob_large_fine_Alex_ACS_10000.npy")

	ctg_f = open("ACS_label.txt")
	ctg = np.array(ctg_f.readlines())
	dist = np.apply_along_axis(getDist, 1, cnn_ft, query_ft)

	winner = list(dist.argsort()[:win_size])

	### Get the result of color histogram computation
	#ch is (distance array, query's top color, all images' color histogram)
	c_h = color_hist_test.colDistance(3, query_path)

	### Get the result of dct transform computation
	dct_dist = dct_99.DCTDistance(query_path)

	# Combine the score and get get top 20's index
	col_dist = c_h[0]
	query_col = c_h[1]
	total_score = factor * dct_dist + (1 - factor) * col_dist

	selected_score_pair = [(total_score[id], id) for id in winner] #zip(total_score, winner)#
	selected_score_pair.sort()
	
	final_winner = [selected_score_pair[i][1] for i in xrange(20)]
	final_winner_scores = [selected_score_pair[i][0] for i in xrange(20)] 
	query_type_result = zip(ctg[query_ft.argsort()[::-1][:3]], np.sort(query_ft)[::-1][:3])
	
	return (final_winner,  query_type_result, query_col, final_winner_scores, 0, cnn_ft[final_winner]) 

if __name__ == '__main__':
	pass
	#getMatrix()
	#print getNeighbor("/Users/tj474474/Development/visual_database/amazon/crawlImages/16449.jpg")
