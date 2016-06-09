'''
Helper module to write a bin file for corrfunc.
@Author Sean McLaughlin
'''

from argparse import ArgumentParser
import numpy as np

desc = '''Helper module to write a bin file for corrfunc.
 Only supports logarithmic binning.'''

parser = ArgumentParser(description=desc)

parser.add_argument('rmin', type=float, help= \
    'Lower edge of the lowest bin. ')
parser.add_argument('rmax', type=float, help= \
    'Highest edge of the highest bin.')
parser.add_argument('nbins', type = int, help =\
    'Number of bins.')

args = vars(parser.parse_args())
rmin, rmax = args['rmin'], args['rmax']
nbins = args['nbins']

assert rmin < rmax
assert nbins > 0

bins = np.logspace(rmin, rmax, nbins)

with open('./binfile') as f:
    for low, high in zip(bins[:-1], bins[1:]):
        f.write('\t%f\t%f'%(low,high))

