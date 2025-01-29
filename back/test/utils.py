
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf

def encode_data(data, tokenizer, label_encoder):
    tokens = []
    labels = []

    for i, row in data.iterrows():
        phrase = row['Phrase']
        dep = row['Départ']
        arr = row['Arrivée']

        tokenized_input = tokenizer.encode_plus(
            phrase,
            add_special_tokens=True,
            return_offsets_mapping=True,
            truncation=True,
            return_tensors="tf"
        )

        dep_positions = []
        arr_positions = []

        start = 0 # find all starting occurrences
        while True:
            idx = phrase.find(dep, start)
            if idx == -1:
                break
            dep_positions.append((idx, idx + len(dep)))
            start = idx + len(dep)

        start = 0 # find all arrival occurrences
        while True:
            idx = phrase.find(arr, start)
            if idx == -1:
                break
            arr_positions.append((idx, idx + len(arr)))
            start = idx + len(arr)

        tokenized_text = tokenizer.convert_ids_to_tokens(tokenized_input.input_ids[0])
        offsets = tokenized_input['offset_mapping'].numpy()[0]
        label_list = ['O'] * len(tokenized_text)

        for j, (offset_start, offset_end) in enumerate(offsets):   # attribution of labels to tokens
            if offset_start == 0 and offset_end == 0:
                continue  # padding token

            token_label = 'O'
            
            for entity_start, entity_end in dep_positions: # check if the token overlaps an arrival entity
                if offset_start >= entity_start and offset_end <= entity_end:
                    if offset_start == entity_start:
                        token_label = 'B-DEP'
                    else:
                        token_label = 'I-DEP'
                    break

            if token_label == 'O': # check if the token overlaps an arrival entity
                for entity_start, entity_end in arr_positions:
                    if offset_start >= entity_start and offset_end <= entity_end:
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

        label_ids = label_encoder.transform(label_list)
        tokens.append(tokenized_input.input_ids.numpy()[0])
        labels.append(label_ids)

    print("\n// Encoding completed")
    return np.array(tokens), np.array(labels)


def visualize_attention(text, model, tokenizer, model_name):
    print("\n/////////////////////////////////////////////////////////////////////////////////////////////////")
    print(f"\n---> Sentence: '{text}'")
    print(f"\nIci on voit sur quels tokens d'entrées {model_name} porte son attention pour chaque token de sortie. Pour produire son embedding.")
    # generate the outputs with the attentions
    inputs = tokenizer.encode_plus(text, return_tensors='tf')
    outputs = model(**inputs, output_attentions=True)
    attentions = outputs.attentions  # (num_layers, batch, num_heads, seq_len, seq_len)
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0].numpy())

    total_layers = len(attentions)
    # select the last 5 layers
    last_5_attentions = attentions[-5:]
    num_layers = len(last_5_attentions)

    # 1 heatmap par couche
    fig, axes = plt.subplots(1, num_layers, figsize=(4 * num_layers, 4))
    if num_layers == 1:
        axes = [axes]

    for layer_idx, layer_attention in enumerate(last_5_attentions):
        layer_attention = tf.squeeze(layer_attention, axis=0)  # (num_heads, seq_len, seq_len)
        layer_attention_mean = tf.reduce_mean(layer_attention, axis=0).numpy()

        ax = axes[layer_idx]
        sns.heatmap(
            layer_attention_mean, 
            xticklabels=tokens, 
            yticklabels=tokens, 
            cmap='viridis', 
            ax=ax
        )
        # The layer index here is relative to the last 5 layers
        absolute_layer_index = (len(attentions) - 5 + layer_idx + 1)
        ax.set_title(f'Layer {absolute_layer_index}', fontsize=12)
        ax.set_xlabel('Input Tokens', fontsize=10)
        ax.set_ylabel('Output Tokens', fontsize=10)
        # Label rotation
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

    fig.suptitle(f"Last 5 layers attention weights for {model_name}", fontsize=16)
    plt.tight_layout()
    plt.show()
    print("Nombre total de layers:", total_layers)
    print("Model summary:", model.summary())



def print_predict_duration(total_start_time, total_end_time):
    total_predict_duration = total_end_time - total_start_time
    seconds = int(total_predict_duration)
    milliseconds = (total_predict_duration - seconds) * 1000
    print(f"\n⏱️ Total prediction time: {seconds} seconds and {milliseconds:.2f} milliseconds")
    return total_predict_duration