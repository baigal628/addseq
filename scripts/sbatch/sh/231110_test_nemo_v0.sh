python3 /private/home/gabai/tools/seqUtils/src/findNemo.py  \
    --mode predict \
    --region chrII \
    --bam /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/chrom.sorted.bam \
    --genome /private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa \
    --eventalign /data/scratch/gabai/addseq_data/eventalign/chrII.eventalign.txt \
    --sigalign /scratch/gabai/addseq_data/231110_test_nemo_v0_chrII/231110_test_chrII_sig_sub1.tsv \
    --outpath /scratch/gabai/addseq_data/231110_test_nemo_v0_chrII/ \
    --prefix 231110_test \
    --threads 2

python3 /private/home/gabai/tools/seqUtils/src/findNemo.py  \
    --mode predict \
    --region chrII \
    --bam /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/chrom.sorted.bam \
    --genome /private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa \
    --sigalign /data/scratch/gabai/addseq_data/231112_test_nemo_v0_chrII/231114_n100_chrII_sig.tsv \
    --outpath /data/scratch/gabai/addseq_data/231112_test_nemo_v0_chrII/ \
    --prefix 231114_n100 \
    --threads 8


    python3 /private/home/gabai/tools/seqUtils/src/findNemo.py  \
    --mode predict \
    --region chrIII \
    --bam /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/chrom.sorted.bam \
    --genome /private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa \
    --sigalign /data/scratch/gabai/addseq_data/231112_test_nemo_v0_chrIII/231114_test_chrIII_sig_n8.tsv \
    --outpath /data/scratch/gabai/addseq_data/231112_test_nemo_v0_chrIII/ \
    --prefix 231114_read_n8 \
    --threads 8


python3 /private/home/gabai/tools/seqUtils/src/findNemo.py  \
    --mode predict \
    --region chrII \
    --bam /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/chrom.sorted.bam \
    --genome /private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa \
    --sigalign /data/scratch/gabai/addseq_data/231112_test_nemo_v0_chrII/231115_chrII_after1542_sig.tsv \
    --outpath /data/scratch/gabai/addseq_data/231112_test_nemo_v0_chrII/ \
    --prefix 231115_complete \
    --threads 16


python3 /private/home/gabai/tools/seqUtils/src/findNemo.py  \
    --mode predict \
    --region chrIII \
    --bam /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/chrom.sorted.bam \
    --genome /private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa \
    --sigalign /data/scratch/gabai/addseq_data/231112_test_nemo_v0_chrIII/231112_test_chrIII_sig.tsv \
    --outpath /data/scratch/gabai/addseq_data/231112_test_nemo_v0_chrIII/ \
    --prefix 231114_read_complete \
    --threads 8