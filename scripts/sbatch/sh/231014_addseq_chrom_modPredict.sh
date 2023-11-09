#!/bin/bash
#SBATCH --job-name=chromModPredict
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --nodes=1
#SBATCH --gres=gpu:0
#SBATCH --time=120:00:00
#SBATCH --mem=70G
#SBATCH --error=/private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/lsf_%j_%x.err      # error file
#SBATCH --output=/private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/lsf_%j_%x.out     # output file
#SBATCH --mail-type=END,FAIL # email notification when job ends/fails
#SBATCH --mail-user=gabai@ucsc.edu  # email to notify

source /private/groups/brookslab/gabai/miniconda3/bin/activate addseq

python3 /private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/py/231014_mean_mean_chrom.py
