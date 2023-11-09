from modTool import alignScore, modPredict
from pyarrow import feather, Table
import pysam
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('--bam','-b',default='/scratch/gabai/addseq/data/ctrl/unique.0.pass.sorted.bam', type=str,action='store',help='bam alignment file goes here')
parser.add_argument('--eventAlign','-e',default='/gicephfs/brookslab/bsaintjo/220516_ang_conc_unique/unique.0.eventalign.tsv', type=str,action='store',help='eventAlign input file goes here')
parser.add_argument('--downReads','-r',default=0, type=int, action='store',help='number of reads to downsample.')
parser.add_argument('--downScores','-s',default=0, type=int, action='store',help='number of scores to downsample per read.')
parser.add_argument('--method','-m',default='max', type=str, action='store',help='method to summarize list of scores per genome location.')
parser.add_argument('--coordinate','-c',default='chr7:45232000-45241000', type=str,action='store', help='coordinate to plot goes here')
parser.add_argument('--arrow','-a',default='/private/groups/brookslab/gabai/projects/Add-seq/data/testdata/pos_scores.arrow', type=str,action='store', help='example arrow file goes here')
parser.add_argument('--outFile','-o',default='/scratch/gabai/addseq/data/ctrl/unique.0.arrow', type=str, action='store',help='output file goes here')

args = parser.parse_args()

samFile = args.bam
evenAlignFile = args.eventAlign
region = args.coordinate
outputFile = args.outFile
downReads = args.downReads
downScores = args.downScores
method = args.method
example_arrow_file = args.arrow

start_time = time.time()
print('Start parsing the bam file...', flush=True)
samfile = pysam.AlignmentFile(samFile, "rb")
parse_bam = {}
for s in samfile:
    readID = s.query_name
    strand = -1 if s.is_reverse else 1
    parse_bam[readID] = strand
samfile.close()
print('Finished parsing the bam file...', flush=True)

setDownReads = '' if downReads == 0 else downReads
setDownScores = '' if downScores == 0 else downScores

print('Start aliging signals to scores...', flush=True)
cawlrRead = alignScore(eventAlign = evenAlignFile, downReads=setDownReads, downScores=setDownScores, parse_bam = parse_bam, method = method)


scored = {"scored": cawlrRead}
new_fdict = scored

table = feather.read_table(example_arrow_file)

output = Table.from_pydict(new_fdict, schema=table.schema)
feather.write_feather(output, outputFile)
print("Done in %.3f seconds." % (time.time() - start_time), flush=True)