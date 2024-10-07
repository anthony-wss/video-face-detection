video_folder=$1
frames_folder=$2
timestamps_file=$3

bash vad.sh $video_folder $timestamps_file
bash sample-frames.sh $video_folder $frames_folder
python main.py --frame_dir $frames_folder

