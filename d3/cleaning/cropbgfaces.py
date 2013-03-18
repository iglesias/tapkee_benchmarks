import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import misc

idirname = '../visualisations/data/pics/faces'
odirname = '../visualisations/data/pics/faces_transparent'
files = os.listdir(idirname)

filterpx = xrange(25, 31)

for fidx, file in enumerate(files):
	img = mpimg.imread(os.path.join(idirname, file))
	Z = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.uint8)
	Z[:,:,0] = img
	Z[:,:,1] = Z[:,:,0]
	Z[:,:,2] = Z[:,:,0]
	for i in xrange(img.shape[0]):
		for j in xrange(img.shape[1]):
			if img[i,j] in filterpx:
				Z[i,j,3] = 0
			else:
				Z[i,j,3] = 255 

	pngfile = file[:-3] + 'png'
	misc.imsave(os.path.join(odirname, pngfile), Z)
	print pngfile, 'saved (' + str(fidx+1) + ' out of ' + str(len(files)) + ' completed).' 
