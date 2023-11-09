import pysam
import bisect
import time
from pyarrow import feather, Table
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.utils.data import DataLoader
from torchsummary import summary
from tqdm import tqdm

from nanopore_dataset import create_sample_map
from nanopore_dataset import create_splits
from nanopore_dataset import load_csv
from nanopore_dataset import NanoporeDataset
from resnet1d import ResNet1D
import seaborn as sns

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print('Device type:', device, flush=True)

model = ResNet1D(
            in_channels=1,
            base_filters=128,
            kernel_size=3,
            stride=2,
            groups=1,
            n_block=8,
            n_classes=2,
            downsample_gap=2,
            increasefilter_gap=4,
            use_do=False)
model.to(device)
summary(model, (1, 400), device= device)

ADDSEQ_FN = './nanopore_classification/best_models/addseq_resnet1d.pt'

weights_path = ADDSEQ_FN
model.load_state_dict(torch.load(weights_path, map_location=torch.device(device)))

model.eval()

ntDict = {'A': 'T', 'C': 'G', 'G': 'C', 'T':'A'}

def reverseCompliment(seq):
    return ''.join([ntDict[i] for i in seq[::-1]])

def alignScore(eventAlign = '', parse_bam = '', downReads = '', downScores = '', method = ''):
    '''
    alignScore function: User input bam file and eventalign file, for each read, the function assign 400 scores to 80 bp sequences.
    '''
    
    cawlr_read = []
    readID = ''
    sequence = ''
    strandID = 'NA'
    signalLength = 0
    signalLengthList = []
    start_time = time.time()
    with open(eventAlign, 'r') as inFile:
        header = inFile.readline()
        for line in inFile:
            line = line.strip().split('\t')
            read = line[3]
            if read in parse_bam:
                strand = parse_bam[read]
            else:
                # print(str(read) + ' not found in bam file!', flush=True)
                continue
            # the very first read or new read
            if readID != read:
                # Store information for the proceesing read
                if sequence:
                    metadata, scores = modPredict(read=readID, chrom=chrom, start=start,
                                                  seq = sequence, signals = signalList,
                                                  signalLengthList=signalLengthList, strandInt=strandID, 
                                                  downScores = downScores, method = method)
                    cawlr_read.append({"metadata": metadata, "scores": scores})
                    if len(cawlr_read)%250 == 0:
                        current_time = time.time()-start_time
                        print('Processed '+ str(len(cawlr_read)), ' reads in ', "%.3f" % current_time, ' seconds.', flush=True)
                    if downReads:
                        if len(cawlr_read) > downReads:
                            sequence = ''
                            break
                    # Set variables back to initial state
                    readID = ''
                    sequence = ''
                    signalList = []
                    signalLength = 0
                    signalLengthList = []
                readID = read
                strandID = strand
                chrom = line[0]
                start = line[1]
                kmer = line[2]
                # signals are stored in column 13 and are separated my comma
                signals = [float(i) for i in line[13].split(',')]
                signalList = signals
                signalLength = len(signals)
                if strandID == -1:
                    kmer = reverseCompliment(kmer)
                sequence += kmer
            # next kmer within the same read
            else:
                signals = [float(i) for i in line[13].split(',')]
                # signalList += signals
                signalList.extend(signals)
                # signalLength records the number of signals for one base movement
                signalLength += len(signals)
                # different kmer
                #  (kmer1, chrom1, start1) = (kmer0, chrom0, start0)
                if (line[2], line[0], line[1]) != (kmer, chrom, start):
                    kmer = line[2]
                    sequence += kmer[-1]
                    signalLengthList.append(signalLength)
        if sequence:
            metadata, scores = modPredict(read=readID, chrom=chrom, start=start,
                                          seq = sequence, signals = signalList,
                                          signalLengthList=signalLengthList, strandInt=strandID, 
                                          downScores = downScores, method = method)
            cawlr_read.append({"metadata": metadata, "scores": scores})
    
    return cawlr_read


