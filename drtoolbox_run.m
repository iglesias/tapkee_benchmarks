1;

addpath 'drtoolbox/techniques'
datafile = getenv('DATAFILE')
method_name = getenv('METHOD')
k = str2num(getenv('K'))

X = load(datafile);
X = X';

if strcmp(method_name,'lle')
	tic;
	lle(X,2,k);
	toc
end
if strcmp(method_name,'isomap')
	tic;
	isomap(X,2,k);
	toc
end
