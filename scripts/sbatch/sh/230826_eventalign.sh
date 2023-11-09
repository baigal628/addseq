#!/bin/bash
#SBATCH --job-name=nanopolish
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --nodes=1
##SBATCH --gres=gpu:2
#SBATCH --time=24:00:00
#SBATCH --mem=50G
#SBATCH --error=/private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/lsf_%j_%x.err      # error file
#SBATCH --output=/private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/lsf_%j_%x.out     # output file
#SBATCH --mail-type=END,FAIL # email notification when job ends/fails
#SBATCH --mail-user=gabai@ucsc.edu  # email to notify

source /private/groups/brookslab/gabai/miniconda3/bin/activate addseq

nanopolish index -d /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/unbasecalled/ /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/basecalled/all_read.fastq

nanopolish eventalign --threads 16 --samples --signal-index --print-read-names --reads /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/basecalled/all_read.fastq --bam /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/AUA1.bam --genome /private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa  --scale-events > /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/eventalign/AUA1.eventalign.txt

nanopolish eventalign --threads 16 --samples --signal-index --print-read-names --reads /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/basecalled/all_read.fastq --bam /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/EMW1.bam --genome /private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa  --scale-events > /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/eventalign/EMW1.eventalign.txt

nanopolish eventalign --threads 16 --samples --signal-index --print-read-names --reads /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/basecalled/all_read.fastq --bam /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/CLN2.bam --genome /private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa  --scale-events > /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/eventalign/CLN2.eventalign.txt

nanopolish eventalign --threads 16 --samples --signal-index --print-read-names --reads /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/basecalled/all_read.fastq --bam /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/PHO3.bam --genome /private/groups/brookslab/gabai/projects/Add-seq/data/ref/sacCer3.fa  --scale-events > /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/eventalign/PHO3.eventalign.txt
