import os, re, json
import numpy as np

from shogun.Converter	import LocallyLinearEmbedding
from shogun.Features	import RealFeatures

def pgm2numpy(filename):
	fin = None
	try:
		fin = open(filename, 'rb')
		fin.readline()
		match = re.match('^(\d+) (\d+)$', fin.readline().strip())
		cols, rows = match.groups()
		result = np.zeros((int(rows), int(cols)))
		fin.readline()
		for i in xrange(result.shape[0]):
			for j in xrange(result.shape[1]):
				char1 = fin.read(1)
				result[i, j] = ord(char1)
		return (result/255.0, rows,cols)
	finally:
		if fin != None:
			fin.close()
		fin = None
	return None
	
directory = '../visualisations/data/pics/faces_pgms'
files = os.listdir(directory)
images = []
fnames = []
for file in files:
	images.append(pgm2numpy(os.path.join(directory, file))[0])
	fnames.append(file)

N = len(images)
dim = len(images[0].ravel())

feature_matrix = np.zeros([dim, N])

for i, image in enumerate(images):
	feature_matrix[:, i] = image.ravel()

converter = LocallyLinearEmbedding
features = RealFeatures(feature_matrix)

converter_instance = converter()
converter_instance.parallel.set_num_threads(4)
converter_instance.set_k(15)
converter_instance.set_target_dim(2)

print 'Applying Shogun converter'
new_features = converter_instance.embed(features).get_feature_matrix()
print 'Shogun converter applied, saving data...'

X = N*[0.0]
Y = N*[0.0]
for i in xrange(N):
	X[i] = new_features[0,i]
	Y[i] = new_features[1,i]	

out = {}
out['embedded_images'] = [{'fname': fname[:-4]+'.png', 'x': x, 'y': y} for (fname, x, y) in zip(fnames, X, Y)]

json.dump(out, open('../visualisations/data/faces.json', 'w'))
