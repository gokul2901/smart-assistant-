import io
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import pyttsx3

def speech_to_text():
    try:
        samplerate = 16000  # 16kHz sample rate
        duration = 5        # Record for 5 seconds
        
        # Record audio from the default microphone
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()  # Wait until the recording is complete
        
        # Convert the recorded numpy array to a WAV file in memory
        wav_io = io.BytesIO()
        sf.write(wav_io, audio_data, samplerate, format='WAV', subtype='PCM_16')
        wav_io.seek(0)
        
        # Use SpeechRecognition with the in-memory WAV file
        r = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio = r.record(source)
            
        text = r.recognize_google(audio)
        return text
    except Exception as e:
        return f"Error: {str(e)}"

def text_to_speech(text):
    try:
        # Clean text of markdown formatting for better speech output
        clean_text = text.replace("**", "").replace("*", "").replace("`", "").replace("RS", "Rupees")
        engine = pyttsx3.init()
        engine.say(clean_text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")