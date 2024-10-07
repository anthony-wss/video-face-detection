#! /usr/env/bash

video_folder=$1
timestamps_file=$2

mkdir temp
shopt -s nullglob

for video_file in "$video_folder/*.mp4"; do
  # Extract the audio
  if [[ ! -f $video_file ]]; then
    continue
  fi
  echo $video_file
  python3 extract.py --input_path "$video_file" --output_directory "temp"
done

python3 vad.py --audio_directory "temp" --output_file "$timestamps_file"

rm -rf temp

