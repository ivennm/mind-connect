from flask import Flask, render_template, request, jsonify
import azure.cognitiveservices.speech as speechsdk

app = Flask(__name__)

# Replace these with your actual Azure Speech credentials
AZURE_SPEECH_KEY = 'CcBGjao6ZunMSdz4fMmw5myOmlU0ACaGlXFkx5fKtEK3Xy2AS6sfJQQJ99BCACHYHv6XJ3w3AAAAACOGtXIK'
AZURE_REGION = 'eastus'

# Initialize Azure Speech Config
speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)

# Function to transcribe speech to text
def transcribe_audio_to_text(audio_stream):
    audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = recognizer.recognize_once()
    return result.text

# Function to synthesize speech from text
def synthesize_speech_from_text(text):
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    synthesizer.speak_text_async(text)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file uploaded'}), 400

    audio_file = request.files['audio']
    audio_stream = speechsdk.audio.AudioDataStream(audio_file.read())

    try:
        # Transcribe audio to text
        transcription = transcribe_audio_to_text(audio_stream)

        # Process the transcription (this is where you can add logic or call an assistant)
        response_text = f"You said: {transcription}. How can I assist you?"

        # Respond back with synthesized speech
        synthesize_speech_from_text(response_text)

        return jsonify({'transcription': transcription, 'response': response_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
