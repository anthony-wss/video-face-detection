count=0
video_folder=$1
frames_folder=$2

for video_file in $video_folder/*.mp4; do
  # Video title format: xxx-[video_id].mp4
  extracted_id=$(echo "$video_file" | grep -oP '\[\K[^\]]+(?=\])')
  
  # Randomly select ~100 frames
  total_frames=$(ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of default=nokey=1:noprint_wrappers=1 "$video_file") > /dev/null 2>&1
  interval=$((total_frames / 100))

  # Save to $frames_folder/[video_id]/
  mkdir -p $frames_folder/$extracted_id
  ffmpeg -i "$video_file" -vf "select='not(mod(n\,$interval))'" -vsync vfr $frames_folder/$extracted_id/frame_%03d.png > /dev/null 2>&1

  # Print progress
  count=$((count + 1))
  if (( count % 10 == 0 )); then
    echo "progress: $((count / 10))%"
  fi
done

