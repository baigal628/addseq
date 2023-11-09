chrVI_evt = '/private/groups/brookslab/gabai/projects/Add-seq/data/chrom/eventalign/chrVI.eventalign.txt'

def parseEventAlign(eventAlign = '', outfile = '', print_sequence = False, header = True):
    '''
    This function reads nanopolish eventalign file, aggregates signals and the number of 
    signals correspinding to one base movement for read in readname list.
    
    input:
        eventAlign: nanopolish eventalign output file.
    optional:
        print_sequence: if True, kmer sequence will be included in outfile.
    output: 
        outfile: siganlAlign.tsv with format: readname\tchrom\teventStart(reference)\tsigList\tsigLenLsit

    E.g.    read1  ACGTGGCTGA
            events ACGTG
                    CGTGG
                     GTGGC
                      TGGCT
                       GGCTG
                        GCTGA
            sigLen  23
                     45
                      61
                       78
                        101
    '''
    
    if outfile:
        outf = open(outfile, 'w')
    
    read = ''
    sequence = ''
    c = 0
    
    with open(eventAlign, 'r') as inFile:
        if header:
            header = inFile.readline()
        for line in inFile:
            line = line.strip().split('\t')
            thisread = line[3]
            thischrom = line[0]
            c+=1
            if c%10000000 == 0:
                print(c/1000000, ' M lines have passed.')

            if thisread != read:

                # parsed read exist
                if sequence:
                    # Set variables back to initial state
                    if print_sequence:
                        out = "{}\t{}\t{}\t{}\t{}\t{}\n".format(read, chrom, eventStart, sequence, ','.join(str(i) for i in sigList), ','.join(str(i) for i in sigLenList))
                    else:
                        out = "{}\t{}\t{}\t{}\t{}\n".format(read, chrom, eventStart, ','.join(str(i) for i in sigList), ','.join(str(i) for i in sigLenList))
                    if outfile:
                        outf.write(out)
                    read = ''
                    sequence = ''
                    sigList = []
                    sigLenList = []

                # very first read
                read = thisread
                chrom = thischrom
                eventStart = line[1]
                start = line[1]
                kmer = line[2]

                # signals are stored in column 13/15 and are separated my comma
                sigList = [float(i) for i in line[-1].split(',')]
                sigLen = len(sigList)
                sigLenList = [sigLen]
                sequence = kmer
            
            # next kmer within the same read
            else:
                signals = [float(i) for i in line[-1].split(',')]
                # or signalList += signals
                sigList.extend(signals)
                # signalLength records the number of signals for one base movement
                sigLen += len(signals)

                # If different kmer
                if (line[1], line[2]) != (start, kmer):
                    deletion = int(line[1]) - int(start) - 1
                    # id there is a deletion in eventalign file
                    if deletion > 0:
                        sequence += deletion*'D'
                        for i in range(deletion):
                            sigLenList.append(sigLenList[-1])
                    start = line[1]
                    kmer = line[2]
                    sequence += kmer[-1]
                    sigLenList.append(sigLen)
                # If same kmer
                else:
                    # Update the number of signals matched to previous kmer
                    sigLenList[-1]=sigLen
        if sequence:
            if print_sequence:
                out = "{}\t{}\t{}\t{}\t{}\t{}\n".format(read, chrom, eventStart, sequence, ','.join(str(i) for i in sigList), ','.join(str(i) for i in sigLenList))
            else:
                out = "{}\t{}\t{}\t{}\t{}\n".format(read, chrom, eventStart, ','.join(str(i) for i in sigList), ','.join(str(i) for i in sigLenList))
            if outfile:
                outf.write(out)
    outf.close()

parseEventAlign(eventAlign = chrVI_evt, outfile= '/data/scratch/gabai/addseq_data/eventalign/chrVI.eventalign.tsv')

