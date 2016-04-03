from sqlalchemy import create_engine
import pandas as pd
import scipy.io as sio
import numpy as np

if __name__ == '__main__':

	engine = create_engine('sqlite:///amazon/test.db')
	d = pd.read_sql_table('Amazon', engine)

	h_form = sio.loadmat('hog1.mat')['hog']
	hogs = np.empty([0, h_form.shape[1]])

	for id in d["id"]:
		hog = sio.loadmat("hog1.mat")['hog']
		print id
		hogs = np.append(hogs, hog, axis = 0)
		print id, "nn"
		#hogs = np.array(hogs)

	#hogs = np.array([sio.loadmat("hog1.mat")['hog'] for id in d["id"]])
	#data = np.array(data)

