#!/bin/bash
#SBATCH --job-name=GetNegArrow
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --nodes=1
#SBATCH --gres=gpu:2
#SBATCH --time=120:00:00
#SBATCH --mem=70G
#SBATCH --error=/private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/lsf_%j_%x.err      # error file
#SBATCH --output=/private/groups/brookslab/gabai/projects/Add-seq/scripts/sbatch/lsf_%j_%x.out     # output file
#SBATCH --mail-type=END,FAIL # email notification when job ends/fails
#SBATCH --mail-user=gabai@ucsc.edu  # email to notify

source /private/groups/brookslab/gabai/miniconda3/bin/activate addseq


python /private/groups/brookslab/gabai/projects/Add-seq/scripts/makeArrow.py -b /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/mapping/unique.0.sub0.3.pass.sorted.bam -e /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/eventalign/unique.0.eventalign.tsv -o /private/groups/brookslab/gabai/projects/Add-seq/data/ctrl/arrow/sub0.3_unique.0.eventalign.arrow
