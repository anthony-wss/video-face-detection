video_folder=$1
frames_folder=$2

bash sample-frames.sh $video_folder $frames_folder
python main.py --frame_dir $frames_folder

