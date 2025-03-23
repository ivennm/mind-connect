from flask import Flask, render_template, request, jsonify
from gemini_backend import generate_response
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    
    if not message:
        return jsonify(error="No message provided"), 400

    # Get response from Gemini (replace this with your actual AI logic)
    response = generate_response(message)
    
    return jsonify(response=response)

if __name__ == '__main__':
    app.run(debug=True)
