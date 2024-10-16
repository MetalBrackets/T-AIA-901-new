# Module NLP NER

### Lancer le Jupiter Notebook

```sh
docker-compose up

# go to http://localhost:8888/lab

```

Kernel : choose Python 3.x

### Les spec du model de classification NER

- Il reçois en entrée une phrase
- Il identifie le départ et la destination
- Pour une commande non valide il retourne un message d'information  
  `sentence ID, Code=['NOT_FRENCH', 'UNKNOWN', 'NOT_TRIP]`
- Pour une commande valide il retourne  
   `sentenceID, Departure, Destination`

```
 note :
- Relations entre les mots qui peuvent être au début ou à la fin d'une séquence
- compréhention d'un départ et d'une arrivée (met les waypoint en negatif)
- compréhension des noms composés, ex : Port-Boulet
- différencier une ville d'un prénom, ex: Albert
```
