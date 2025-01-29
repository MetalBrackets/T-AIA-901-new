# T-AIA-901

## Information de projet

📁 [Repository](https://github.com/MetalBrackets/T-AIA-901-new)  
📁 [Mirror](https://github.com/EpitechMscProPromo2025/T-AIA-901-NAN_3)

## Front

### Install Dependencies

```
 cd /front
 npm install
```

### Start Project

```
npm run dev
```

## Back

### Setup Virtual Env

```
cd /back/API
python -m venv env
source env/Scripts/activate
source env/bin/activate

```

For notebook: Kernel -> choose Python 3.11

### Install Dependencies

```
pip install -r requirements.txt
```

/!\ windows, install executable ffmpeg-master-latest-win64-gpl.zip
: https://github.com/BtbN/FFmpeg-Builds/releases

### Start Project

```
python app.py
```

### The specifications of the NER classification model

- It receives a sentence as input
- It identifies the departure and destination
- For an invalid command it returns an information message  
  `Phrase ID, Code=['NOT_FRENCH', 'UNKNOWN', 'NOT_TRIP]`
- For a valid order it returns  
   `sentenceID, Departure, Destination`

```
 note :
- Relationships between words that can be at the beginning or end of a sequence
- understanding of a departure and an arrival (with waypoints in negative)
- understanding of compound nouns, e.g.: Port-Boulet
- differentiate a city from a first name, e.g.: Albert
```
