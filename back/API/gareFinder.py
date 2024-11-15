import pandas as pd
from unidecode import unidecode
import json


def gareFinders(cityStart,cityEnd):
    file_path = "../../students_project/liste-des-gares.csv"
    data = pd.read_csv(file_path, delimiter=';')

    


    cityStartUpper = unidecode(cityStart[0].upper())
    cityEndUpper = unidecode(cityEnd[0].upper())

    gareStart = ""
    gareEnd = ""



    gareStartList = []
    gareEndList = []

    for index, row in data.iterrows():
        if row['COMMUNE'] == cityStartUpper:
            gareStartList.append("Gare de " + row['LIBELLE'])
        if row['COMMUNE'] == cityEndUpper:
            gareEndList.append("Gare de " + row['LIBELLE'])


    



    file_path = "../../students_project/timetables.csv"
    dataTravel = pd.read_csv(file_path, delimiter='\t')

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

    trajects = []

    for gareStart in gareStartList:
        for gareEnd in gareEndList:
            trajects.append(f"{gareStart} - {gareEnd}")
            
    return trajects
    