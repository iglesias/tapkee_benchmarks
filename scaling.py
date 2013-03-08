import subprocess, re, multiprocessing

omp_threads = 'OMP_NUM_THREADS'
tapkee_elf = '/tapkee/tapkee'
datafile = 'data/cbcl.dat'
options = '--benchmark'

n_tries = 5

for n_threads in [i for i in xrange(1,1+2*multiprocessing.cpu_count())]:
	walltime = 0.0
	for _ in xrange(n_tries):
		walltime += float(subprocess.check_output("%s=%d .%s -i %s -o output.dat %s" % 
	                                              (omp_threads, n_threads, 
	                                               tapkee_elf, datafile, options),
	                                              shell=True).split()[-2])
	walltime /= n_tries
	print n_threads, walltime
