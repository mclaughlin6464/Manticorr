'''
Main file for this module.
Takes the gadget base as input and an output name.
Calculates the matter correlation function in a gadget output.
Downsamples the particles randomly by a certain fraction.
@Author Sean McLaughlin
'''

#TODO wrap this in a main()
import os
from argparse import ArgumentParser
import warnings
from glob import glob
from multiprocessing import cpu_count
import numpy as np
from Corrfunc._countpairs import countpairs_xi
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

BIN_FILE = './binfile'#location of files with bin edges
#no clue why I can't just make these there!

assert os.path.exists(inbase+ '.0'), "%s is not a valid path!"%(inbase+'.0') #check that the path is valid
assert 0 < p < 1 , "%f is not a valid fraction between 0 and 1"%p #p must be a valid fraction!
assert num_cores > 0 #must be an int larger than 0.
if num_cores > MAX_CPUS:
    warnings.warn("Input num_cores %d larger than Max %d; setting to Max."%(num_cores, MAX_CPUS))
    num_cores = MAX_CPUS

#check we can write to the outputfile
try:
    open(outputfile, 'w')
except OSError:
    raise IOError('Outputfile %s is not writable!'%outputfile)

all_pos = np.array([])

header = readGadgetSnapshot(inbase+'.0')

#TODO pos may need some h's!
for file in glob(inbase+'*'):
    #TODO should find out which is "fast" axis and use that.
    #Numpy uses fortran ordering.
    pos = readGadgetSnapshot(file, read_pos=True)[1] #Think this returns some type of tuple; should check
    pos = pos[np.random.rand(pos.shape[0]) < p] #downsample
    all_pos = np.resize(all_pos, (all_pos.shape[0]+pos.shape[0], 3))
    all_pos[-pos.shape[0]:, :] = pos

xi = countpairs_xi(header.BoxSize, num_cores, binfile, pos[:,0], pos[:,1], pos[:,2])