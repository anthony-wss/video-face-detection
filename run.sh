video_folder=$1
frames_folder=$2

bash vad.sh $video_folder timestamps.csv
bash sample-frames.sh chunked_videos $frames_folder
python main.py --frame_dir $frames_folder