def sumScore(probList, method = ''):
    '''
    Set different ways to summarize the predicted probability when there is multiple probability matches the same kmer.
    '''
    
    if method == 'max':
        return np.max(probList)
    elif method == 'mean':
        return np.mean(probList)
    elif method == 'median':
        return np.median(probList)
    else:
        print('method not found or invalid!', flush=True)


def modPredict(read, chrom, start, seq, signals, signalLengthList, strandInt, downScores = '', method = '', 
               signalWindow = 400, seqLength = 80):
    
    strand = {
        "strand": strandInt,
    }

    metadata = {
        "chrom": str(chrom),
        "length": int(len(seq)),
        "name": str(read),
        # seq will always be an empty string
        "seq": "addseq_pos",
        "start": int(start),
        # True is positive strand, False is negative strand
        "strand": strand,
    }

    scores = []
    outScore = {
        # left most position represent the position
        # ie T is 101, A is 102, T is 103, T is 104, etc.
        "kmer": "",
        "pos": 0,
        # For your case, "score" and "signal_score" should be the same
        # This is where you will put in the scores output by the method
        # you are working with.
        "score": 0,
        "signal_score": 0,
        # For your case, skip_score is always 0.0
        "skip_score": 0.0,
        # For your case, skipped will always be set to False
        "skipped": False,
    }

    input_tensor = torch.zeros((1, 1, 400)).to(device)
    sequence_tensor = torch.tensor(signals)

    # Here signal window must be 400
    # for pos in tqdm(range(len(signals)-signalWindow)):
    for pos in range(len(signals)-signalWindow):
        # print(len(signals)-signalWindow)
        # if pos%5 != 0:
        #     # print(pos)
        #     continue
        input_tensor[:, :, :] = sequence_tensor[pos:pos+signalWindow]
        # match 400 signals to the kmer
        # signalLengthList stores the cumulative number of signals that aligns to each base
        left = bisect.bisect_right(signalLengthList, pos)
        right = left + seqLength
#       right = bisect.bisect_left(signalLengthList, pos+signalWindow)
        kmer = seq[left:right]
        # Store absolute position instead of relative position 
        startPos = left + int(start)
        prob = model(input_tensor).sigmoid().item()
        # either the very first kmer or the new kmer
        if (kmer, startPos) != (outScore["kmer"], outScore["pos"]):
            # print('old: ', outScore["kmer"], " ", outScore["pos"])
            # print('new: ', kmer, " ", start)
            # store the previous kmer information
            if outScore["kmer"]:
                scores.append({
                    # left most position represent the position
                    # ie T is 101, A is 102, T is 103, T is 104, etc.
                    "kmer": str(outScore["kmer"]),
                    "pos": int(outScore["pos"]),
                    # For your case, "score" and "signal_score" should be the same
                    # This is where you will put in the scores output by the method
                    # you are working with.
                    "score": float(sumScore(probList, method = method)),
                    "signal_score": float(sumScore(probList, method = method)),
                    # For your case, skip_score is always 0.0
                    "skip_score": 0.0,
                    # For your case, skipped will always be set to False
                    "skipped": False,
                })
                # if len(scores)%100000 == 0:
                #     print(len(scores), ' modification scores are called for current read.', )
                if downScores:
                    if len(scores) >= downScores:
                        outScore["kmer"] = ""
                        break
            # store the new kmer information
            outScore["kmer"] = str(kmer)
            outScore["pos"] = int(startPos)
            probList = [prob]
        else:
            probList.append(prob)
    if outScore["kmer"]:
        scores.append({
            # left most position represent the position
            # ie T is 101, A is 102, T is 103, T is 104, etc.
            "kmer": str(outScore["kmer"]),
            "pos": int(outScore["pos"]),
            # For your case, "score" and "signal_score" should be the same
            # This is where you will put in the scores output by the method
            # you are working with.
            "score": float(sumScore(probList, method = method)),
            "signal_score": float(sumScore(probList, method = method)),
            # For your case, skip_score is always 0.0
            "skip_score": 0.0,
            # For your case, skipped will always be set to False
            "skipped": False,
        })
    
    return (metadata, scores)