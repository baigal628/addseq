#!/bin/bash
#SBATCH --job-name=RDN37ModPredict
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --nodes=1
#SBATCH --gres=gpu:4
#SBATCH --time=120:00:00
#SBATCH --mem=70G
#SBATCH --error=/private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/log/lsf_%j_%x.err      # error file
#SBATCH --output=/private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/log/lsf_%j_%x.out     # output file
#SBATCH --mail-type=END,FAIL # email notification when job ends/fails
#SBATCH --mail-user=gabai@ucsc.edu  # email to notify

source /private/groups/brookslab/gabai/miniconda3/bin/activate addseq

python3 /private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/py/231024_RDN37_mean_median_chrom.py

python3 /private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/py/231024_RDN37_mean_median_neg.py

python3 /private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/py/231024_RDN37_mean_median_pos.py
