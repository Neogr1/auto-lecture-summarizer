#!/bin/bash

INPUT_FILE=$1
USER=$(whoami)

read -r header < "$INPUT_FILE"

while IFS=',' read -r class lecture language url; do
    # remove carrage return
    url=$(echo "$url" | sed 's/\r//')

    SAVE_DIR="/home/$USER/lecture/$class"
    FILE_PATH="$SAVE_DIR/$lecture.mp4"

    mkdir -p "$SAVE_DIR"
    wget -O "$FILE_PATH" -q --show-progress "$url"
    WGET_STATUS=$?

    if [ $WGET_STATUS -eq 0 ]; then
        python3 summarizer.py "$FILE_PATH" "$language"
    else
        echo "Failed to download $url"
    fi
done < <(tail -n +2 "$INPUT_FILE")
