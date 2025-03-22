import pyttsx3

# Initialize the converter
engine = pyttsx3.init()


# Open and read the text file
# The text file will be updated for every response from the therapist
with open('file.txt', 'r') as file:
    text = file.read()

# Convert text to speech
engine.say(text)
engine.runAndWait()
