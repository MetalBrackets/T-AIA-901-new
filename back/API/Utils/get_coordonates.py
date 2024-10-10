import os
import pandas as pd

# Access the CSV file
file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'liste-des-gares.csv')
absolute_file_path = os.path.abspath(file_path)
print(f"/// PATH : {absolute_file_path}")

# Load station data
def load_station_data():
    df = pd.read_csv(absolute_file_path, delimiter=';')
    # Rename 'latitude' and 'longitude'
    df = df.rename(columns={'X_WGS84': 'longitude', 'Y_WGS84': 'latitude'})
    # Drop rows with missing values in latitude and longitude
    return df.dropna(subset=['latitude', 'longitude'])

# Fetch les coordonnées d'une ville
def get_coordinates(city_name, df):
    """ Fetch les coordinates for a given city from the dataframe"""
    if df is None:
        return None, None
    filtered_df = df[df['LIBELLE'].str.contains(city_name, case=False, na=False)]
    if not filtered_df.empty:
        lat = filtered_df.iloc[0]['latitude']
        lon = filtered_df.iloc[0]['longitude']
        return lat, lon
    else:
        print(f"No coordinates found for {city_name}")
        return None, None


# Example usage to test the script
df = load_station_data()
if df is not None:
    start_city = "Nantes"
    end_city = "Aixe-sur-Vienne"
    start_coords = get_coordinates(start_city, df)
    end_coords = get_coordinates(end_city, df)

    print(f"Start coordinates for {start_city}: {start_coords}")
    print(f"End coordinates for {end_city}: {end_coords}")
