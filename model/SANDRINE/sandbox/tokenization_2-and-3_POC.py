##############################################
# This script 2 & 3 is used to tokenize data #
#############################################

import os
import json
import pandas as pd
from nltk.tokenize import RegexpTokenizer

# Access to csv
file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'reservation-first-dataset-train.csv')
absolute_file_path = os.path.abspath(file_path)
print(f"PATH : {absolute_file_path}")

# Tokenized with regex for french : 
# Tirst REGEX tested RegexpTokenizer(r"\b(?:d'|l'|j'|qu'|n'|s'|t'|m'|c')?\w+\b")
# Second REGEX tested for better results
tokenizer = RegexpTokenizer(r"\b(?:d'|l'|j'|qu'|n'|s'|t'|m'|c')\b|\b\w+\b")


def annotate_tokens(depart, arrivee, tokens):
    labels = ['O'] * len(tokens)
    depart_tokens = tokenizer.tokenize(depart)
    arrivee_tokens = tokenizer.tokenize(arrivee)

    def annotate_entity(entity_tokens, tag_prefix):
        if not entity_tokens:
            return  # exit if the list is empty
        
        start_index = 0
        while start_index < len(tokens):
            try:
                start_index = tokens.index(entity_tokens[0], start_index)
                if tokens[start_index:start_index+len(entity_tokens)] == entity_tokens:
                    labels[start_index] = f"B-{tag_prefix}"
                    for i in range(1, len(entity_tokens)):
                        labels[start_index + i] = f"I-{tag_prefix}"
                    start_index += len(entity_tokens)
                else:
                    start_index += 1
            except ValueError:
                break

    annotate_entity(depart_tokens, 'DEP')
    annotate_entity(arrivee_tokens, 'ARR')
    
    return labels

def process_csv(filepath):
    if not os.path.exists(filepath):
        print(f"Le fichier n'existe pas : {filepath}")
        return []

    df = pd.read_csv(filepath)
    annotated_data = []

    # To fill NaN values with '' in the title of the columns
    df.fillna({'Départ': '', 'Arrivée': ''}, inplace=True)

    for _, row in df.iterrows():
        tokens = tokenizer.tokenize(row['Phrase'])
        labels = annotate_tokens(row['Départ'], row['Arrivée'], tokens)
        annotated_data.append({"tokens": tokens, "labels": labels})
    
    return annotated_data

annotated_dataset = process_csv(absolute_file_path)

# Export JSON
# json_file_path = os.path.join(os.path.dirname(__file__), 'tokenized_2_POC.json') # First REGEX
json_file_path = os.path.join(os.path.dirname(__file__), 'tokenized_3_POC.json')

json_data = []
for data in annotated_dataset:
    json_data.append({
        'tokens': data['tokens'],
        'labels': data['labels']
    })

with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

print(f"Json dump in {json_file_path}")
