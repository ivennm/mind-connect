import pyttsx3
import subprocess

subprocess.run(["python3", "gemini.py"], check=True)

# Initialize the converter
engine = pyttsx3.init()

# Open and read the text fileW
with open('file.txt', 'r') as file:
    text = file.read()

# Convert text to speech
engine.say(text)
engine.runAndWait()