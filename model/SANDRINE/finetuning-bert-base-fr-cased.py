import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import tensorflow as tf
from transformers import BertTokenizerFast, TFBertForTokenClassification
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

tokenizer = BertTokenizerFast.from_pretrained('Geotrend/bert-base-fr-cased', token=huggingface_token)

print("\n// Starting train data encoding...")
train_tokens, train_labels = encode_data(data_train, tokenizer, label_encoder, max_length=36)
print("\n// Starting test data encoding...")
test_tokens, test_labels = encode_data(data_test, tokenizer, label_encoder, max_length=36)

##################
# Model training #
##################

model = TFBertForTokenClassification.from_pretrained(
    'Geotrend/bert-base-fr-cased', 
    num_labels=len(label_encoder.classes_), 
    token=huggingface_token
)
print("-> model loaded with ", len(label_encoder.classes_), "labels")

# configuration
optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

model.fit(train_tokens, train_labels, epochs=10, batch_size=9, validation_split=0.1) # training

##############
# Model Save #
##############
model_path = os.path.join(os.getcwd(), 'model', 'models', 'bert-base-fr-cased')
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



# 1/1 [==============================] - 1s 1s/step - loss: 0.1506 - accuracy: 0.9736
# Evaluation results: [0.15063849091529846, 0.9736111164093018]
# 1/1 [==============================] - 4s 4s/step

# Confusion Matrix:
# [[ 19   1   0   0   0]
#  [  1  20   0   1   0]
#  [  0   0  55   2   0]
#  [  0   0   5  76   0]
#  [  0   1   6   2 531]]

# Classification Report:
#               precision    recall  f1-score   support

#            O       0.95      0.95      0.95        20
#        B-DEP       0.91      0.91      0.91        22
#        I-DEP       0.83      0.96      0.89        57
#        B-ARR       0.94      0.94      0.94        81
#        I-ARR       1.00      0.98      0.99       540

#     accuracy                           0.97       720
#    macro avg       0.93      0.95      0.94       720
# weighted avg       0.98      0.97      0.97       720