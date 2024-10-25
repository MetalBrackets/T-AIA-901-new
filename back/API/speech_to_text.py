import speech_recognition as sr
from pydub import AudioSegment

def speech_to_text():
   
    # Convertion en format WAV si l'audio
    

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language='fr-FR')
        return jsonify({'text': text}), 200
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': str(e)}), 500