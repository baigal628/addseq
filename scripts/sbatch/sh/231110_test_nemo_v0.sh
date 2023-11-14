python3 /private/home/gabai/tools/seqUtils/src/findNemo.py  \
    --region chrII \
    --bam /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/chrom.sorted.bam \
    --genome /private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa \
    --eventalign /data/scratch/gabai/addseq_data/eventalign/chrII.eventalign.txt \
    --sigalign /scratch/gabai/addseq_data/231110_test_nemo_v0_chrII/231110_test_chrII_sig_sub1.tsv \
    --outpath /scratch/gabai/addseq_data/231110_test_nemo_v0_chrII/ \
    --prefix 231110_test \
    --threads 2

python3 /private/home/gabai/tools/seqUtils/src/findNemo.py  \
    --region chrIII \
    --bam /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/chrom.sorted.bam \
    --genome /private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa \
    --eventalign /data/scratch/gabai/addseq_data/eventalign/chrIII.eventalign.txt \
    --outpath /data/scratch/gabai/addseq_data/231112_test_nemo_v0_chrIII/ \
    --prefix 231112_test \
    --threads 8


python3 /private/home/gabai/tools/seqUtils/src/findNemo.py  \
    --region chrII \
    --bam /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/chrom.sorted.bam \
    --genome /private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa \
    --eventalign /data/scratch/gabai/addseq_data/eventalign/chrII.eventalign.txt \
    --outpath /data/scratch/gabai/addseq_data/231112_test_nemo_v0_chrII/ \
    --prefix 231112_test \
    --threads 8