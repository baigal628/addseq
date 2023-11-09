import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.utils.data import DataLoader
from torchsummary import summary
from tqdm import tqdm
from nanopore_dataset import create_sample_map
from nanopore_dataset import create_splits
from nanopore_dataset import load_csv
from nanopore_dataset import NanoporeDataset

from resnet1d import ResNet1D
import seaborn as sns

device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

model = ResNet1D(
            in_channels=1,
            base_filters=128,
            kernel_size=3,
            stride=2,
            groups=1,
            n_block=8,
            n_classes=2,
            downsample_gap=2,
            increasefilter_gap=4,
            use_do=False)

summary(model, (1, 400), device= device)


MESMLR_FN = './nanopore_classification/best_models/mesmlr_resnet1d.pt'
ADDSEQ_FN = './nanopore_classification/best_models/addseq_resnet1d.pt'

weights_path = ADDSEQ_FN
model.load_state_dict(torch.load(weights_path, map_location=torch.device(device)))
model.to(device)
model.eval()


neg_fn = '../data/data/addseq/reprocessed-unique.0.eventalign.signal.csv'
pos_fn = '../data/data/addseq/reprocessed-unique.500.eventalign.signal.csv'

min_val = 50 # Used to clip outliers
max_val = 130 # Used to clip outliers

seq_len = 400

print("Preparing unmodified...")
print("Loading csv...")
unmodified_sequences = load_csv(neg_fn,
                                min_val=min_val,
                                max_val=max_val,
                                max_sequences=None)
print("Creating sample map...")
unmodified_sample_map = create_sample_map(unmodified_sequences,
                                          seq_len=seq_len)

print("Creating splits...")
unmodified_train, unmodified_val, unmodified_test = create_splits(
        unmodified_sequences, unmodified_sample_map, seq_len=seq_len, shuffle=False)
print("Prepared.")

print("Preparing modified...")
print("Loading csv...")
modified_sequences = load_csv(pos_fn,
                              min_val=min_val,
                              max_val=max_val,
                              max_sequences=None)
print("Creating sample map...")
modified_sample_map = create_sample_map(modified_sequences,
                                        seq_len=seq_len)
print("Creating splits...")
modified_train, modified_val, modified_test = create_splits(
        modified_sequences, modified_sample_map, seq_len=seq_len, shuffle=False)
print("Prepared.")


batch_size = 512
val_dataset = NanoporeDataset(unmodified_sequences,
                              unmodified_val,
                              modified_sequences,
                              modified_val,
                              device=device,
                              synthetic=False,
                              seq_len=seq_len)

val_dataloader = DataLoader(val_dataset,
                            batch_size=batch_size,
                            shuffle=True)

pos_read = []
neg_read = []

with torch.no_grad():
    seq_preds = {}
    dataloader_idx = 0
    for samples, labels in tqdm(val_dataloader):
        samples.to(device)
        pred = model(samples).sigmoid()
        for i in range(len(pred)):
            seq_idx = val_dataset.get_seq_idx(dataloader_idx)
            dataloader_idx += 1
            seq_label = labels[i].item()
            prediction = pred[i].item()
            seq_id = (seq_label, seq_idx)
            if seq_id not in seq_preds:
                seq_preds[seq_id] = []
            seq_preds[seq_id].append(pred[i].item())
            if seq_label == 1.0:
                pos_read.append(prediction)
            else:
                neg_read.append(prediction)
                
    
print('Plotting figures...')
sns.kdeplot(np.array(neg_read), label= 'neg')
sns.kdeplot(np.array(pos_read), label= 'pos')
plt.legend()
plt.savefig('../results/figures/addseq_full_prediction_prob_distribution.pdf')
plt.close()


print('Compute summary performance statistics...')

correct = {0: 0, 1: 0}
total = {0: 0, 1: 0}

for seq_id in tqdm(seq_preds):
    label = seq_id[0]
    pred_arr = np.round(np.array(seq_preds[seq_id]))
    if label == 0:
        label_arr = np.zeros(len(pred_arr))
    else:
        label_arr = np.ones(len(pred_arr))
    correct_arr = (pred_arr == label_arr)
    correct[label] += np.sum(correct_arr)
    total[label] += len(pred_arr)

accuracy = (correct[0] + correct[1]) / float(total[0] + total[1])  

true_negatives = correct[0]
true_positives = correct[1]
false_negatives = total[1] - correct[1]
false_positives = total[0] - correct[0]

precision = true_positives / float(true_positives + false_positives)
recall = true_positives / float(true_positives + false_negatives)

print("True negatives:", true_negatives)
print("True positives:", true_positives)
print("False negatives:", false_negatives)
print("False positives:", false_positives)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)


print('Ploting prediction mean and std for each validation sequence...')

seq_means = {0: [], 1: []}
seq_stds = {0: [], 1: []}
for seq_id in tqdm(seq_preds):
    label = seq_id[0]
    seq_means[label].append(np.mean(seq_preds[seq_id]))
    seq_stds[label].append(np.std(seq_preds[seq_id]))
plt.scatter(seq_means[0], seq_stds[0], label='negative')
plt.scatter(seq_means[1], seq_stds[1], label='positive')
plt.legend()
plt.xlabel('Prediction Mean')
plt.ylabel('Prediction Std')
plt.savefig('../results/figures/addseq_full_prediction_mean_variance.pdf')
plt.close()

print('Ploting ROC curve...')
from sklearn.metrics import roc_curve

pred_list = []
label_list = []
for seq_id in tqdm(seq_preds):
    seq_len = len(seq_preds[seq_id])
    label = seq_id[0]
    preds = seq_preds[seq_id]
    if label == 0:
        labels = np.zeros(seq_len)
    else:
        labels = np.ones(seq_len)
    pred_list.append(preds)
    label_list.append(labels)
    
pred_cat = np.concatenate(pred_list)
label_cat = np.concatenate(label_list)

fpr, tpr, thresholds = roc_curve(label_cat, pred_cat)
plt.plot(fpr, tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.savefig('../results/figures/addseq_full_prediction_ROC.pdf')
plt.close()