import base64
import requests
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

audio_file= open("./entrevistas/entrevista.m4a", "rb")

transcription = client.audio.transcriptions.create(
    model="gpt-4o-transcribe", 
    file=audio_file
)

print(transcription.text)