from google import genai
from google.genai import types

# Here change the API key to your if you want (this is Jhon's)
client = genai.Client(api_key="AIzaSyAPgVO7V4wwB5C7iwb7y50R_Sn-dGkDnds")

# response is going to be made into text which then is 
# made into speech
response = client.models.generate_content(
    model = "gemini-2.0-flash",
    config = types.GenerateContentConfig(
        system_instruction = "You are a therapist. Comfort the user."),
    # Here we can input the text file from the speech-to-text
    contents = [input()]
)
print(response.text)
