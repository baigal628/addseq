import sys
sys.path.insert(0, '/private/groups/brookslab/gabai/tools/seqUtils/src/')
import time
import numpy as np
from seqUtil import *
from bamUtil import *
from nanoUtil import *
from nntUtil import *
from modPredict import *
from plotUtil import *
import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
from collections import defaultdict 

nuc_regions = {
    'PHO5': 'chrII:429000-435000',
    'CLN2': 'chrXVI:66000-67550',
    'HMR': 'chrIII:290000-299000',
    'AUA1': 'chrVI:114000-116000',
    'EMW1': 'chrXIV:45000-50000',
    'NRG2': 'chrII:370000-379000',
    'RDN37': 'chrXII:450300-459300'}

myregion = nuc_regions['HMR']
reg = myregion.split(':')
chrom, pStart, pEnd = reg[0], int(reg[1].split('-')[0]), int(reg[1].split('-')[1])

genome = '/private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa'
chrom_bam = '/private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/all_read.bam'
pos_bam = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.500.pass.sorted.bam'
neg_bam = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.0.pass.sorted.bam'


method = 'median'

models = {
    'resnet1D':resnet1D
}
mymodel = models['resnet1D']
myweight =  '/private/groups/brookslab/gabai/tools/seqUtils/src/nanopore_classification/best_models/addseq_resnet1d.pt'

sigAlign_HMR_chrom = '/private/groups/brookslab/gabai/projects/Add-seq/data/chrom/modPredict/231023_HMR_chrom_meanScore_medianPos_chrIII:290000-299000siganlAlign.tsv'
sigAlign_HMR_neg = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/modPredict/231023_HMR_neg_meanScore_medianPos_chrIII:290000-299000siganlAlign.tsv'
sigAlign_HMR_pos = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/modPredict/231023_HMR_pos_meanScore_medianPos_chrIII:290000-299000siganlAlign.tsv'

chrom_binScores, chrom_binCounts = exportBedGraph(region = myregion, sam = chrom_bam, sigAlign = sigAlign_HMR_chrom, genome=genome, model=mymodel, weight=myweight, binSize = 75)
writeBedGraph(bedGraphHeader = bedGraphHeader, binScores = chrom_binScores, binCounts = chrom_binCounts, 
              binSize =75, chrom = chrom, outfile = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/modPredict/231102_HMR_chrom.bedgraph')

pos_binScores, pos_binCounts = exportBedGraph(region = myregion, sam = pos_bam, sigAlign = sigAlign_HMR_pos, genome=genome, model=mymodel, weight=myweight, binSize = 75)
writeBedGraph(bedGraphHeader = bedGraphHeader, binScores = pos_binScores, binCounts = pos_binCounts,
              binSize =75, chrom = chrom, outfile = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/modPredict/231102_HMR_pos.bedgraph')

neg_binScores, neg_binCounts = exportBedGraph(region = myregion, sam = neg_bam, sigAlign = sigAlign_HMR_neg, genome=genome, model=mymodel, weight=myweight, binSize = 75)
writeBedGraph(bedGraphHeader = bedGraphHeader, binScores = neg_binScores, binCounts = neg_binCounts, 
              binSize =75, chrom = chrom, outfile = '/private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/modPredict/231102_HMR_neg.bedgraph')