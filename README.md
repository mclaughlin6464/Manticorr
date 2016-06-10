# Manticorr

#### Description
---
Manticorr is a simple module to calculate the matter correlation function from Gadget outputs. In general, the raw particle data from an N-body simulation is very large. So large in fact that even if a speedy correlation function calculator is available, calculating a matter correlation function from all points is non-trivial. A imple workaround is to sample particles at random from the simulation and calculate the correlation function. Downsampling in this way, though a bit of a hack, allows the entire calculation to easily fit into memory and be done realtively quickly. 

Manticorr loads a gadget snapshot, downsamples it, and calculates a correlation function via [Corrfunc](https://github.com/manodeep/Corrfunc). 

####Dependencies
----
Manticorr has minimal dependencies. It requires numpy (which you probably have) and CorrFunc (which you probably don't). Corrfunc is vailable [here](https://github.com/manodeep/Corrfunc). 

####Using Manticorr
---
Manticorr is run via the following command line call:

`python manticorr.py [-h] [-p SAMPLE_FRAC] [-n NUM_CORES] inbase outputfile`

The parameters are defined via:
* `inbase`: The path and base file name for the gadget files. Manticorr reads all files that satisfy `inbase + '.*'`. 
* `outputfile`: The file to save the calculated correlation function to. 
* `SAMPLE_FRAC`: Optional. Fraction of particles to retain for calculation. Too large of a value will possible exceed memory, and too small will result in too few or 0 particles being sampled! 
* `NUM_CORES`: Optional. Number of cores to use for the correlation function calculation. Default is the number given by Python's `multiprocessing.num_cores` function. 

Corrfunc requires as an input `binfile`, a file which contains the lower and upper edges of each bin. Manticorr includes the arbitray default written from `np.logspace(-1, 1.7, 20)`. To change it, simply run makeBins via:

`python makeBins.py [-h] rmin rmax nbins`

Which plugs those values into their appropriate place in `np.logspace` and writes them to `binfile`. 

