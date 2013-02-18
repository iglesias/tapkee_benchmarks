addpath 'drtoolbox/techniques'

disp '====LLE===='
disp 'Swissroll 5000'
X = load('data/swissroll5000.dat');
[mappedX, ~] = lle(X, 2, 20, 'Matlab', 1);
disp 'Swissroll 10000'
X = load('data/swissroll10000.dat');
[mappedX, ~] = lle(X, 2, 20, 'Matlab', 1);
disp 'MNIST 2000'
X = load('data/mnist2000.dat');
[mappedX, ~] = lle(X, 2, 20, 'Matlab', 1);
disp 'MNIST 4000'
X = load('data/mnist4000.dat');
[mappedX, ~] = lle(X, 2, 20, 'Matlab', 1);
disp 'MIT_CBCL'
X = load('data/cbcl.dat');
[mappedX, ~] = lle(X, 2, 20, 'Matlab', 1);
