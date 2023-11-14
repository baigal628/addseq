import sys
import numpy as np
sys.path.insert(0, '/private/groups/brookslab/gabai/tools/seqUtils/src/')
from seqUtil import *
from nanoUtil import *
from bamUtil import *

bam = '/private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/chrom.sorted.bam'
genome = '/private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa'
chrVI_evt = '/data/scratch/gabai/addseq_data/eventalign/chrVI.eventalign.txt'

chrVI_sig= '/data/scratch/gabai/addseq_data/eventalign/chrVI.sig.tsv'

chrVI_alignment, chrom, qStart, qEnd = getAlignedReads(bam, region = 'chrVI', genome = genome)
parseEventAlign(eventAlign = chrVI_evt, alignment = chrVI_alignment, outfile =chrVI_sig)