from flask import Flask, render_template, request, jsonify
from gemini_backend import generate_response
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    my_variable = generate_response('test')
    return render_template('index.html', variable=my_variable)

@app.route('/chat', methods=['POST'])
def chat():
<<<<<<< HEAD
    user_input = request.json.get('user_input')  # Get JSON data from the client

    if not user_input:
        return jsonify(error="No input provided"), 400

#Generate response from the backend logic
    my_variable = generate_response(user_input)

#Return the new response as JSON
    return jsonify(response=my_variable)
=======
    data = request.get_json()
    message = data['message']
    
    if not message:
        return jsonify(error="No message provided"), 400

    # Get response from Gemini (replace this with your actual AI logic)
    response = generate_response(message)
    
    return jsonify(response=response)
>>>>>>> 11f73a11019101bb5f06617158b534a4621a8bfa

if __name__ == '__main__':
    app.run(debug=True)
