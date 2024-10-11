import os
import pandas as pd
from sklearn.model_selection import train_test_split

#####################
# Préparation des Données
######################

# Access to csv
file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'reservation-first-dataset-train.csv')
absolute_file_path = os.path.abspath(file_path)

# Load the data
data = pd.read_csv(absolute_file_path)
data = data.fillna('') # for possible NaN values

sentences = []
tags = []

for idx, row in data.iterrows():
    phrase = row['Phrase']
    depart = row['Départ']
    arrivee = row['Arrivée']
    
    words = phrase.split()
    tag_sequence = []

    for word in words:
        if word in depart.split():
            tag_sequence.append("B-Départ")
        elif word in arrivee.split():
            tag_sequence.append("B-Arrivée")
        else:
            tag_sequence.append("O")
    
    sentences.append(words)
    tags.append(tag_sequence)

# Split data into train and test sets
train_sentences, val_sentences, train_tags, val_tags = train_test_split(sentences, tags, test_size=0.1)


#####################
# Tokenisation et Préparation des Données
#####################

from transformers import AutoTokenizer
import tensorflow as tf

# Utiliser CamemBERT comme exemple
tokenizer = AutoTokenizer.from_pretrained('camembert-base')

label_list = ["O", "B-Départ", "B-Arrivée"]
label_to_id = {label: i for i, label in enumerate(label_list)}

def tokenize_and_align_labels(sentences, tags):
    tokenized_inputs = tokenizer(sentences, truncation=True, padding=True, is_split_into_words=True, return_tensors="tf")
    labels = []

    for i, label in enumerate(tags):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        label_ids = []
        previous_word_idx = None

        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)  # Ignore special tokens
            elif word_idx != previous_word_idx:
                label_ids.append(label_to_id[label[word_idx]])
            else:
                label_ids.append(-100)  # Ignorer les sous-tokens
            previous_word_idx = word_idx

        labels.append(label_ids)

    tokenized_inputs["labels"] = tf.constant(labels)
    return tokenized_inputs

train_tokenized = tokenize_and_align_labels(train_sentences, train_tags)
val_tokenized = tokenize_and_align_labels(val_sentences, val_tags)



#########################
# Construction et Entraînement du Modèle TensorFlow
##########################

from transformers import TFAutoModelForTokenClassification
from transformers import create_optimizer
import tensorflow_addons as tfa

# Charger un modèle pré-entraîné adapté pour la classification des tokens
model = TFAutoModelForTokenClassification.from_pretrained('camembert-base', num_labels=len(label_list))

# Optimizer et Schedule de l'apprentissage
batch_size = 8
num_train_steps = len(train_tokenized["input_ids"]) // batch_size * 3  # 3 epochs
num_warmup_steps = num_train_steps // 10

optimizer, schedule = create_optimizer(init_lr=2e-5, num_train_steps=num_train_steps, num_warmup_steps=num_warmup_steps)

model.compile(optimizer=optimizer, loss=model.compute_loss, metrics=['accuracy'])

# Préparer les datasets TensorFlow
train_dataset = tf.data.Dataset.from_tensor_slices((dict(train_tokenized), train_tokenized["labels"]))
val_dataset = tf.data.Dataset.from_tensor_slices((dict(val_tokenized), val_tokenized["labels"]))

train_dataset = train_dataset.shuffle(100).batch(batch_size).prefetch(tf.data.AUTOTUNE)
val_dataset = val_dataset.batch(batch_size).prefetch(tf.data.AUTOTUNE)

# Entraîner le modèle
history = model.fit(train_dataset, validation_data=val_dataset, epochs=3)


###################################
# Évaluation du Modèle
################################

import numpy as np

# Prédire sur le jeu de validation
predictions = model.predict(val_dataset)
predictions = np.argmax(predictions.logits, axis=-1)

true_labels = [[label_list[label] for label in labels if label != -100] for labels in val_tokenized["labels"]]
predicted_labels = [[label_list[p] for (p, l) in zip(prediction, labels) if l != -100] for prediction, labels in zip(predictions, val_tokenized["labels"])]

# Afficher un rapport de classification
from sklearn.metrics import classification_report
print(classification_report(true_labels, predicted_labels))
