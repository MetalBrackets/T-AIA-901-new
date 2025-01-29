import pandas as pd
from unidecode import unidecode
import json


def gareFinders(cityStart, cityEnd):
    try:
        file_path = "../../data/liste-des-gares.csv"
        data = pd.read_csv(file_path, delimiter=';')
    except FileNotFoundError:
        return "Error: The file liste-des-gares.csv was not found."
    except pd.errors.EmptyDataError:
        return "Error: The file liste-des-gares.csv is empty."
    except Exception as e:
        return f"Error: An unexpected error occurred while reading liste-des-gares.csv: {e}"

    cityStartUpper = unidecode(cityStart[0].upper())
    cityEndUpper = unidecode(cityEnd[0].upper())

    gareStartList = []
    gareEndList = []

    for index, row in data.iterrows():
        if row['COMMUNE'] == cityStartUpper:
            gareStartList.append("Gare de " + row['LIBELLE'])
        if row['COMMUNE'] == cityEndUpper:
            gareEndList.append("Gare de " + row['LIBELLE'])

    if not gareStartList:
        return f"Error: No stations found for the starting city {cityStart}."
    if not gareEndList:
        return f"Error: No stations found for the ending city {cityEnd}."

    try:
        file_path = "../../data/timetables.csv"
        dataTravel = pd.read_csv(file_path, delimiter='\t')
    except FileNotFoundError:
        return "Error: The file timetables.csv was not found."
    except pd.errors.EmptyDataError:
        return "Error: The file timetables.csv is empty."
    except Exception as e:
        return f"Error: An unexpected error occurred while reading timetables.csv: {e}"

    gareStartListExist = []
    gareEndListExist = []

    for _, row in dataTravel.iterrows():
        travel = row["trajet"]
        departure_station, arrival_station = travel.rsplit(" - ", 1)
        if departure_station in gareStartList:
            gareStartListExist.append(departure_station)
        if arrival_station in gareEndList:
            gareEndListExist.append(arrival_station)

    gareStartList = list(set(gareStartListExist))
    gareEndList = list(set(gareEndListExist))

    if not gareStartList:
        return f"Error: No valid starting stations found for the city {cityStart}."
    if not gareEndList:
        return f"Error: No valid ending stations found for the city {cityEnd}."

    trajects = []

    for gareStart in gareStartList:
        for gareEnd in gareEndList:
            trajects.append(f"{gareStart} - {gareEnd}")

    return trajects
