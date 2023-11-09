import sys
sys.path.insert(0, '/private/groups/brookslab/gabai/tools/seqUtils/src/')
import time
import numpy as np
from seqUtil import *
from bamUtil import *
from nanoUtil import *
from nntUtil import *
from modPredict import *
import matplotlib.pyplot as plt
import seaborn as sns

genome = '/private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa'
chrom_bam = '/private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/all_read.bam'
pos_bam = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.500.pass.sorted.bam'
neg_bam = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.0.pass.sorted.bam'
chrom_evt = '/private/groups/brookslab/gabai/projects/Add-seq/data/chrom/eventalign/all_read.eventalign.txt'
pos_evt = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/eventalign/unique.500.eventalign.tsv'
neg_evt = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/eventalign/unique.0.eventalign.tsv'
neg_sigAlign = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/eventalign/231012_PHO5_neg_chrII:429000-435000siganlAlign.tsv'


modPredict(bam = neg_bam, event = neg_evt, region = 'PHO5', 
           genome = genome, sigAlign = neg_sigAlign, method = 'mean',
           prefix = '231012_PHO5_neg_meanScore_meanPos')