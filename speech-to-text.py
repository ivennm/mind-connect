import speech_recognition as sr
import pyttsx3

def record_text():
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Clear the file contents at the start of the program
    with open('speech_output.txt', 'w') as file:
        file.write('')
    
    # Recording the audio
    with sr.Microphone() as source:
        print("Speak now...")
        audio = recognizer.listen(source)
        
    try:
        # Converting speech to text
        text = recognizer.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service.")
        return ""

def output_text(text):
    # Initialize text-to-speech engine
    engine = pyttsx3.init()
    
    # Converting text to speech
    if text:
        engine.say(text)
        engine.runAndWait()
        
        # Save the text to a file
        with open('speech_output.txt', 'a') as file:
            file.write(text + '\n')

while(1):
    text = record_text()
    output_text(text)

    print("Finished Writing text")
