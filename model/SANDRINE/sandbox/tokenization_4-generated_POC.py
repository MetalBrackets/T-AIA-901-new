import os
import pandas as pd
import json
from transformers import AutoTokenizer

# Access to csv
file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'reservation-first-dataset-train.csv')
absolute_file_path = os.path.abspath(file_path)

# Load the data
data = pd.read_csv(absolute_file_path)
data = data.fillna('') # for possible NaN values

# French tokenizers list to test
tokenizer_names = [
    'camembert-base',
    'flaubert/flaubert_base_cased',
    'dbmdz/bert-base-french-europeana-cased',
    'bert-base-multilingual-cased'  # inclut le français
]

# Load tokenizers
tokenizers = {name: AutoTokenizer.from_pretrained(name) for name in tokenizer_names}
results = []

# Iterate over the DataFrame
for idx, row in data.iterrows():
    phrase = row['Phrase']
    depart = row['Départ']
    arrivee = row['Arrivée']
    
    # Store the tokens of each tokenizer for the current phrase 
    tokens_per_tokenizer = {}
    evaluation_per_tokenizer = {}
    
    for name, tokenizer in tokenizers.items():
        tokens = tokenizer.tokenize(phrase)
        tokens_per_tokenizer[name] = tokens

    # Append in results
    results.append({
        'Phrase': phrase,
        'Départ': depart,
        'Arrivée': arrivee,
        'Tokens': tokens_per_tokenizer,
    })

# JSON dump
output_json_path = os.path.join(os.path.dirname(__file__), 'tokenized_4_POC_generation.json')
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)

print(f"Json dump in {output_json_path}")


