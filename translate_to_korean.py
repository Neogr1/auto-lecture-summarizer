import os
import sys
import openai

# OpenAI API 키 설정
openai.api_key = os.environ['gpt_api_key']

def translate_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI that translates text from English to Korean. Translate the text in a way that is suitable for summarizing video lectures in markdown format. Ensure that all sentences end with a noun form in Korean. Do not translate technical terms, jargon, or topic titles. Also, do not translate any markdown formatting such as headers, bold, or italic text; leave them exactly as they are in the original."},
            {"role": "user", "content": f"""{text}\n\n\n---\n\nTranslate the above text into Korean. The translation should be appropriate for summarizing video lectures in markdown format, with all sentences ending in a noun form. Keep all titles, technical terms, and markdown formatting (like headers and bold text) in English without translation."""}
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
