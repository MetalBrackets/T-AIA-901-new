import os
import pandas as pd
from geopy.distance import geodesic
from shapely.geometry import Point, LineString

# Access the CSV file
file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'liste-des-gares.csv')
absolute_file_path = os.path.abspath(file_path)
print(f"/// PATH : {absolute_file_path}")

# Load station data
def load_station_data():
    # Load data into a DataFrame
    df = pd.read_csv(absolute_file_path, delimiter=';')
    # Parse coordinates and filter all rows with missing values
    df['latitude'], df['longitude'] = zip(*df['position_geographique'].astype(str).map(parse_coordinates))
    return df.dropna(subset=['latitude', 'longitude'])

# Parse coordinates
def parse_coordinates(coord):
    """Convert coordinates to string -> tuple float (latitude, longitude)"""
    try:
        lat, lon = map(float, coord.split(','))
        return lat, lon
    except ValueError:
        return None, None  # if the string is poorly formatted

# Fetch les coordonnées d'une ville
def get_coordinates(city_name, df):
    """ Fetch les coordinates for a given city from the dataframe"""
    filtered_df = df[df['nom'].str.contains(city_name, case=False, na=False)]
    if not filtered_df.empty:
        position = filtered_df.iloc[0]['position_geographique']
        return parse_coordinates(position)
    else:
        print(f"No coordinates found for {city_name}")
        return None, None

def calculate_distance(start_coords, end_coords):
    """ Calculate the geodesic distance between two coordinates 
    """
    return geodesic(start_coords, end_coords).kilometers

def is_intermediate_station(row, start_coords, end_coords, max_distance=1):
    """ Determine if a station is intermediate based on its geographical position. """
    line = LineString([start_coords, end_coords])  # Line between start and end
    station_point = Point((row['latitude'], row['longitude']))  # Station point
    distance_to_line = station_point.distance(line) * 111  # Distance in km : 1° of longitude ≃ 111 km
    
    if distance_to_line > max_distance:
        return False
    
    # Check if the station is geographically between the start and end points
    lat_min, lat_max = sorted([start_coords[0], end_coords[0]])
    lon_min, lon_max = sorted([start_coords[1], end_coords[1]])
    return (lat_min <= row['latitude'] <= lat_max) and (lon_min <= row['longitude'] <= lon_max)

def get_intermediate_stations(df, start_coords, end_coords):
    """ Filter stations that qualify as intermediate based on defined criteria. """
    return df[df.apply(is_intermediate_station, args=(start_coords, end_coords), axis=1)]

# Example usage for test the script here
df = load_station_data()
start_city = "Nantes"
end_city = "Paris Montparnasse"
start_coords = get_coordinates(start_city, df)
end_coords = get_coordinates(end_city, df)

if start_coords and end_coords:
    intermediate_stations = get_intermediate_stations(df, start_coords, end_coords)
    print(intermediate_stations[['nom', 'latitude', 'longitude']])
else:
    print("Noms de villes invalides, vérifier les noms et réessayer")
