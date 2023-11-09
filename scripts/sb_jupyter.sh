#!/bin/bash
#SBATCH --job-name=gali_jupyter
#SBATCH --ntasks=1
##SBATCH --cpus-per-task=8
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --time=96:00:00
#SBATCH --mem=50G



source /private/groups/brookslab/gabai/miniconda3/bin/activate addseq

# get tunneling info
XDG_RUNTIME_DIR=""
node=$(hostname -s)
user=$(whoami)
cluster="phoenix"
port=8886
if [ "$1" != "" ]; then
  port=$1
fi

# print tunneling instructions jupyter-log
echo -e "
Command to create ssh tunnel:
ssh -N -f -L ${port}:${node}:${port} ${user}@${cluster}.prism

Use a Browser on your local machine to go to:
localhost:${port}  (prefix w/ https:// if using password)
"

# Run Jupyter
jupyter notebook --no-browser --port=${port} --ip=${node}
