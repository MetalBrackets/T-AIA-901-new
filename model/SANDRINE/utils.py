
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc, roc_auc_score
from sklearn.preprocessing import label_binarize
from itertools import cycle
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
from itertools import cycle
import tensorflow as tf


def encode_data(data, tokenizer, label_encoder, max_length=36):
    tokens = []
    labels = []

    for i, row in data.iterrows():
        phrase = row['Phrase']
        dep = row['Départ']
        arr = row['Arrivée']

        if i < 4:
            print(f"\n---> Ligne {i+1}")
            print("- Original sentence: ", phrase)

        dep_positions = []
        arr_positions = []

        start = 0  # find all starting occurrences
        while True:
            idx = phrase.find(dep, start)
            if idx == -1:
                break
            dep_positions.append((idx, idx + len(dep)))
            start = idx + len(dep)

        start = 0  # find all arrival occurrences
        while True:
            idx = phrase.find(arr, start)
            if idx == -1:
                break
            arr_positions.append((idx, idx + len(arr)))
            start = idx + len(arr)

        tokenized_input = tokenizer.encode_plus(
            phrase,
            add_special_tokens=True,
            return_offsets_mapping=True,
            max_length=max_length,
            truncation=True,
            padding="max_length",
            return_tensors="tf"
        )

        tokenized_text = tokenizer.convert_ids_to_tokens(tokenized_input.input_ids[0])
        offsets = tokenized_input['offset_mapping'].numpy()[0]
        label_list = ['O'] * len(tokenized_text)

        if i < 4:
            print("- Encoded tokens: ", tokenized_text)

        for j, (offset_start, offset_end) in enumerate(offsets):  # attribution of labels to tokens
            if offset_start == 0 and offset_end == 0:
                continue  # padding token
            token_label = 'O'

            for entity_start, entity_end in dep_positions: # check if the token overlaps a starting entity
                if (offset_start >= entity_start) and (offset_end <= entity_end):
                    if offset_start == entity_start:
                        token_label = 'B-DEP'
                    else:
                        token_label = 'I-DEP'
                    break
            
            for entity_start, entity_end in arr_positions: # check if the token overlaps an arrival entity
                if (offset_start >= entity_start) and (offset_end <= entity_end):
                    if offset_start == entity_start:
                        token_label = 'B-ARR'
                    else:
                        token_label = 'I-ARR'
                    break

            label_list[j] = token_label

        # Ensure no 'I-xxx' is used without a preceding 'B-xxx' or 'I-xxx'
        for k in range(1, len(label_list) - 1):  # exclude [CLS] and [SEP]
            if label_list[k].startswith('I-'): 
                entity_type = label_list[k][2:]
                if k == 0: # if the first label in the list is 'I-xxx', change it to 'B-xxx'
                    label_list[k] = 'B-' + entity_type
                else: # else the previous label is not 'B-xxx' or 'I-xxx' of the same type, change 'I-xxx' to 'B-xxx'
                    prev_label = label_list[k-1] # Get the previous label
                    if not (prev_label == 'B-' + entity_type or prev_label == 'I-' + entity_type):
                        label_list[k] = 'B-' + entity_type

        if i < 4:
            print("- Labels after encoding the entities: ", label_list)

        label_ids = label_encoder.transform(label_list)
        tokens.append(tokenized_input.input_ids.numpy()[0])
        labels.append(label_ids)

        if i < 4:
            print("- Label IDs", label_ids)

    print("\n// Encoding completed")
    return np.array(tokens), np.array(labels)


