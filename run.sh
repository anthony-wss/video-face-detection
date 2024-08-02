video_folder=$1

bash sample-frames.sh $video_folder
python main.py --frame_dir ./frames

