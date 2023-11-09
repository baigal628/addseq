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
chrom_evt = '/private/groups/brookslab/gabai/projects/Add-seq/data/chrom/eventalign/all_read.eventalign.txt'
chrom_sigAlign = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/eventalign/231012_PHO5_chrom_chrII:429000-435000siganlAlign.tsv'

modPredict(bam = chrom_bam, event = chrom_evt, region = 'PHO5', genome = genome,
           prefix = '231014_PHO5_chrom_meanScore_medianPos', n_rname=0, 
           outPath='/private/groups/brookslab/gabai/projects/Add-seq/data/chrom/modPredict/')