#!/bin/bash
#SBATCH --job-name=SubsetBamFiles
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --nodes=1
##SBATCH --gres=gpu:2
#SBATCH --time=24:00:00
#SBATCH --mem=10G
#SBATCH --error=/private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/lsf_%j_%x.err      # error file
#SBATCH --output=/private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/lsf_%j_%x.out     # output file
#SBATCH --mail-type=END,FAIL # email notification when job ends/fails
#SBATCH --mail-user=gabai@ucsc.edu  # email to notify


samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/all_read.bam -q 20 -F 0x900 -@ 4 "chrVI:114000-116000" > /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/AUA1.bam
samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/all_read.bam -q 20 -F 0x900 -@ 4 "chrXIV:42500-51000" > /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/EMW1.bam
samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/all_read.bam -q 20 -F 0x900 -@ 4 "chrXIV:42500-51000" > /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/EMW1.bam
samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/all_read.bam -q 20 -F 0x900 -@ 4 "chrXIV:65000-69000" > /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/CLN2.bam
samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/all_read.bam -q 20 -F 0x900 -@ 4 "chrII:427500-450000" > /private/groups/brookslab/gabai/projects/Add-seq/data/chrom/mapping/PHO3.bam

samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.500.pass.sorted.bam -q 20 -F 0x900 -@ 4 "chrVI:114000-116000" > /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/AUA1_pos.bam
samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.500.pass.sorted.bam -q 20 -F 0x900 -@ 4 "chrXIV:42500-51000" > /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/EMW1_pos.bam
samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.500.pass.sorted.bam -q 20 -F 0x900 -@ 4 "chrXIV:42500-51000" > /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/EMW1_pos.bam
samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.500.pass.sorted.bam -q 20 -F 0x900 -@ 4 "chrXIV:65000-69000" > /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/CLN2_pos.bam
samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.500.pass.sorted.bam -q 20 -F 0x900 -@ 4 "chrII:427500-450000" > /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/PHO3_pos.bam


samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.0.pass.sorted.bam -q 20 -F 0x900 -@ 4 "chrVI:114000-116000" > /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/AUA1_neg.bam
samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.0.pass.sorted.bam -q 20 -F 0x900 -@ 4 "chrXIV:42500-51000" > /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/EMW1_neg.bam
samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.0.pass.sorted.bam -q 20 -F 0x900 -@ 4 "chrXIV:42500-51000" > /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/EMW1_neg.bam
samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.0.pass.sorted.bam -q 20 -F 0x900 -@ 4 "chrXIV:65000-69000" > /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/CLN2_neg.bam
samtools view -b /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.0.pass.sorted.bam -q 20 -F 0x900 -@ 4 "chrII:427500-450000" > /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/PHO3_neg.bam