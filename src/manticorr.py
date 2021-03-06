#!/u/ki/swmclau2/.conda/envs/hodemulator/bin/python
'''
Main file for this module.
Takes the gadget base as input and an output name.
Calculates the matter correlation function in a gadget output.
Downsamples the particles randomly by a certain fraction.
@Author Sean McLaughlin
'''

#TODO wrap this in a main()
from os import path
from argparse import ArgumentParser
import warnings
from glob import glob
from multiprocessing import cpu_count
import numpy as np
from Corrfunc._countpairs import countpairs_xi
from halotools.mock_observables import return_xyz_formatted_array,tpcf
from readGadgetSnapshot import *#TODO fix relative imports

desc = '''Main file for this module.
Takes the gadget base as input and an output name.
Calculates the matter correlation function in a gadget output.
Downsamples the particles randomly by a certain fraction.'''

parser = ArgumentParser(description=desc)

parser.add_argument('inbase', type=str, help= \
    'Path and file base for the gadget files.')
parser.add_argument('outputfile', type=str, help= \
    'Filename to write the final correlation function.')

#TODO find a good value for p
p0 = 1e-3
parser.add_argument('-p', '--sample_frac', default = p0,type = float, help='Fraction to sample. Default is %f.'%p0)

MAX_CPUS = cpu_count()
parser.add_argument('-n', '--num_cores', default = MAX_CPUS, type = int, help=\
                    'Number of cores to use for the calculation. Default is the max available.')

args = vars(parser.parse_args())

inbase = args['inbase']
outputfile= args['outputfile']
p = args['sample_frac']
num_cores = args['num_cores']

BINFILE = path.join(path.dirname(path.abspath(__file__)), "binfile")#location of files with bin edges
#no clue why I can't just make these here!

assert path.exists(inbase+ '.0'), "%s is not a valid path!"%(inbase+'.0') #check that the path is valid
assert 0 < p < 1 , "%f is not a valid fraction between 0 and 1"%p #p must be a valid fraction!
assert num_cores > 0 #must be an int larger than 0.
if num_cores > MAX_CPUS:
    warnings.warn("Input num_cores %d larger than Max %d; setting to Max."%(num_cores, MAX_CPUS))
    #num_cores = MAX_CPUS

#check we can write to the outputfile
try:
    open(outputfile, 'w')
except IOError:
    raise IOError('Outputfile %s is not writable!'%outputfile)

all_pos = np.array([], dtype = 'float32')

header = readGadgetSnapshot(inbase+'.0')
print header

h = header.HubbleParam 
#TODO should fail gracefully if memory is exceeded or if p is too small.
for file in glob(inbase+'*'):
    #TODO should find out which is "fast" axis and use that.
    #Numpy uses fortran ordering.
    pos = readGadgetSnapshot(file, read_pos=True)[1] #Think this returns some type of tuple; should check
    pos = pos[np.random.rand(pos.shape[0]) < p] #downsample
    if pos.shape[0] == 0:
        continue

    all_pos = np.resize(all_pos, (all_pos.shape[0]+pos.shape[0], 3))
    all_pos[-pos.shape[0]:, :] = pos

all_pos*=h
xi = countpairs_xi(header.BoxSize*h, num_cores, BINFILE, all_pos[:,0], all_pos[:,1], all_pos[:,2])
xi = np.array(xi)#[:, 4] #returns radius info as well, could avoid reading the BINFILE if I wanted.

#TODO Make this append after writing a header!
#out = np.stack((bin_centers, xi)) 
np.savetxt(outputfile, xi, delimiter= ',' )
