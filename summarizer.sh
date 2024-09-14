#!/bin/bash

video_path=$1

if [ ! -f "$video_path" ]; then
  echo "ERROR: No such file '$video_path'"
  exit 1
fi

base_name=$(basename "$video_path" .mp4)
output_dir="./output"
audio_dir="$output_dir/audio"
text_dir="$output_dir/text"
summary_dir="$output_dir/summary"

mkdir -p "$audio_dir"
mkdir -p "$text_dir"
mkdir -p "$summary_dir"

# 1. MP3로 1.4배 속도의 음성 파일 추출
echo "1.4배 속도로 음성 파일을 추출합니다."
audio_path="$audio_dir/${base_name}_1.4x.mp3"
ffmpeg -i "$video_path" -filter:a "atempo=1.4" -b:a 32k "$audio_path" -loglevel quiet
echo "1.4배 속도의 음성 파일이 $audio_path에 저장되었습니다."

# 2. MP3에서 텍스트 추출
echo "Whisper 모델을 이용하여 텍스트를 추출합니다."
transcript_path="$text_dir/$base_name.txt"
python3 transcribe_audio.py "$audio_path" "$transcript_path"
echo "텍스트 파일이 $transcript_path에 저장되었습니다."

# 3. 텍스트 파일을 요약
echo "텍스트 파일을 요약합니다."
summary_path="$summary_dir/${base_name}_summary.md"
python3 summarize_text.py "$transcript_path" "$summary_path"
echo "요약 파일이 $summary_path에 저장되었습니다."

# 4. 요약된 파일을 한국어로 번역
echo "요약 파일을 한국어로 번역합니다."
translated_path="$summary_dir/${base_name}_summary_ko.md"
python3 translate_to_korean.py "$summary_path" "$translated_path"
echo "한국어 번역 파일이 $translated_path에 저장되었습니다."