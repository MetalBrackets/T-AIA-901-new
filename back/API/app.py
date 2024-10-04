from flask import Flask, jsonify, request
import folium

app = Flask(__name__)


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
def audio():
    data = request.get_json()
    audio = data['audio']
    return jsonify({'audio': audio}), 200


if __name__ == '__main__':
    app.run(debug=True)
