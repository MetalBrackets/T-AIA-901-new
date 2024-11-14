import pandas as pd
from unidecode import unidecode
import json


def gareFinders(cityStart,cityEnd):
    file_path = "../../students_project/liste-des-gares.csv"
    data = pd.read_csv(file_path, delimiter=';')

    


    cityStartUpper = unidecode(cityStart[0].upper())
    cityEndUpper = unidecode(cityEnd[0].upper())

    gareStart =""
    gareEnd = ""



    gareStartList = []
    gareEndList = []

    for index, row in data.iterrows():
        if row['COMMUNE'] == cityStartUpper:
            gareStartList.append("Gare de " + row['LIBELLE'])
        if row['COMMUNE'] == cityEndUpper:
            gareEndList.append("Gare de " + row['LIBELLE'])


    gareStartList = list(set(gareStartList))
    gareEndList = list(set(gareEndList))

    print(gareStartList)
    print(gareEndList)

    return json.dumps({"Departure":gareStart,"Destination":gareEnd})
    