import sys
import numpy as np
sys.path.insert(0, '/private/groups/brookslab/gabai/tools/seqUtils/src/')
from seqUtil import *
from nanoUtil import *
from bamUtil import *

bam = '/private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/chrom.sorted.bam'
genome = '/private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa'
chrII_evt = '/data/scratch/gabai/addseq_data/eventalign/chrII.eventalign.txt'

chrII_sig= '/data/scratch/gabai/addseq_data/eventalign/chrII.sig.tsv'

chrII_alignment, chrom, qStart, qEnd = getAlignedReads(bam, region = 'chrII', genome = genome)
parseEventAlign(eventAlign = chrII_evt, alignment = chrII_alignment, outfile =chrII_sig)