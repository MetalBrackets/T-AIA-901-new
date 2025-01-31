# T-AIA-901

## Projects

📁 [Repository](https://github.com/MetalBrackets/T-AIA-901-new)  
📁 [Mirror](https://github.com/EpitechMscProPromo2025/T-AIA-901-NAN_3)

## Launch the app

Front

```sh
# Install Dependencies
 cd /front
 npm install

 # Start Project
 npm run dev
```

Back

```sh
# Setup Virtual Env
cd /back/API
python -m venv env

# For Windows OS
source env/Scripts/activate

# For Linux OS or Venv
source env/bin/activate

# Install Dependencies
pip install -r requirements.txt

# For notebook: Kernel -> choose Python 3.11

# /!\ windows, install executable ffmpeg-master-latest-win64-gpl.zip
# https://github.com/BtbN/FFmpeg-Builds/releases

# Start Project
python app.py
```

### Speech to text

🔬 Voir le resultat de [l'étude comparative](./_documentation/etude_stt.md)

### The specifications of the NER classification model

- It receives a sentence as input
- It identifies the departure and destination
- For an invalid command it returns an information message  
  `Phrase ID, Code=['NOT_FRENCH', 'UNKNOWN', 'NOT_TRIP]`
- For a valid order it returns  
   `sentenceID, Departure, Destination`

```
 Note :
- Relationships between words that can be at the beginning or end of a sequence
- understanding of a departure and an arrival
- understanding of compound nouns, ex: Port-Boulet
- differentiate a city from a first name, ex: Albert
```

Choix du modèle final - Bert base fr  
🔬 Voir le resultat de [l'étude des entrainements des NER](./_documentation/etude_ner.md)
