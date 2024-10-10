# Recherche pour tokenizer

## Phrases de test

```csv
# CSV
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
