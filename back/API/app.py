from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from dijkstra import dijkstra
import pathfinder
from pydub import AudioSegment
import speech_recognition as sr

from predict_departure_and_destination import process_sentence
from gareFinder import gareFinders  

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5000/api/v1/"}})

travelInfo = []

@app.route("/api/v1/travel", methods=["POST"])
def travel():
    if 'audio' not in request.files:
        return jsonify({'error': 'Aucun fichier audio'}), 400
    
    audio_file = request.files['audio']
    if not audio_file:
        return jsonify({'error': 'Fichier audio invalide'}), 400

    try:
        audio = AudioSegment.from_file(audio_file, format="webm")
        audio.export('output.wav', format="wav")
    except Exception as e:
        return jsonify({'error': f'Impossible de convertir l\'audio'}), 400
    
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language='fr-FR')
    except sr.UnknownValueError:
        return jsonify({'error': 'Impossible de comprendre l\'audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f'Erreur de reconnaissance vocale'}), 500
    except Exception as e:
        return jsonify({'error': f'Erreur lors du traitement de l\'audio'}), 500

    try:
        result = process_sentence(1, text)
    except Exception as e:
        return jsonify({'error': f'Erreur lors du traitement de la phrase'}), 500

    try:
        traject = gareFinders(result["Departure"], result["Destination"])
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la recherche des gares'}), 500

    try:
        graph = pathfinder.load_graph()
    except Exception as e:
        return jsonify({'error': f'Erreur lors du chargement du graphe'}), 500

    full_path = []
    total_distance = 0
    travelInfo = []
    shortest_distance = 100000

    try:
        for i in range(len(traject) - 1):
            start_node = traject[i].split(" - ")[0]
            end_node = traject[i].split(" - ")[1]
            path, distance = dijkstra(graph, start_node, end_node)
            full_path.extend(path[:-1])  # Exclude the last node to avoid duplication
            full_path.append(traject[i].split(" - ")[1])
            
            if shortest_distance > distance:
                shortest_distance = distance
                travelInfo = ({
                    "start": traject[i].split(" - ")[0],
                    "end": traject[i].split(" - ")[1],
                    "path": full_path,
                    "distance": shortest_distance
                })
                full_path = []
            full_path = []
    except Exception as e:
        return jsonify({'error': f'Erreur lors du calcul du chemin'}), 500

    return jsonify(travelInfo), 200

@app.route("/api/v1/shortest-path", methods=["GET"])
def shortest_path():
    start_node = 'Gare de Brest'
    end_node = 'Gare de Lyon-Perrache'
    try:
        graph = pathfinder.load_graph()
        path, distance = dijkstra(graph, start_node, end_node)
    except Exception as e:
        return jsonify({'error': f'Erreur lors du calcul du chemin le plus court'}), 500

    return jsonify({
        "path": path,
        "distance": distance
    })

@app.route('/api/v1/audio', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({'error': 'Aucun fichier audio'}), 400

    audio_file = request.files['audio']
    if not audio_file:
        return jsonify({'error': 'Fichier audio invalide'}), 400

    try:
        audio = AudioSegment.from_file(audio_file, format="webm")
        audio.export('output.wav', format="wav")
    except Exception as e:
        return jsonify({'error': f'Impossible de convertir l\'audio'}), 400

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language='fr-FR')
    except sr.UnknownValueError:
        return jsonify({'error': 'Impossible de comprendre l\'audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f'Erreur de reconnaissance vocale'}), 500
    except Exception as e:
        return jsonify({'error': f'Erreur lors du traitement de l\'audio'}), 500

    return jsonify({'text': text}), 200

if __name__ == '__main__':
    app.run(debug=True)
