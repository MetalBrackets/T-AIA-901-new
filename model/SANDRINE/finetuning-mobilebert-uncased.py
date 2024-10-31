import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import tensorflow as tf
from transformers import BertTokenizerFast, TFMobileBertForTokenClassification
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

tokenizer = BertTokenizerFast.from_pretrained('google/mobilebert-uncased', token=huggingface_token)

print("\n// Starting train data encoding...")
train_tokens, train_labels = encode_data(data_train, tokenizer, label_encoder, max_length=36)
print("\n// Starting test data encoding...")
test_tokens, test_labels = encode_data(data_test, tokenizer, label_encoder, max_length=36)

##################
# Model training #
##################

model = TFMobileBertForTokenClassification.from_pretrained(
    'google/mobilebert-uncased',
    num_labels=len(unique_labels),
    ignore_mismatched_sizes=True,
    token=huggingface_token
)
print("-> model loaded with ", len(unique_labels), "labels")

# configuration
optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

model.fit(train_tokens, train_labels, epochs=10, batch_size=9, validation_split=0.1) # training


##############
# Model Save #
##############

model_path = os.path.join(os.getcwd(), 'model', 'models', 'mobilebert-uncased')
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
# 2/2 [==============================] - 1s 358ms/step - loss: 1.1565 - accuracy: 0.8594
# Evaluation results: [1.1564723253250122, 0.8594104051589966]
# 2/2 [==============================] - 16s 357ms/step

# Confusion Matrix
# [[  18    1    1    0    0]
#  [   0   21    0    0    1]
#  [   0    0   57    2    5]
#  [   0    0    7   75    1]
#  [  30   28   95   77 1345]]

# Confusion Matrix 2
# [[0.9  0.05 0.05 0.   0.  ]
#  [0.   0.95 0.   0.   0.05]
#  [0.   0.   0.89 0.03 0.08]
#  [0.   0.   0.08 0.9  0.01]
#  [0.02 0.02 0.06 0.05 0.85]]

# Classification Report:
#               precision    recall  f1-score   support

#            O       0.38      0.90      0.53        20
#        B-DEP       0.42      0.95      0.58        22
#        I-DEP       0.36      0.89      0.51        64
#        B-ARR       0.49      0.90      0.63        83
#        I-ARR       0.99      0.85      0.92      1575

#     accuracy                           0.86      1764
#    macro avg       0.53      0.90      0.63      1764
# weighted avg       0.93      0.86      0.88      1764

