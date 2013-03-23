from numpy import *

filename = 'swissroll10000.dat'
X = loadtxt(filename)
savetxt(filename,X.T,fmt='%.2f')
