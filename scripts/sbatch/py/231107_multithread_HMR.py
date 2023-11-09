import multiprocessing
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
import matplotlib.patches as mplpatches
from collections import defaultdict
from plotUtil import *
import threading

nuc_regions = {
            'PHO5': 'chrII:429000-435000',
                'CLN2': 'chrXVI:66000-67550',
                    'HMR': 'chrIII:290000-299000',
                        'AUA1': 'chrVI:114000-116000',
                            'EMW1': 'chrXIV:45000-50000',
                                'NRG2': 'chrII:370000-379000',
                                    'RDN37': 'chrXII:450300-459300'}


myregion = nuc_regions['HMR']

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

def nucPredict(readID, eventStart, sigList, sigLenList, pStart, bins, refSeq, kmerWindow, signalWindow, threshold,
               device, model, weight):
    print('Start processing ', readID)
    
    start_time = time.time()
    sigLenList_init = pStart-eventStart-1
    binScores = {bin:0 for bin in bins}
    binCounts = {bin:0 for bin in bins}
    
    for bin in bins:
        # print('Predicting at position:', bin, '-', bin+kmerWindow)
        # 1. Fetch sequences with kmer window size, this step is optional
        seq = refSeq[bin:bin+kmerWindow]
        # 2. Fetch signals with signal window size 
        signals = fetchSignal(bin-pStart, sigLenList_init, sigLenList, sigList, kmerWindow, signalWindow)
        if signals == 'del':
            continue
        if signals == 'end':
            break
        # 3. Get predicted probability score from machine learning model
        prob = nntPredict(signals, device = device, model = model, weights_path = weight)
        if prob > threshold:
            binScores[bin]+=1
        binCounts[bin] +=1

    total_time = "%.2f" % (time.time()-start_time)
    
    print('finished processing ', readID, ' in ', total_time, 's.')
    
    return binScores, binCounts

def process_read(worker_input):
    (readID, eventStart, sigList, sigLenList, pStart, bins, refSeq, 
     kmerWindow, signalWindow, threshold, device, model, weight) = worker_input
    
    binScores, binCounts = nucPredict(readID, eventStart, sigList, sigLenList, pStart, bins, refSeq, kmerWindow, signalWindow, threshold, device, model, weight)

    return readID, binScores, binCounts

def modPredict(region, sam, sigAlign, kmerWindow=75, signalWindow=400, threshold = 0.7, modBase = ['AT', 'TA'], 
                   genome = genome, model = mymodel, weight = myweight, device = device, pool_size = 6):

    alignment = getAlignedReads(sam = sam, region = region, genome=genome, print_name=False)
    refSeq = alignment['ref']    
    reg = region.split(':')
    chrom, pStart, pEnd = reg[0], int(reg[1].split('-')[0]), int(reg[1].split('-')[1])
    
    bins = np.arange(pStart, pEnd, kmerWindow)

   
    num_processes = min(pool_size, multiprocessing.cpu_count())  # Use the specified pool size or maximum available CPU cores
    pool = multiprocessing.Pool(processes=num_processes)

    # Prepare worker input data for parallel processing
    worker_inputs = [(readID, eventStart, sigList, sigLenList, pStart, bins, refSeq, kmerWindow, signalWindow, 
                      threshold, device, model, weight) for readID, eventStart, sigList, sigLenList in parseSigAlign(sigAlign)]

    # Use the pool.map() function to process reads in parallel
    results = pool.map(process_read, worker_inputs)

    # Close the pool to release resources
    pool.close()
    pool.join()

    return results

def exportBdgFromPredict(predictedScores):
    binScores = []
    binCounts = []
    with open(predictedScores, 'r') as predScoresFh:
        for line in predScoresFh:
            line = line.strip().split('\t')
            binScores.append(line[1].split(','))
            binCounts.append(line[2].split(','))
    
    binScores = np.array(binScores, dtype = int)
    binCounts = np.array(binCounts, dtype = int)
    normScores = np.sum(binScores, axis = 0)*1000/np.sum(binCounts, axis = 0)
    
    return normScores


def writeBedGraph(header, scores, binSize, region, outfile, print_result = False):
    
    
    reg = region.split(':')
    chrom, pStart, pEnd = reg[0], int(reg[1].split('-')[0]), int(reg[1].split('-')[1])
    bins = np.arange(pStart, pEnd, binSize) 
    
    outFh = open(outfile, 'w')
    
    for k,v in bedGraphHeader.items():
        if v:
            line = k + '=' + v + ' '
            outFh.write(line)
    outFh.write('\n')
    i = 0
    for chrStart in bins:
        chrEnd = chrStart + binSize
        score = "%.3f" % (scores[i])
        line = '{chr}\t{start}\t{end}\t{score}\n'.format(chr = chrom, start = chrStart,  end = chrEnd, score = score)
        if print_result:
            print(line)
        outFh.write(line)
        i+=1
    outFh.close()

bedGraphHeader = {'track type':'bedGraph', 
              'name':'AUA1_0.65', 
              'description':'addseq',
              'visibility':'', 
              'color':'r', 
              'altColor':'r', 
              'priority':'', 
              'autoScale':'off', 
              'alwaysZero':'off', 
              'gridDefault':'off', 
              'maxHeightPixels':'default', 
              'graphType':'bar',
              'viewLimits':'upper',
              'yLineMark':'',
              'yLineOnOff':'on',
              'windowingFunction':'mean',
              'smoothingWindow':'on'
             }

if __name__ == '__main__':
    torch.multiprocessing.set_start_method('spawn')
    results = modPredict(region = myregion, sam = chrom_bam, sigAlign = sigAlign_HMR_chrom, genome = genome, 
                                                  model= mymodel, weight = myweight,  threshold = 0.60)
    prefix = '231108_HMR_chrom_0.60'
    
    predictedScores_out = '/private/groups/brookslab/gabai/projects/Add-seq/data/chrom/modPredict/' + prefix + '_predictedScores.tsv'
    outFh = open(predictedScores_out, 'w')
    for (readID, binScore, binCount) in results:
        outFh.write('{readID}\t{binScores}\t{binCounts}\n'.format(readID=readID, binScores = ','.join(map(str, binScore.values())), binCounts = ','.join(map(str, binCount.values()))))
    outFh.close()

    normScores = exportBdgFromPredict(predictedScores_out)
    bedGraphHeader['name'] = prefix
    predictedScores_out = '/private/groups/brookslab/gabai/projects/Add-seq/data/chrom/modPredict/' + prefix + '_predictedScores.bedgraph'
    writeBedGraph(bedGraphHeader, normScores, 75, region = myregion, outfile = predictedScores_out)