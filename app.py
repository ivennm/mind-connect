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
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify(error="No input provided"), 400
    
    # Get response from Gemini
    response = generate_response(user_input)
    return jsonify(response=response)

if __name__ == '__main__':
    app.run(debug=True)
