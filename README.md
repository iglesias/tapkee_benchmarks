This repository includes [a script](benchmark.py) that can be used to 
benchmark various implementations of dimension reduction algorithms. Currently the
script supports three modes:

- *jmlr*. Reproduce comparison table from the JMLR MLOSS submission of paper on Tapkee.
- *all*. Run all Tapkee algorithms on all included datasets and output walltime.
- *scaling*. Measure speedups caused by increasing number of used threads.

To run the script with some mode use `python benchmark.py [mode]` where mode is any of the modes listed above.

This repository also includes methods availability table that can be found [here](available_methods.md).

Included libraries:

- *Tapkee*. This repository includes binary of application from the Tapkee library v0.1. Requires no installation.

- *Scikit-learn*. This repository includes Scikit-learn v.0.13.1 with no patches applied. To install Scikit-learn
cd to scikit-learn/sklearn and run `python setup.py build` and 'sudo python setup.py install' commands.

- *Waffles*. This repository includes version 2012-08-31 of Waffles library with small patch to support
time measuring. To build Waffles cd to waffles/src and run 'sudo make install' command. After that, binaries will 
be located in the waffles/bin/ folder.

- *Matlab Toolbox for Dimensionality Reduction (MTfDR)*. This repository includes MTfDR v.08 April 2012 without
any changes. MTfDR requires no installation.

License
=======

Included libraries are distributed under their own licenses without any changes from our side. All other included files
are free and you may use, modify and redistribute it for any purposes without limitations and permissions.