def get_ROC_curve(true_labels, logits, unique_labels):
    n_labels = len(unique_labels)
    y_true = true_labels.flatten()
    
    # Binarize real classes for ROC calculation (One-vs-Rest)
    y_true_binarized = label_binarize(y_true, classes=range(n_labels)) #  0, 1, 2, ..., n_labels-1

    # Moving from logits to probabilities via a softmax
    probabilities = tf.nn.softmax(logits, axis=-1).numpy()  # shape (N, seq_len, n_labels)
    probabilities = probabilities.reshape(-1, n_labels)     # shape (N*seq_len, n_labels)

    # Calculate fpr, tpr and AUC for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    for i in range(n_labels):
        fpr[i], tpr[i], _ = roc_curve(y_true_binarized[:, i], probabilities[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Calcul of the micro-average of all classes
    fpr["micro"], tpr["micro"], _ = roc_curve(y_true_binarized.ravel(), probabilities.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    plt.figure(figsize=(8, 6))
    plt.plot(
        fpr["micro"], tpr["micro"],
        label="Micro-average ROC (AUC = {0:0.2f})".format(roc_auc["micro"]),
        color="deeppink", linestyle=":", linewidth=4
    )
    colors = cycle(["aqua", "darkorange", "cornflowerblue", "green", "red", "purple"])
    for (i, color) in zip(range(n_labels), colors):
        plt.plot(
            fpr[i], tpr[i], color=color, lw=2,
            label="Classe '{0}' (AUC = {1:0.2f})".format(unique_labels[i], roc_auc[i])
        )

    print("\nROC multiclasses curve:")
    plt.plot([0, 1], [0, 1], "k--", lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("Taux de Faux Positifs (FPR)")
    plt.ylabel("Taux de Vrais Positifs (TPR)")
    plt.title("ROC multiclasses")
    plt.legend(loc="lower right")
    plt.show()


def get_metrics(true_labels, predicted_labels, unique_labels, history=None):
    cm = confusion_matrix(true_labels, predicted_labels)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] # normalisation

    print("\nConfusion Matrix %:")
    # Heatmap
    plt.figure(figsize=(10, 7))
    custom_palette = ["#DCDED6", "#CED0C3", "#B4BAB1", "#859393", "#5D726F", "#485665"]
    ax = sns.heatmap(cm_normalized, annot=True, fmt=".2f", cmap=custom_palette, xticklabels=unique_labels, yticklabels=unique_labels, square=True, linewidths=2, linecolor='white')
    plt.title('Confusion Matrix', fontsize=16, fontweight='bold')
    plt.ylabel('True Label', fontsize=12, fontweight='bold')
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.xticks(fontsize=10, fontweight='normal')
    plt.yticks(fontsize=10, fontweight='normal')

    # color based on value
    for text in ax.texts:
        t = float(text.get_text())
        if 0.1 <= t < 0.7:
            text.set_color('#CA3C66')
        elif t >= 0.7:
            text.set_color('#FFFFFF')
        else:
            text.set_color('#485665')

    plt.show()

    # Confusion Matrix stdout
    print("\nConfusion Matrix:")
    print(cm)
    # Classification Report stdout
    print("\nClassification Report:")
    print(classification_report(true_labels, predicted_labels, target_names=unique_labels))
    
    # History
    print("\nEvolution of accuracy and loss over the epoch:")
    if history is not None:
        # accuracy
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'], label='Training accuracy', marker='o')
        plt.plot(history.history['val_accuracy'], label='Validation accuracy', marker='o')
        plt.title('Model accuracy over epochs')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
        # loss
        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'], label='Training loss', marker='o')
        plt.plot(history.history['val_loss'], label='Validation loss', marker='o')
        plt.title('Model loss over epochs')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()

        plt.tight_layout()
        plt.show()


def get_metrics_simple(true_labels, predicted_labels, unique_labels):
    # Confusion Matrix stdout
    confusion = confusion_matrix(true_labels, predicted_labels)
    print("\nConfusion Matrix")
    print(confusion)

    # Confusion Matrix 2 stdout
    confusion_normalized = confusion.astype('float') / confusion.sum(axis=1)[:, np.newaxis]
    confusion_normalized_rounded = np.around(confusion_normalized, decimals=2)
    print("\nConfusion Matrix 2")
    print(confusion_normalized_rounded)

    # Classification Report stdout
    print("\nClassification Report:")
    print(classification_report(true_labels, predicted_labels, target_names=unique_labels))