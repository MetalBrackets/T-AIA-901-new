from flask import Flask, jsonify, request
import folium
import speech_recognition as sr
from flask_cors import CORS
from pydub import AudioSegment

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5000/api/v1/"}})


@app.route('/api/v1/travel', methods=['GET'])
def get_travel():
    travel = {
        "departure": "Paris",
        "arrival": "Nantes",
        "routes": [
            {
                "departure": "Paris Montparnasse",
                "arrival": "Nantes",
                "lat_departure": 48.8415,  # Latitude de la gare de départ
                "lon_departure": 2.3215,  # Longitude de la gare de départ
                "lat_arrival": 47.2184,  # Latitude de la gare d'arrivée
                "lon_arrival": -1.5536  # Longitude de la gare d'arrivée
            }
        ]
    }
    # Créer une carte avec Folium
    m = folium.Map(location=[(travel["routes"][0]["lat_departure"] + travel["routes"][0]["lat_arrival"]) / 2,
                             (travel["routes"][0]["lon_departure"] + travel["routes"][0]["lon_arrival"]) / 2],
                   zoom_start=8)
    # Ajouter un marqueur pour le départ
    folium.Marker(
        location=[travel["routes"][0]["lat_departure"], travel["routes"][0]["lon_departure"]],
        popup=f'Départ: {travel["routes"][0]["departure"]}',
        icon=folium.Icon(color='blue')
    ).add_to(m)

    # Ajouter un marqueur pour l'arrivée
    folium.Marker(
        location=[travel["routes"][0]["lat_arrival"], travel["routes"][0]["lon_arrival"]],
        popup=f'Arrivée: {travel["routes"][0]["arrival"]}',
        icon=folium.Icon(color='green')
    ).add_to(m)
    # Tracer une ligne entre les deux points
    folium.PolyLine(
        locations=[[travel["routes"][0]["lat_departure"], travel["routes"][0]["lon_departure"]],
                   [travel["routes"][0]["lat_arrival"], travel["routes"][0]["lon_arrival"]]],  # Ajout de la liste
        color='red',
    ).add_to(m)
    # Enregistrer la carte dans un fichier HTML
    m.save('map.html')
    print(travel)
    return jsonify(travel)


@app.route('/api/v1/audio', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file'}), 400

    audio_file = request.files['audio']
    # Convertion en format WAV si l'audio
    audio = AudioSegment.from_file(audio_file, format="webm")
    audio.export('output.wav', format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language='fr-FR')
        return jsonify({'text': text}), 200
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
