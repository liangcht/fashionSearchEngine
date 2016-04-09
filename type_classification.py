from sqlalchemy import create_engine
import pandas as pd
import scipy.io as sio
import numpy as np
import sys
import os
os.environ['GLOG_minloglevel'] = '3' 
import caffe

######### Initialize caffe model ##########
caffe_root = '/Users/tj474474/Development/caffe/'  
caffe.set_mode_cpu()

model_def = caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
model_weights = caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

# load the mean ImageNet image (as distributed with Caffe) for subtraction
mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

# set the size of the input (we can skip this if we're happy
#  with the default; we can also change it later, e.g., for different batch sizes)
net.blobs['data'].reshape(1,        # batch size
                          3,         # 3-channel (BGR) images
                      227, 227)  # image size is 227x227


def getDist(target, query):
	return np.linalg.norm(query - target)

def getMatrix():
	pass
	####### Get vector of whole database ############
	# Loading Database
	engine = create_engine('sqlite:///amazon/test.db')
	d = pd.read_sql_table('Amazon', engine)

	# sample_d = d[d["type"].isin(["T-Shirt", "Wool Jacket", "Buttom-Down Shirt", "Dress"])]
	# hogs = np.array([sio.loadmat("./hog/hog10.mat")['hog'][0] for id in sample_d["id"]])

	# Get the layer 7 feature of each picture in database
	cnn_ft = np.empty([d.shape[0], 1000])

	for index, path in enumerate(d["path"].values):
		print index
		# download an image
		my_image_url = path  # paste your URL here

		# transform it and copy it into the net
		image = caffe.io.load_image(my_image_url)
		net.blobs['data'].data[...] = transformer.preprocess('data', image)

		# perform classification
		net.forward()

		# obtain the output probabilities
		#output_prob = net.blobs['prob'].data[0]
		cnn_ft[index, ] = net.blobs['prob'].data[0]

		# sort top five predictions from softmax output
		#top_inds = output_prob.argsort()[::-1][:5]

		# load ImageNet labels
		#labels_file = caffe_root + 'data/ilsvrc12/synset_words.txt'
	    
		#labels = np.loadtxt(labels_file, str, delimiter='\t')

		#print 'probabilities and labels:'
		#print zip(output_prob[top_inds], labels[top_inds])

	np.save(open("cnn_prob.npy", 'wb'), cnn_ft)

def getNeighbor(query_path=""):

	###### Test Input Query #######

	image = caffe.io.load_image(query_path)
	net.blobs['data'].data[...] = transformer.preprocess('data', image)

	# perform classification
	net.forward()
	query_ft = net.blobs['prob'].data[0]

	cnn_ft = np.load("cnn_prob.npy")
	dist = np.apply_along_axis(getDist, 1, cnn_ft, query_ft)

	np.save(open("dist.npy", 'wb'), dist)
	return list(dist.argsort()[:10].values)

if __name__ == '__main__':

	print getNeighbor("/Users/tj474474/Development/visual_database/amazon/crawlImages/16449.jpg")
