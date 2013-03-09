import subprocess,re, numpy
from collections import defaultdict
from time import time
from sklearn import manifold
default_k = 10

def tapkee_time(datafile, method, k=default_k):
	output = subprocess.check_output('DATAFILE=%s METHOD=%s K=%d ./tapkee_run.sh' % (datafile,method,k), shell=True)
	return sum([float(x) for x in re.findall('\d+.\d+',output)])

def waffles_time(datafile, method, k=default_k):
	output = subprocess.check_output('DATAFILE=%s METHOD=%s K=%d ./waffles_run.sh' % (datafile,method,k), shell=True)
	return sum([float(x) for x in re.findall('\d+.\d+',output)])

def mtfdr_time(datafile, method, k=default_k):
	output = subprocess.check_output('DATAFILE=%s METHOD=%s K=%d ./drtoolbox_run.sh' % (datafile,method,k), shell=True)
	return sum([float(x) for x in re.findall('\d+.\d+',output)])

def scikit_time(datafile, method, k=default_k):
	data = numpy.loadtxt(datafile)
	methods = {'lle' : lambda x : manifold.LocallyLinearEmbedding(k,2,method='standard').fit_transform(x),
	           'isomap' : lambda x : manifold.Isomap(k,2).fit_transform(x)}
	t0 = time()
	methods[method](data)
	return time()-t0

def tapkee_performance():
	datasets = [('Swissroll','data/swissroll5000.dat'),('MIT-CBCL','data/cbcl.dat'),('MNIST','data/mnist2000.dat')]
	methods = ['locally_linear_embedding','hessian_locally_linear_embedding',
	           'local_tangent_space_alignment','isomap','landmark_isomap'
	           'multidimensional_scaling','landmark_multidimensional_scaling',
	           'diffusion_map','neighborhood_preserving_embedding',
	           'linear_local_tangent_space_alignment','laplacian_eigenmaps',
	           'locality_preserving_projections','pca','kernel_pca','factor_analysis',
	           'random_projection','stochastic_proximity_embedding']
	print 'Tapkee implementations benchmark'
	for method in methods:
		for dataset_name,dataset_file in datasets:
			print '%s on %s takes %.4fs' % (method.replace('_',' ').title(), dataset_name, tapkee_time(dataset_file, method))

def jmlr_paper_table():
	k = 10
	n_updates = 5
	time_limit = 60.0

	datasets = [('Swissroll','data/swissroll5000.dat'),('MIT-CBCL','data/cbcl.dat'),('MNIST','data/mnist2000.dat')]
	libraries = [('Tapkee',tapkee_time), ('Scikit-learn',scikit_time), ('Waffles',waffles_time), ('MTfDR',mtfdr_time)]
	methods = ['lle','isomap']
	walltimes = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : 0.0)))
	for dataset_name,dataset_file in datasets:
		for library_name, library_timer in libraries:
			for method in methods:
				print 'Measuring %s method implementation in %s on %s dataset' % (method,library_name,dataset_name)
				count = 1
				walltime = library_timer(dataset_file,method,k)
				if walltime < time_limit:
					for _ in xrange(n_updates-1):
						walltime += library_timer(dataset_file,method,k)
						count += 1
				else:
					print 'Skipping repetitions as time exceeds limit'
				walltime /= count
				walltimes[dataset_name][library_name][method] = walltime

	endline = '\\\\hline\n'
	libraries_header = "".join(['& \\multicolumn{2}{c}{\\textit{%s}} ' % (library_name) for (library_name,_) in libraries]) + endline
	methods_header_element = "".join(['& \\textsc{%s} ' % (method_name) for method_name in methods])
	methods_header = "".join([methods_header_element for _ in libraries]) + endline
	
	walltimes_table = ""
	for dataset_name,_ in datasets:
		dataset_line = '\\textit{%s} ' % dataset_name
		for library_name,_ in libraries:
			implementation_element = "".join(['& %.2f ' % walltimes[dataset_name][library_name][method_name] for method_name in methods])
			dataset_line += implementation_element
		dataset_line += endline
		walltimes_table += dataset_line
	return libraries_header + methods_header + walltimes_table

#tapkee_performance()
#print jmlr_paper_table()
