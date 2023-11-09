import time
import sys
sys.path.insert(0, '/private/groups/brookslab/gabai/tools/seqUtils/src/')
import pysam
import numpy as np
import random
from seqUtil import *
from bamUtil import *
from nanoUtil import *


evt = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/eventalign/unique.0.eventalign.tsv'
start_time = time.time()
parseEventAlign(eventAlign = evt, readname = '', 
                outfile = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/eventalign/unique.0.signalAlign.txt')
end_time = time.time()
print(end_time - start_time, flush = True)