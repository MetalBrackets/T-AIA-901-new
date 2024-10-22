import os
import tensorflow as tf
from transformers import TFBertForTokenClassification, BertTokenizerFast
from transformers import MobileBertTokenizerFast, TFMobileBertForTokenClassification
from sklearn.preprocessing import LabelEncoder
from langdetect import detect
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0' 

model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'model', 'models', 'bert-base-fr-cased')
absolute_model_path = os.path.abspath(model_path)
print(f"Absolute path: {absolute_model_path}")
tokenizer = BertTokenizerFast.from_pretrained(absolute_model_path)
model = TFBertForTokenClassification.from_pretrained(absolute_model_path)

# model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'model', 'models', 'NER_MobileBERT')
# absolute_model_path = os.path.abspath(model_path)
# print(f"Absolute path: {absolute_model_path}")
# tokenizer = MobileBertTokenizerFast.from_pretrained(absolute_model_path)
# model = TFMobileBertForTokenClassification.from_pretrained(absolute_model_path)

unique_labels = ['O', 'B-DEP', 'I-DEP', 'B-ARR', 'I-ARR']
label_encoder = LabelEncoder()
label_encoder.fit(unique_labels)

def is_french(text):
    try:
        return detect(text) == 'fr'
    except:
        return False

def extract_entities(phrase, max_length=36):
    """Extract departure and arrival entities from the phrase"""
    print("\n- Processing sentence: ", phrase)
    tokenized_input = tokenizer(phrase, return_offsets_mapping=True, add_special_tokens=True, return_tensors="tf", truncation=True, max_length=max_length)
    tokens = tokenizer.convert_ids_to_tokens(tokenized_input.input_ids[0])
    print("\n- Encoded tokens: ", tokens)

    offsets = tokenized_input['offset_mapping'].numpy()[0]
    predictions = model(tokenized_input.input_ids).logits
    label_indices = tf.math.argmax(predictions, axis=-1).numpy()[0]

    predicted_labels = label_encoder.inverse_transform(label_indices)
    print("\n- Labels after encoding the entities: ", predicted_labels)
    
    departure, arrival = [], []
    current_entity = []
    current_label = None

    for token, label, (start, end) in zip(tokens, predicted_labels, offsets):
        if 'B-' in label:
            if current_entity:
                if current_label == 'B-DEP':
                    departure.append(''.join(current_entity))
                elif current_label == 'B-ARR':
                    arrival.append(''.join(current_entity))
            current_entity = [token.replace("##", "")]
            current_label = label
        elif 'I-' in label and current_entity:
            current_entity.append(token.replace("##", ""))
        else:
            if current_entity:
                if current_label == 'B-DEP':
                    departure.append(''.join(current_entity))
                elif current_label == 'B-ARR':
                    arrival.append(''.join(current_entity))
            current_entity = []
            current_label = None

    print(f"\n- Detected Departure: {departure}")
    print(f"- Detected Arrival: {arrival}")

    return departure, arrival

def process_sentence(sentence_id, new_phrase):
    """Process the sentence to extract travel related information"""
    if not is_french(new_phrase):
        return {'sentenceID': sentence_id, 'Code': 'NOT_FRENCH'}

    departure, arrival = extract_entities(new_phrase)
    if not departure and not arrival:
        return {'sentenceID': sentence_id, 'Code': 'UNKNOWN'}
    if not departure or not arrival:
        return {'sentenceID': sentence_id, 'Code': 'NOT_TRIP'}

    return {'sentenceID': sentence_id, 'Departure': departure, 'Destination': arrival}

# Example usage
new_phrase = "demain, je planifie un voyage de Saint-Germain-en-Laye à L'Haÿ-les-Roses, en passant prendre des amis à Asnières-sur-Seine et peut-être faire une halte à Vitry-sur-Seine pour le déjeuner"
# new_phrase = "Tomorrow I'm planning a trip from Saint-Germain-en-Laye to L'Haÿ-les-Roses, picking up friends in Asnières-sur-Seine and maybe stopping in Vitry-sur-Seine for lunch"
# new_phrase = "J'aimerais aller à Londres"
result = process_sentence(1, new_phrase)
print(result)

