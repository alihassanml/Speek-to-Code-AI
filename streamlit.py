import speech_recognition as sr
from pydub import AudioSegment
import time
import io
import os
from IPython import display
import re
import streamlit as st
from groq import Groq
import speech_recognition as sr
import librosa
import matplotlib.pyplot as plt



api_key = ''
client = Groq(api_key=api_key)


def voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
            st.write("Adjusting noise...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            st.write('Recording voice')
            recorded_audio = recognizer.listen(source, timeout=7)
            st.write("Done recording.")
            text = recognizer.recognize_google(recorded_audio, language="en-US")
            st.write("Decoded Text: {}".format(text))
            
            # ------------------- Save As File

            if os.path.exists('file.wav'):
                os.remove("file.wav")
            with open("file.wav", "wb") as f:
                f.write(recorded_audio.get_wav_data())
            st.audio('file.wav',format='audio/wav')


def display_grok_data():
    filename = 'file.wav'
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
        file=(filename, file.read()), # Required audio file
        model="distil-whisper-large-v3-en", # Required model to use for transcription
        prompt="Specify context or spelling",  # Optional
        response_format="json",  # Optional
        language="en",  # Optional
        temperature=0.0  # Optional
        )
        # Print the transcription text
        st.write(transcription.text)
        data =  transcription.text
        return data


def get_result(prompot):
    client = Groq(
        api_key=api_key,
    )
    chat_completion = client.chat.completions.create(
        messages=[
                    {
                        "role": "system",
                        "content": "Write block code with all necessary imports and no example usage.\n Note: I want to show the result in code \n Give me full code" ,
                    },
                    {
                        "role": "user",
                        "content": prompot,
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




def remove_docstrings_and_comments(code):
    code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
    code = re.sub(r"'''(.*?)'''", '', code, flags=re.DOTALL)
    code = re.sub(r'#.*', '', code)
    code = re.sub(r'\n\s*\n', '\n', code).strip()
    return code


if st.button('Open Mic'):
    voice()
result_1 = display_grok_data()
result_2 = get_result(result_1)
result_3 = extract_code_from_result(result_2)
output_text = replace_and_newline(result_3)
# output_text = remove_docstrings_and_comments(output_text)
st.code(output_text)
