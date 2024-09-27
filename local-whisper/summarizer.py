import os
import sys
import time
import warnings
import subprocess
import whisper
import openai

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")
openai.api_key = os.environ['gpt_api_key']

def extract_audio(video_path, audio_path):
    command = f"ffmpeg -y -i '{video_path}' -filter:a 'atempo=1.4' -b:a 32k '{audio_path}' -loglevel quiet"
    subprocess.call(command, shell=True, stdin=subprocess.DEVNULL)
    print(f"[INFO] Audio extracted to {audio_path}")

def transcribe_audio(audio_path, transcript_path, language='en'):
    model = whisper.load_model("small")
    result = model.transcribe(audio_path, language=language)
    with open(transcript_path, "w") as f:
        f.write(result["text"])
    print(f"[INFO] Transcription saved to {transcript_path}")

def summarize_text(transcript_path, summary_path, language='en'):
    with open(transcript_path, "r") as f:
        text = f.read()
        
    ENG_TEXT_USER = {"role": "user", "content": f"""{text}\n\n\n---\n\nSummarize the above text in markdown style. The text is transcribed from speech recognition of English with a Korean accent. Because of this, the text may be inaccurate or incorrect. You must take this into account and summarize it accordingly. Summarize the text with as much detail as possible."""}
    KOR_TEXT_USER = {"role": "user", "content": f"""{text}\n\n\n---\n\nSummarize the above text in markdown style in Korean. The text is transcribed from speech recognition of Korean. Because of this, the text may be inaccurate or incorrect. You must take this into account and summarize it accordingly. Summarize the text with as much detail as possible."""}

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI that summarizes video transcripts in markdown style."},
            ENG_TEXT_USER if language == 'en' else KOR_TEXT_USER
        ]
    )
    summary = response['choices'][0]['message']['content']
    with open(summary_path, "w") as f:
        f.write(summary)
    print(f"[INFO] Summary saved to {summary_path}")

def translate_text(summary_path, translation_path):
    with open(summary_path, "r") as f:
        text = f.read()
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI that translates text to Korean. Translate the text in a way that is suitable for summarizing video lectures in markdown format. Ensure that all sentences end with a noun form in Korean. Do not translate technical terms, jargon, or topic titles. Also, do not translate any markdown formatting such as headers, bold, or italic text; leave them exactly as they are in the original."},
            {"role": "user", "content": f"""{text}\n\n\n---\n\nTranslate the above text into Korean. The translation should be appropriate for summarizing video lectures in markdown format, with all sentences ending in a noun form. Keep all titles, technical terms, and markdown formatting (like headers and bold text) in English without translation."""}
        ]
    )
    translation = response['choices'][0]['message']['content']
    with open(translation_path, "w") as f:
        f.write(translation)
    print(f"[INFO] Summary saved to {translation_path}")


def create_directories(base_dir):
    audio_dir = os.path.join(base_dir, "audio")
    text_dir = os.path.join(base_dir, "text")
    summary_dir = os.path.join(base_dir, "summary")
    os.makedirs(audio_dir, exist_ok=True)
    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(summary_dir, exist_ok=True)
    return audio_dir, text_dir, summary_dir

def main(video_path, language='en'):
    base_dir, video_filename = os.path.split(video_path)
    filename_without_ext = os.path.splitext(video_filename)[0]
    audio_dir, text_dir, summary_dir = create_directories(base_dir)

    audio_path = os.path.join(audio_dir, f"{filename_without_ext}.mp3")
    transcript_path = os.path.join(text_dir, f"{filename_without_ext}.txt")
    summary_path = os.path.join(summary_dir, f"{filename_without_ext}_summary_{language}.txt")
    translation_path = os.path.join(summary_dir, f"{filename_without_ext}_summary_ko.txt")

    print("[INFO] Audio extraction started.")
    start_time = time.time()
    extract_audio(video_path, audio_path)
    audio_extraction_time = time.time() - start_time
    print(f"[INFO] Audio extraction took {audio_extraction_time:.2f} seconds.")

    print("[INFO] Transcription started.")
    start_time = time.time()
    transcribe_audio(audio_path, transcript_path, language=language)
    transcription_time = time.time() - start_time
    print(f"[INFO] Transcription took {transcription_time:.2f} seconds.")

    print("[INFO] Summarization started.")
    start_time = time.time()
    summarize_text(transcript_path, summary_path, language=language)
    summarization_time = time.time() - start_time
    print(f"[INFO] Summarization took {summarization_time:.2f} seconds.")

    if language == 'en':
        print("[INFO] Translation started.")
        start_time = time.time()
        translate_text(summary_path, translation_path)
        translation_time = time.time() - start_time
        print(f"[INFO] Translation took {translation_time:.2f} seconds.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] Usage: python script.py <video_path> [<language>]")
    else:
        video_path = sys.argv[1]
        lang = 'en' if len(sys.argv) == 2 else sys.argv[2]
        main(video_path, language=lang)
