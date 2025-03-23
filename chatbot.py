import google.generativeai as gemini
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import datetime
from pymongo.server_api import ServerApi

# Load environment variables
load_dotenv()

# Configure Gemini API
gemini.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Connect to MongoDB
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI,server_api=ServerApi('1'))

print(MONGODB_URI)
db = client["chatbot_db"]
collection = db["conversations"]
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

print("Connected to MongoDB")

def save_conversation(user_message, bot_response):
    conversation = {
        "user_message": user_message,
        "bot_response": bot_response,
        "timestamp": datetime.datetime.now()
    }
    collection.insert_one(conversation)
    print("Conversation saved to MongoDB.")

def save_user_preferences(user_id, name):
    user_data = {
        "user_id": user_id,
        "name": name,
        "preferences": {}  # You can add other preferences like themes, etc.
    }
    collection.update_one({"user_id": user_id}, {"$set": user_data}, upsert=True)
    print("User preferences saved.")

def display_conversations():
    all_conversations = collection.find()
    print("\n--- Stored Conversations ---")
    for conversation in all_conversations:
        print(f"Time: {conversation['timestamp']}")
        print(f"User: {conversation['user_message']}")
        print(f"Bot: {conversation['bot_response']}")
        print("--------------------------")


# Initialize the chatbot
def chatbot():
    print("Welcome to the Mental Health Chatbot! Type 'exit' to end the conversation.")
    
    # Initialize the Gemini model with the correct name
    model = gemini.GenerativeModel('gemini-1.5-flash')  # Updated model name
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Exit the chatbot
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye! Take care.")
            break
        if user_input.lower() == 'show conversations':
            display_conversations()
            continue
        # Generate a response using Gemini
        try:
            response = model.generate_content(user_input)
            print(f"Chatbot: {response.text}")

            save_conversation(user_input, response.text)    
        except Exception as e:
            print(f"Chatbot: Sorry, I encountered an error. Please try again. Error: {e}")

# Run the chatbot
if __name__ == '__main__':
    collection.insert_one({"conversation":"one"})
    chatbot()