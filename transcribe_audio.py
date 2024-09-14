import os
import sys
import openai

openai.api_key = os.environ['gpt_api_key']

def transcribe_audio(audio_path, language="en"):
    with open(audio_path, "rb") as audio_file:
        transcription = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            language=language
        )
    return transcription["text"]

if __name__ == "__main__":
    audio_path = sys.argv[1]
    output_path = sys.argv[2]

    transcript = transcribe_audio(audio_path)
    with open(output_path, 'w') as f:
        f.write(transcript)