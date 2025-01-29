import pandas as pd
from collections import defaultdict


# Charger le fichier CSV et construire le graphe
def load_graph():
    file_path = "../../data/timetables.csv"
    data = pd.read_csv(file_path, delimiter='\t')
    graph = defaultdict(dict)

    for _, row in data.iterrows():
        travel = row["trajet"]
        duration = int(row["duree"])
        departure_station, arrival_station = travel.rsplit(" - ", 1)
        graph[departure_station][arrival_station] = duration
        graph[arrival_station][departure_station] = duration  # Ajout de la connexion inverse

    return graph

