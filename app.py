from flask import Flask, request, render_template, jsonify
import os
import re
from groq import Groq

app = Flask(__name__)
api_key = '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'
client = Groq(api_key=api_key)

def save_audio_file(audio_data, filename="file.wav"):
    with open(filename, "wb") as f:
        f.write(audio_data)

def process_audio(filename="file.wav"):
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()), 
            model="distil-whisper-large-v3-en", 
            prompt="Specify context or spelling",  
            response_format="json",  
            language="en",  
            temperature=0.0  
        )
        text = transcription.text
        text = ''.join(text)
        return text

def get_result(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Generate a complete block of code with all necessary imports. The code should be functional and self-contained, without usage examples. Make sure to handle any potential errors or issues based on the prompt's requirements."
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model="mixtral-8x7b-32768",
    )
    result = chat_completion.choices[0].message.content
    return result

def extract_code_from_result(result):
    pattern = r'```(?:\s*(?:py|python)\s*)?\n([\s\S]*?)```'
    match = re.search(pattern, result)
    if match:
        return match.group(1)
    return result

def replace_and_newline(text):
    return re.sub(r'/ \n', '/\n', text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['POST'])
def record_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No file part"}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if audio_file:
        save_audio_file(audio_file.read())
        transcription = process_audio()
        return jsonify({"transcription": transcription})

    return jsonify({"error": "Unknown error"}), 500

@app.route('/generate_code', methods=['POST'])
def generate_code():
    data = request.json
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    result = get_result(prompt)
    output_text = replace_and_newline(extract_code_from_result(result))
    return jsonify({"code": output_text})

if __name__ == '__main__':
    app.run(debug=True)
