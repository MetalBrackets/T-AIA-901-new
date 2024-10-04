# Datas

## Dataset pour le(s) modèle(s) NLP de catégorisation (ner)

**Création des datasets**

- `reservation-first-dataset-train`
- `reservation-first-dataset-test`

**Objectif**  
Entrainer et tester un modèle à reconnaitre une ville de départ et d'arrivée dans un texte transcrit pas le module speech-to-text.

**Les étapes de fabrication**

- Utilisation du dataset [ATIS Airline Travel Information System](https://www.kaggle.com/datasets/hassanamin/atis-airlinetravelinformationsystem?resource=download)
- Filtrage dans excel : récupération uniquement des phrases labéllisées _atis_flight_
- Traduction dans Sheet : fonction google translate
- Nettoyage : utilisation de ChatGPT pour transformer avion en train. Remplacement des noms des villes américaines par des villes prisent aléatoirement dans le dataset `gare-de-voyageurs`  
   ✏️ Le format markdown évite les problèmes de caractères spéciaux
- Catégorisation : Chaque ligne à la main car les différentes tentatives de prompt n'ont pas données la qualité de réponse pour la catégorisation des villes d'arrivée et de départ
