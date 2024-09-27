# Video Face Detection

The code is designed for large amount of videos (>1k).

## TODOs

- [ ] optimize: accelerate frame sampling process

## Start

```bash
pip install -r requirements.txt
bash run.sh [video_folder] [frames_folder]
```

## Implementation

1. Extract 100 frames as png from all the mp4 files in `video_folder`.
2. Detect all faces in each frame with `face_recognition.batch_face_locations` (GPU required)
3. Encode the faces with `face_recognition.face_encodings`.
4. Cluster all the faces so that the distance between any two vectors within the same cluster is less than or equal to `TOLERANCE`
5. Dump the results to `results.json`.

### results.json
Format in results.json:
```python
[
    video_id,
    face_prob,
    face_clusters,
    avg_num_faces
]
```

$N$: number of sampled frames

$n$: number of frames that has at least one face

$a_i$: number of faces in frame $i$

$b_i$: number of faces in frame $i$ after background faces removal

$c_i$: for a particular face $i$, it appears $c_i$ time in all the $N$ frames

* `video_id`: the folder name in `frames/`
* `face_prob`: the probability $\frac{n}{N}$
* `face_clusters`: the distribution of each faces: $\frac{c_1}{N}, \frac{c_2}{N}, ...$
* `avg_num_faces`: the average of faces number for all frames after background faces removal: $\frac{\sum_i^n b_i}{n}$

### `LOG_CLUSTER_IMG`

Save the face clustering results to `debug/` folder. This is used to tune the `TOLERANCE`.

