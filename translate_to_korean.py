import os
import sys
import openai

# OpenAI API 키 설정
openai.api_key = os.environ['gpt_api_key']

def translate_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI that translates text from English to Korean."},
            {"role": "user", "content": f"""
                {text}\n\n\n
                Translate the above text into Korean.
            """}
        ]
    )
    translation = response['choices'][0]['message']['content']
    return translation

if __name__ == "__main__":
    summary_path = sys.argv[1]
    output_path = sys.argv[2]
    
    with open(summary_path, 'r') as f:
        summary_text = f.read()
    
    translated_text = translate_text(summary_text)
    
    with open(output_path, 'w') as f:
        f.write(translated_text)
