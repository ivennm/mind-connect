from gemini_backend import generate_response
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

user_input = 'hello there'

# Generate response using the user input
x = generate_response(user_input)
print('response:')
print(x)

# Ensure the response is written to a file
with open('test_backend.txt', 'w') as file:
    file.write(x)
