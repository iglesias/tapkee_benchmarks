from time import time
import numpy
from sklearn import manifold

swissroll5000 = ('Swissroll 5000',numpy.loadtxt('data/swissroll5000.dat'))
swissroll10000 = ('Swissroll 10000',numpy.loadtxt('data/swissroll5000.dat'))
mnist2000 = ('MNIST 2000',numpy.loadtxt('data/mnist2000.dat'))
mnist4000 = ('MNIST 4000',numpy.loadtxt('data/mnist4000.dat'))
cbcl = ('MIT-CBCL',numpy.loadtxt('data/cbcl.dat'))

for (dataset_name,dataset) in (swissroll5000,swissroll10000,mnist2000,mnist4000,cbcl):
	t0 = time()
	print dataset.shape
	manifold.LocallyLinearEmbedding(20,2,method='standard').fit_transform(dataset)
	print dataset_name, '%f.4 s' % (time() - t0)
