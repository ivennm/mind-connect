from google import genai
from google.genai import types
import os

# Set up the API client
client = genai.Client(api_key="API-KEY")

# Load previous conversation history (if exists)
history_file = "history.txt"

if os.path.exists(history_file):
    with open(history_file, "r") as file:
        history = file.read()
else:
    history = ""

# Get user input
user_input = input("Enter your message: ")

# Append new input to conversation history
full_conversation = f"{history}\nUser: {user_input}\nAI:"

# Generate response with past conversation as context
response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a therapist. Comfort the user."
    ),
    contents=[full_conversation]
)

# Ensure response is valid
if hasattr(response, "text"):
    response_text = response.text
else:
    response_text = "Sorry, I couldn't generate a response."

# Save updated conversation history
with open(history_file, "w") as file:
    file.write(f"{full_conversation} {response_text}\n")

# Save response to file.txt for text-to-speech
with open("file.txt", "w") as file:
    file.write(response_text)
