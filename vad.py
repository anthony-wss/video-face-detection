from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
from argparse import ArgumentParser
from typing import List
import os

SAMPLING_RATE = 16000
MIN_LENGTH = 1 # in seconds

def main(args):
    model = load_silero_vad(onnx=True)
    files: List[str] = os.listdir(args.audio_directory)
    for file in files:
        if file.endswith('.mp3'):
            extracted_id = file.split('.')[0]
            ret = []
            audio = read_audio(args.audio_directory + '/' + file)
            speech_timestamps = get_speech_timestamps(audio, model)
            for chunk in speech_timestamps:
                start_time = chunk['start'] / SAMPLING_RATE
                end_time = chunk['end'] / SAMPLING_RATE
                if end_time - start_time > MIN_LENGTH:
                    ret.append((round(start_time, 1), round(end_time, 1)))
            with open(args.output_file, 'a') as f:
                for i,chunk in enumerate(ret):
                    print(f'{extracted_id},{i},{chunk[0]},{chunk[1]}', file=f)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--audio_directory', required=True)
    parser.add_argument('--output_file', required=True)
    args = parser.parse_args()
    main(args)