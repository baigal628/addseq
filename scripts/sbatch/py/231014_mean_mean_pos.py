from doctest import OutputChecker
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
pos_sigAlign = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/modPredict/231014_PHO5_pos_meanScore_medianPos_chrII:429000-435000siganlAlign.tsv'

modPredict(bam = pos_bam, event = pos_evt, region = 'PHO5', 
           genome = genome, method = 'mean',sigAlign = pos_sigAlign,
           prefix = '231014_PHO5_pos_meanScore_meanPos',
           outPath='/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/modPredict/')