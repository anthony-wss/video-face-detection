# Video Face Detection

Features:
- Design for large amount of videos (>1k).

## Start

```bash
pip install -r requirements.txt
bash run.sh [folder-to-videos]
```

## Implementation

1. Extract 100 frames as png from 1k mp4 files.
2. Detect all faces within each frame with `face_recognition.batch_face_locations` (require GPU)
3. Calculate its embedding with `face_recognition.face_encodings`.
4. Cluster all the faces so that the distance between any two vectors within the same cluster is less than or equal to `TOLERANCE`
5. Dump the following info into `results.json`:
    1. % of frames with faces
    2. % of frequency for each faces

