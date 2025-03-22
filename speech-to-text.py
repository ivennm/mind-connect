import speech_recognition as sr
from enum import Enum
import time
import sys

class Language(Enum):
    ENGLISH = "en-US"
    CHINESE = "zh-TW"
    FRENCH = "fr-FR"
    SPANISH_SPAIN = "es-ES"
    SPANISH_LATAM = "es-US"
    KOREAN = "ko-KR"
    JAPANESE = "ja-JP"

class SpeechToText():
    @staticmethod
    def print_mic_device_index():
        try:
            mics = sr.Microphone.list_microphone_names()
            if not mics:
                print("No microphones found!")
                return
            print("Available microphones:")
            for index, name in enumerate(mics):
                print("Microphone {1}, device_index={0}".format(index, name))
        except Exception as e:
            print(f"Error listing microphones: {e}")
    
    @staticmethod
    def speech_to_text(device_index, language=Language.ENGLISH):
        r = sr.Recognizer()
        
        # Lower the energy threshold for better speech detection
        r.energy_threshold = 1000  # Lowered from 4000
        r.dynamic_energy_threshold = True
        r.pause_threshold = 0.8  # Shorter pause threshold
        
        try:
            # Initialize the microphone
            mic = sr.Microphone(device_index=device_index)
            print(f"Using microphone: {sr.Microphone.list_microphone_names()[device_index]}")
            
            with mic as source:
                print("Please Start Speaking...")
                # Adjust for ambient noise
                print("Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source, duration=2)
                print(f"Energy threshold set to: {r.energy_threshold}")
                print("Ready! Listening... (You have 15 seconds to start speaking)")
                
                # Increased timeout to 15 seconds and phrase_time_limit to 30 seconds
                try:
                    audio = r.listen(source, timeout=15, phrase_time_limit=30)
                    print("Speech detected! Processing...")
                    
                    try:
                        text = r.recognize_google(audio, language=language.value)
                        print("You said: {}".format(text))
                        return text
                    except sr.UnknownValueError:
                        print("Sorry, could not understand the audio. Please speak clearly and try again.")
                    except sr.RequestError as e:
                        print("Could not request results from Google Speech Recognition service;")
                        print(f"Error details: {e}")
                except sr.WaitTimeoutError:
                    print("No speech detected within the timeout period.")
                    print("Please check:")
                    print("1. Is your microphone working? Try speaking into it and check if the input level changes")
                    print("2. Are you speaking loud enough?")
                    print("3. Is the microphone too far away?")
                    print("4. Is there too much background noise?")
        except Exception as e:
            print(f"Error accessing microphone: {e}")
            print("Troubleshooting steps:")
            print("1. Check if your microphone is properly connected")
            print("2. Grant microphone permissions to Terminal/IDE in System Settings > Privacy > Microphone")
            print("3. Try using a different microphone from the list above")
            print(f"4. Technical error details: {str(e)}")
        finally:
            try:
                mic.close()
            except:
                pass

def check_mic_device_index():
    SpeechToText.print_mic_device_index()

def run_speech_to_text_english(device_index):
    return SpeechToText.speech_to_text(device_index, Language.ENGLISH)

def run_speech_to_text_spanish(device_index):
    return SpeechToText.speech_to_text(device_index, Language.SPANISH_SPAIN)

if __name__ == '__main__':
    # First check available microphones
    check_mic_device_index()
    
    # Try to use the first available microphone
    try:
        device_index = 0  # Start with the first microphone
        print("\nTesting English recognition:")
        if run_speech_to_text_english(device_index):
            print("Speech recognition successful!")
        
        print("\nWould you like to try Spanish recognition? (y/n)")
        response = input().lower()
        if response.startswith('y'):
            time.sleep(1)
            print("\nTesting Spanish recognition:")
            run_speech_to_text_spanish(device_index)
    except KeyboardInterrupt:
        print("\nStopping speech recognition...")
        sys.exit(0)

