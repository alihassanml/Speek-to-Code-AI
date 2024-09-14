# Speak to Code AI

A Flask-based web application that transcribes audio into code. Users can upload audio files, which are then transcribed into text, and use that text to generate functional code snippets via an AI-powered API.

## Features

- **Audio Transcription:** Upload audio files and receive transcriptions.
- **Code Generation:** Generate functional code snippets based on text prompts.
- **3D Website Integration:** Incorporates 3D elements in the web interface (details not provided in this script).

image[./1.png]

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alihassanml/Speek-to-Code-AI.git
   cd Speek-to-Code-AI
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory and add your API key:
   ```env
   API_KEY=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
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

## Usage

- **Record Audio:** Send a POST request to `/record` with a file upload. The response will contain the transcription of the audio.
- **Generate Code:** Send a POST request to `/generate_code` with a JSON body containing the `prompt` for code generation. The response will include the generated code.

## API Endpoints

- `POST /record`: Uploads audio and returns transcription.
- `POST /generate_code`: Accepts a prompt and returns generated code.

## Dependencies

- Flask
- groq

## License

This project is licensed under the MIT License.
