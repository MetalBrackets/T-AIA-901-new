import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import tensorflow as tf
from transformers import MobileBertTokenizerFast, TFMobileBertForTokenClassification
from sklearn.preprocessing import LabelEncoder
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
from dotenv import load_dotenv
from utils import encode_data, get_metrics


load_dotenv()
huggingface_token = os.environ.get('HUGGINGFACEHUB_API_TOKEN')
if not huggingface_token:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN n'a pas été trouvé -> vérifier le .env")


train_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'reservation-first-dataset-train.csv')
test_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'reservation-first-dataset-test.csv')
absolute_train_path = os.path.abspath(train_path)
absolute_test_path = os.path.abspath(test_path)
print(f"absolute_train_path: {absolute_train_path}")
print(f"absolute_test_path: {absolute_test_path}")

data_train = pd.read_csv(absolute_train_path).fillna('')
data_test = pd.read_csv(absolute_test_path).fillna('')

print("\n// Preparation of labels ['O', 'B-DEP', 'I-DEP', 'B-ARR', 'I-ARR']")
unique_labels = ['O', 'B-DEP', 'I-DEP', 'B-ARR', 'I-ARR']
label_encoder = LabelEncoder()
label_encoder.fit(unique_labels)
print("-> mapping labels and ids: ", {label: idx for idx, label in enumerate(label_encoder.classes_)})

tokenizer = MobileBertTokenizerFast.from_pretrained('SKNahin/NER_MobileBert', token=huggingface_token)

print("\n// Starting train data encoding...")
train_tokens, train_labels = encode_data(data_train, tokenizer, label_encoder, max_length=36)
print("\n// Starting test data encoding...")
test_tokens, test_labels = encode_data(data_test, tokenizer, label_encoder, max_length=36)

##################
# Model training #
##################

model = TFMobileBertForTokenClassification.from_pretrained(
    'SKNahin/NER_MobileBert',
    num_labels=len(unique_labels),
    ignore_mismatched_sizes=True,
    token=huggingface_token
)
print("-> model loaded with ", len(unique_labels), "labels")

# configuration
optimizer = tf.keras.optimizers.Adam(learning_rate=2e-5)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

model.fit(train_tokens, train_labels, epochs=10, batch_size=9, validation_split=0.1) # training

##############
# Model Save #
##############

model_path = os.path.join(os.getcwd(), 'model', 'models', 'NER_MobileBert')
absolute_model_path = os.path.abspath(model_path)
print(f"Path : {absolute_model_path}")

model.save_pretrained(absolute_model_path)  # model
tokenizer.save_pretrained(absolute_model_path)  # tokenizer

####################
# Model Evaluation #
####################
evaluation_results = model.evaluate(test_tokens, test_labels)
print("Evaluation results:", evaluation_results)

test_predictions = model.predict(test_tokens).logits
predicted_labels = np.argmax(test_predictions, axis=-1).flatten()
true_labels = test_labels.flatten() 

get_metrics(true_labels, predicted_labels, unique_labels)


# -> model loaded with  5 labels
# Epoch 1/10

# WARNING:tensorflow:From C:\Users\devme\AppData\Local\Programs\Python\Python311\Lib\site-packages\tf_keras\src\engine\base_layer_utils.py:384: The name tf.executing_eagerly_outside_functions is deprecated. Please use tf.compat.v1.executing_eagerly_outside_functions instead.

# 21/21 [==============================] - 134s 1s/step - loss: 4573.0898 - accuracy: 0.0989 - val_loss: 2.3426 - val_accuracy: 0.2725
# Epoch 2/10
# 21/21 [==============================] - 15s 703ms/step - loss: 1.7466 - accuracy: 0.4619 - val_loss: 1.2459 - val_accuracy: 0.6601
# Epoch 3/10
# 21/21 [==============================] - 14s 677ms/step - loss: 1.1865 - accuracy: 0.6829 - val_loss: 1.0663 - val_accuracy: 0.7130
# Epoch 4/10
# 21/21 [==============================] - 13s 632ms/step - loss: 1.0742 - accuracy: 0.7004 - val_loss: 0.9543 - val_accuracy: 0.7130
# Epoch 5/10
# 21/21 [==============================] - 16s 742ms/step - loss: 0.9737 - accuracy: 0.7050 - val_loss: 0.8784 - val_accuracy: 0.7288
# Epoch 6/10
# 21/21 [==============================] - 13s 621ms/step - loss: 0.9227 - accuracy: 0.7085 - val_loss: 0.8398 - val_accuracy: 0.7275
# Epoch 7/10
# 21/21 [==============================] - 14s 658ms/step - loss: 0.8836 - accuracy: 0.7204 - val_loss: 0.8072 - val_accuracy: 0.7302
# Epoch 8/10
# 21/21 [==============================] - 13s 609ms/step - loss: 0.8613 - accuracy: 0.7189 - val_loss: 0.7878 - val_accuracy: 0.7368
# Epoch 9/10
# 21/21 [==============================] - 14s 655ms/step - loss: 0.8401 - accuracy: 0.7303 - val_loss: 0.7710 - val_accuracy: 0.7394
# Epoch 10/10
# 21/21 [==============================] - 17s 742ms/step - loss: 0.8265 - accuracy: 0.7291 - val_loss: 0.7521 - val_accuracy: 0.7447
# 1/1 [==============================] - 0s 411ms/step - loss: 0.8357 - accuracy: 0.7361
# Evaluation results: [0.8357020616531372, 0.7361111044883728]
# 1/1 [==============================] - 12s 12s/step

# Confusion Matrix      
# [[  0   1   3   3  13]
#  [  2   0   4   3  13]
#  [  0   5   4  16  39]
#  [  2   1   8  25  47]
#  [  0   0  15  15 501]]

# Confusion Matrix 2
# [[0.   0.05 0.15 0.15 0.65]
#  [0.09 0.   0.18 0.14 0.59]
#  [0.   0.08 0.06 0.25 0.61]
#  [0.02 0.01 0.1  0.3  0.57]
#  [0.   0.   0.03 0.03 0.94]]

# Classification Report:
#               precision    recall  f1-score   support

#            O       0.00      0.00      0.00        20
#        B-DEP       0.00      0.00      0.00        22
#        I-DEP       0.12      0.06      0.08        64
#        B-ARR       0.40      0.30      0.34        83
#        I-ARR       0.82      0.94      0.88       531

#     accuracy                           0.74       720
#    macro avg       0.27      0.26      0.26       720
# weighted avg       0.66      0.74      0.69       720

