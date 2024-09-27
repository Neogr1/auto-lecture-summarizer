import os
import sys
import re
import openai

openai.api_key = os.environ['gpt_api_key']

def preprocess_text(text):
    stopwords = ['so', 'and', 'like', 'but', 'or', 'because', 'then', 'just', 'very', 'actually', 'yeah', 'okay', 'may', 'some', 'please']
    pattern = r'\b(?:' + '|'.join(stopwords) + r')\b'

    text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    text = re.sub(r'\b(for example|such as|including|like)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def summarize_text(text):
    text = preprocess_text(text)
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI that summarizes video transcripts in markdown style."},
            {"role": "user", "content": f"""{text}\n\n\n---\n\nSummarize the above text in markdown style. The text is transcribed from speech recognition of English with a Korean accent. Because of this, the text may be inaccurate or incorrect. You must take this into account and summarize it accordingly. Summarize the text with as much detail as possible."""}
        ]
    )
    summary = response['choices'][0]['message']['content']
    return summary

if __name__ == "__main__":
    transcript_path = sys.argv[1]
    output_path = sys.argv[2]
    
    with open(transcript_path, 'r') as f:
        text = f.read()
    summary = summarize_text(text)
    with open(output_path, 'w') as f:
        f.write(summary)
