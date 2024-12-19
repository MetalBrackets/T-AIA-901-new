
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

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

        start = 0  # Trouver toutes les occurrences de départ
        while True:
            idx = phrase.find(dep, start)
            if idx == -1:
                break
            dep_positions.append((idx, idx + len(dep)))
            start = idx + len(dep)

        start = 0  # Trouver toutes les occurrences d'arrivée
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

        for j, (offset_start, offset_end) in enumerate(offsets):  # Attribution des labels aux tokens
            if offset_start == 0 and offset_end == 0:
                continue  # Token de padding
            token_label = 'O'

            # Vérifier si le token chevauche une entité de départ
            for entity_start, entity_end in dep_positions:
                if (offset_start >= entity_start) and (offset_end <= entity_end):
                    if offset_start == entity_start:
                        token_label = 'B-DEP'
                    else:
                        token_label = 'I-DEP'
                    break

            # Vérifier si le token chevauche une entité d'arrivée
            for entity_start, entity_end in arr_positions:
                if (offset_start >= entity_start) and (offset_end <= entity_end):
                    if offset_start == entity_start:
                        token_label = 'B-ARR'
                    else:
                        token_label = 'I-ARR'
                    break

            label_list[j] = token_label

        if i < 4:
            print("- Labels after encoding the entities: ", label_list)

        label_ids = label_encoder.transform(label_list)
        tokens.append(tokenized_input.input_ids.numpy()[0])
        labels.append(label_ids)

        if i < 4:
            print("- Label IDs", label_ids)

    print("\n// Encoding completed")
    return np.array(tokens), np.array(labels)


def get_metrics(true_labels, predicted_labels, unique_labels, history=None):
    cm = confusion_matrix(true_labels, predicted_labels)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] # normalisation

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