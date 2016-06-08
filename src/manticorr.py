'''
Main file for this module.
Takes the gadget base as input and an output name.
Calculates the matter correlation function in a gadget output.
Downsamples the particles randomly by a certain fraction.
'''

#TODO wrap this in a main()
import os
from argparse import ArgumentParser
from glob import glob
import numpy as np
#import Corrfunc
from readGadgetSnapshot import *#TODO fix relative imports

desc = '''Main file for this module.
Takes the gadget base as input and an output name.
Calculates the matter correlation function in a gadget output.
Downsamples the particles randomly by a certain fraction.'''

parser = ArgumentParser(description=desc)

parser.add_argument('inbase', type=str, help= \
    'Path and file base for the gadget files.')
# May want to rename to tmp
parser.add_argument('outputfile', type=str, help= \
    'Filename to write the final correlation function.')

#TODO find a good value for p
p0 = 1e-3
parser.add_argument('-p', '--sample_frac', default = p0,type = float, help='Fraction to sample. Default is %f.'%p0)

args = vars(parser.parse_args())

inbase = args['inbase']
outputfile= args['outputfile']
p = args['sample_frac']

assert os.path.exists(inbase+ '.0'), "%s is not a valid path!"%(inbase+'.0') #check that the path is valid
assert 0 < p < 1 , "%f is not a valid fraction between 0 and 1"%p #p must be a valid fraction!

#check we can write to the outputfile
try:
    open(outputfile, 'w')
except OSError:
    raise IOError('Outputfile %s is not writable!'%outputfile)

all_pos = np.array([])

for file in glob(inbase+'*'):
    pos = readGadgetSnapshot(file, read_pos=True)[1] #Think this returns some type of tuple; should check
    pos = pos[np.random.rand(pos.shape[0]) < p] #downsample
    all_pos = np.resize(all_pos, (all_pos.shape[0]+pos.shape[0], 3))
    all_pos[-pos.shape[0]:, :] = pos
    break

print all_pos

#all pos have been collected. now run corrFunc.