import speech_recognition as sr
import pyttsx3
import sounddevice as sd
import numpy as np
import time

# Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ',': '--..--', '.': '.-.-.-', '?': '..--..',
    '/': '-..-.', '-': '-....-', '(': '-.--.', ')': '-.--.-', '&': '.-...',
    ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-',
    '_': '..--.-', '"': '.-..-.', '@': '.--.-.', ' ': '/'
}

# Reverse Morse code dictionary
REVERSE_MORSE_CODE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}

def text_to_morse_code(text):
    return ' '.join(MORSE_CODE_DICT.get(char.upper(), '') for char in text)

def morse_code_to_text(morse_code):
    words = morse_code.split('   ')  # Morse code words are separated by 3 spaces
    decoded_message = ''
    for word in words:
        characters = word.split()  # Morse code characters are separated by 1 space
        decoded_message += ''.join(REVERSE_MORSE_CODE_DICT.get(char, '') for char in characters)
        decoded_message += ' '
    return decoded_message.strip()

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Sorry, there was an error with the request.")
            return None

# Function to convert text to speech
def text_to_speech(text, rate=150):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)  # Adjust speech rate (lower value for slower speech)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) 
    engine.say(text)
    engine.runAndWait()

def play_morse_code_sound(morse_code):
    frequency = 1000  # Frequency of the beep sound in Hertz
    dot_duration = 0.07  # Duration of a dot (in seconds)
    dash_duration = 0.25  # Duration of a dash (in seconds)
    
    intra_char_gap = 0.04  # Gap between elements (dots/dashes within the same character)
    inter_char_gap = 0.15  # Gap between characters
    word_gap = 0.4  # Gap between words
    
    sample_rate = 44100  # Sample rate for playback
    
    for symbol in morse_code:
        if symbol == '.':
            duration = dot_duration
        elif symbol == '-':
            duration = dash_duration
        elif symbol == ' ':
            time.sleep(inter_char_gap)  # Wait for gap between characters
            continue
        elif symbol == '/':  # Handling spaces between words
            time.sleep(word_gap)  # Wait for gap between words
            continue
        
        # Generate sound wave
        samples = (np.sin(2 * np.pi * np.arange(sample_rate * duration) * frequency / sample_rate)).astype(np.float32)
        
        # Play sound
        sd.play(samples, samplerate=sample_rate)
        sd.wait()  # Wait until sound is done playing

        # Wait for the intra-character gap after the sound
        time.sleep(intra_char_gap)

def morse_code_to_speech(morse_code):
    morse_speech = morse_code.replace('.', 'dot').replace('-', 'dash').replace(' ', ' ')
    text_to_speech(morse_speech, rate=125)  # Speak slower for Morse code

# Main functionality
print("1: Convert speech to Morse code")
print("2: Convert Morse code to text")
choice = input("Choose an option (1 or 2): ")

if choice == '1':
    text = recognize_speech_from_mic()
    if text:
        print("Recognized text:", text)
        morse_code = text_to_morse_code(text)
        print("Morse code:", morse_code)
        play_morse_code_sound(morse_code)  # Play Morse code sound
elif choice == '2':
    morse_code = input("Enter Morse code (use space between letters and 3 spaces between words): ")
    decoded_text = morse_code_to_text(morse_code)
    print("Decoded text:", decoded_text)
    text_to_speech(f"{decoded_text}")  # Speak the decoded text
else:
    print("Invalid choice. Please choose 1 or 2.")
    text_to_speech("Invalid choice. Please choose 1 or 2.")
