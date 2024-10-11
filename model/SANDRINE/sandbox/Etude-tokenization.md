# Recherche pour tokenizer

-> install

```
pip install tensorflow pandas numpy transformers
pip install pandas transformers sacremoses nltk
```

## Phrases

📄 utilisation du fichier reservation-first-dataset-train.csv

```csv
# ex :
Phrase,Départ,Arrivée
"j'aimerais voyager de Ailly-sur-Somme à Aix-les-Bains le Revard","Ailly-sur-Somme","Aix-les-Bains le Revard"
"quels trains voyagent d'Alençon à Corbeil-Essonnes","Alençon","Corbeil-Essonnes"
```

### Script 1

Tokenisation avec `word_tokenize` de `NLTK`  
-> utilise simplement str.split()  
**Problèmes**

- Les contractions comme "d'Alençon" ne sont pas gérées
- Ne trouve pas l'entité

```json
   {
    "tokens": ["j'aimerais", "voyager", "de", "Ailly-sur-Somme", "à", "Aix-les-Bains", "le", "Revard"],
    "labels": ["O", "O", "O", "B-DEP", "O", "B-ARR", "I-ARR", "I-ARR"]
  },
  {
    "tokens": ["quels", "trains", "voyagent", "d'Alençon", "à", "Corbeil-Essonnes"],
    "labels": ["O", "O", "O", "O", "O", "B-ARR"]
  }
```

### Script 2

Introduction d'un `RegexpTokenizer` personnalisé pour gérer les contractions françaises  
REGEX : `r"\b(?:d'|l'|j'|qu'|n'|s'|t'|m'|c')?\w+\b"`  
Ce tokenizer tokenise à la fois les phrases et les mots  
ex: Ailly-sur-Somme est découpé en 3 tokens

**Problèmes**

- Contractions non séparées (ex: "d'Alençon" est un seul token)
- Erreur d'annotation

```json
  {
    "tokens": ["j'aimerais", "voyager", "de", "Ailly", "sur", "Somme", "à", "Aix", "les", "Bains", "le", "Revard"],
    "labels": ["O", "O", "O", "B-DEP", "I-DEP", "I-DEP", "O", "B-ARR", "I-ARR", "I-ARR", "I-ARR", "I-ARR"]
  },
  {
    "tokens": ["quels", "trains", "voyagent", "d'Alençon", "à", "Corbeil", "Essonnes"],
    "labels": ["O", "O", "O", "O", "O", "B-ARR", "I-ARR"]
  }
```

### Script 3

Amélioration
REGEX : `r"\b(?:d'|l'|j'|qu'|n'|s'|t'|m'|c')\b|\b\w+\b"`

- Sépare les contractions en deux tokens distincts ("d'" et "Alençon")

Très bon résultat

```json
  {
    "tokens": ["j'", "aimerais", "voyager", "de", "Ailly", "sur", "Somme", "à", "Aix", "les", "Bains", "le", "Revard"],
    "labels": ["O", "O", "O", "O", "B-DEP", "I-DEP", "I-DEP", "O", "B-ARR", "I-ARR", "I-ARR", "I-ARR", "I-ARR"]
  },
  {
    "tokens": ["quels", "trains", "voyagent", "d'", "Alençon", "à", "Corbeil", "Essonnes"],
    "labels": ["O", "O", "O", "O", "B-DEP", "O", "B-ARR", "I-ARR"]
  }
```

### Script 4

Observer la sortie des tokenizeurs entrainés sur du fr avec des lib d'Hugging Face. Le pipeline NER ne peut pas deviner par lui même le départ et l'arrivé sans être entrainé sur les données.

Chaque tokenizeur a sa propre stratégie de segmentation :

- CamemBERT et FlauBERT -> optimisés pour le français / conserver les mots entiers
- BERT français -> segmentation très fine
- BERT multilingue -> flexibilité linguistique mais peut sacrifier certaines spécificités

CamemBERT :

- Sépare "d" et l'apostrophe
- Utilise "▁" pour indiquer le début d'un nouveau mot

FlauBERT :

- Garde "d'" ensemble
- Utilise "</w>" pour indiquer la fin d'un mot
  Les traits d'union sont généralement tokenisés comme des tokens séparés ou utilisés pour segmenter les mots.
  Indicateurs de sous-mots :

BERT français et BERT multilingue :

- Utilisent "##" pour indiquer que le token est une continuation du précédent

```json
{
  "Phrase": "quels trains voyagent d'Alençon à Corbeil-Essonnes",
  "Départ": "Alençon",
  "Arrivée": "Corbeil-Essonnes",
  "Tokens": {
    "camembert-base": ["▁quels", "▁trains", "▁voyage", "nt", "▁d", "'", "Al", "en", "çon", "▁à", "▁Corb", "e", "il", "-", "Essonne", "s"],
    "flaubert/flaubert_base_cased": ["quels</w>", "trains</w>", "voyagent</w>", "d'</w>", "Alençon</w>", "à</w>", "Cor", "be", "il-", "Ess", "onnes</w>"],
    "dbmdz/bert-base-french-europeana-cased": ["quels", "trains", "voyage", "##nt", "d", "'", "Alençon", "à", "Corbeil", "-", "Ess", "##onnes"],
    "bert-base-multilingual-cased": ["quel", "##s", "trains", "voyage", "##nt", "d", "'", "Ale", "##nç", "##on", "à", "Cor", "##bei", "##l", "-", "Essonne", "##s"]
  }
}
```

#### Entrainement d'un modèle

🚧 chantier est en court  
Pour qu'il puisse predir le départ et l'arrivé avec le sens de la phrase.

## Conclusion

🚧 en cours ..  
Le script 3 qui est performant avec une approche simple sans entrainement de modèle.
La tokenization avec la lib python NLTK est basé sur une REGEX qui prend en compte les contractions du français (d'|l'|j'|qu'|n'|s'|t'|m'|c'). Cette méthode détecte correctement les entity (Départ, Arrivée) dans une forme naturelle des mots sans les sur-fragmenter en sous-tokens, comme le font les tokenizers de modèles pré-entraînés. De plus le format BIO (Begin, Inside, Outside) est plus lisible pour l'évaluation humaine.

L'utilisation d'un modèle finetuné 🚧 en cours ..
