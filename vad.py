from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
from argparse import ArgumentParser
from typing import List
import os

SAMPLING_RATE = 16000
NEIGHBOR_THRESHOLD = 3  # seconds
MIN_DURATION = 15  # seconds

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
                ret.append((start_time, end_time))
            # Concatenate adjacent chunks that are close to each other
            merged_chunks = []
            if ret:
                current_chunk = ret[0]
                for next_chunk in ret[1:]:
                    if next_chunk[0] - current_chunk[1] <= NEIGHBOR_THRESHOLD:  # Adjust the threshold as needed
                        current_chunk = (current_chunk[0], next_chunk[1])
                    else:
                        merged_chunks.append(current_chunk)
                        current_chunk = next_chunk
                merged_chunks.append(current_chunk)
            ret = merged_chunks
            ret = [(start, end) for start, end in ret if end - start >= MIN_DURATION]
            with open(args.output_file, 'a') as f:
                for i,chunk in enumerate(ret):
                    print(f'{extracted_id},{i},{chunk[0]},{chunk[1]}', file=f)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--audio_directory', required=True)
    parser.add_argument('--output_file', required=True)
    args = parser.parse_args()
    main(args)