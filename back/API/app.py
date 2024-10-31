from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from dijkstra import dijkstra
import pathfinder
from pydub import AudioSegment
import speech_recognition as sr

from predict_departure_and_destination import process_sentence

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5000/api/v1/"}})


travelInfo = []


@app.route("/api/v1/travel", methods=["POST"])
def travel():
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
        result = process_sentence(1, text)
        print("ttttt")
        print(result)
        print(result["Departure"])
        print(result["Destination"])

        travelInfo.append(result)
        return jsonify({'result': result}), 200
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/v1/shortest-path", methods=["GET"])
def shortest_path():
   
    start_node = 'Gare de Brest'
    end_node = 'Gare de Lyon-Perrache'
    graph = pathfinder.load_graph()
    path, distance = dijkstra(graph, start_node, end_node)

    return jsonify({
        "path": path,
        "distance": distance
    })

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