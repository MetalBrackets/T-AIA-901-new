
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def encode_data(data, tokenizer, label_encoder):
    tokens = []
    labels = []

    for i, row in data.iterrows():
        phrase = row['Phrase']
        dep = row['Départ']
        arr = row['Arrivée']

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
            truncation=True,
            return_tensors="tf"
        )

        tokenized_text = tokenizer.convert_ids_to_tokens(tokenized_input.input_ids[0])
        offsets = tokenized_input['offset_mapping'].numpy()[0]
        label_list = ['O'] * len(tokenized_text)

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

        label_ids = label_encoder.transform(label_list)
        tokens.append(tokenized_input.input_ids.numpy()[0])
        labels.append(label_ids)

    print("\n// Encoding completed")
    return np.array(tokens), np.array(labels)


# def visualize_attention_heatmap(attention, tokens, model_name):
#     plt.figure(figsize=(6, 5))
#     sns.heatmap(attention, xticklabels=tokens, yticklabels=tokens, cmap='viridis')
#     plt.title(f'Attention weights for {model_name}')
#     plt.xlabel('Input Tokens')
#     plt.ylabel('Output Tokens')

#     plt.show()


def print_predict_duration(total_start_time, total_end_time):
    total_predict_duration = total_end_time - total_start_time
    seconds = int(total_predict_duration)
    milliseconds = (total_predict_duration - seconds) * 1000
    print(f"\n⏱️ Total prediction time: {seconds} seconds and {milliseconds:.2f} milliseconds")
    return total_predict_duration