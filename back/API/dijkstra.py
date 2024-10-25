import heapq


def dijkstra(graph, start, end):
    # Dictionnaire pour stocker la distance minimale de chaque nœud
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0  # La distance du point de départ à lui-même est 0

    # Priority queue pour les nœuds à explorer
    priority_queue = [(0, start)]  # (distance, node)

    # Dictionnaire pour garder une trace des chemins
    previous_nodes = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        # Si nous atteignons le nœud de destination, nous pouvons arrêter
        if current_node == end:
            break

        # Si la distance actuelle est supérieure à la distance enregistrée, on ignore
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # Seulement si la nouvelle distance est plus courte, on met à jour
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstructer le chemin à partir du dictionnaire des nœuds précédents
    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]

    path.reverse()  # On inverse le chemin pour avoir l'ordre correct
    print(path)
    return path, distances[end]  # Retourne le chemin et la distance totale
