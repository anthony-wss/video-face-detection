from argparse import ArgumentParser
import face_recognition
import os
import json
from tqdm import tqdm
import cv2
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist
from collections import Counter


TOLERANCE = 0.7
LOG_CLUSTER_IMG = False
BATCH_SIZE = 30

# def find_face_in_pool(face_emb, emb_pool, TOLERANCE=0.4):
#     """ 
#     Return the pos of the first match, otherwise return -1.
#     """
#     distances = list(face_recognition.face_distance(emb_pool, face_emb))
#     distances = [dis if dis <= TOLERANCE else 1 for dis in distances]
#     if not distances or min(distances) == 1:
#         return -1
#     return np.argmin(distances)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--frame_dir", required=True)
    args = parser.parse_args()

    frame_dir = args.frame_dir
    results = []

    for video_folder in tqdm(os.listdir(frame_dir)):
        N = len(os.listdir(os.path.join(frame_dir, video_folder)))
        all_embs = []
        all_faces = []
        has_face = 0
        batch_img = []
        face_in_frames = []

        # Read images
        for frame_png in os.listdir(os.path.join(frame_dir, video_folder)):
            image = face_recognition.load_image_file(os.path.join(frame_dir, video_folder, frame_png))
            image = np.ascontiguousarray(image[:, :, ::-1])
            batch_img.append(image)

        # Find face locations with GPU
        batch_of_face_locations = []
        for batch_i in range(0, len(batch_img), BATCH_SIZE):
            end = min(len(batch_img), batch_i+BATCH_SIZE)    
            locations = face_recognition.batch_face_locations(batch_img[batch_i:end], number_of_times_to_upsample=0)
            batch_of_face_locations.extend(locations)

        # Encode the images into embedding
        for frame_number_in_batch, face_locations in enumerate(batch_of_face_locations):
            face_areas = [(pos[2]-pos[0])*(pos[1]-pos[3]) for pos in face_locations]
            face_areas = sorted(face_areas, reverse=True)

            # Background faces removal
            # Definition: the face area is more than 3x smaller than
            # the smallest face in the detected faces.
            end_idx = len(face_areas)
            for i in range(len(face_areas)):
                if i+1 < len(face_areas) and face_areas[i] / face_areas[i+1] > 3:
                    end_idx = i+1
                    break
            face_areas = face_areas[:end_idx]

            # Encode faces into embeddings
            face_embs = face_recognition.face_encodings(
                batch_img[frame_number_in_batch], known_face_locations=face_locations, num_jitters=10,
                model='large'
            )
            if len(face_areas) > 0:
                face_in_frames.append(len(face_areas))
            all_embs.extend(face_embs)

            if LOG_CLUSTER_IMG:
                for i in range(len(face_embs)):
                    pos = face_locations[i]
                    img = batch_img[frame_number_in_batch][pos[0]:pos[2], pos[3]:pos[1], :]
                    all_faces.append(img)
            if len(face_embs) > 0:
                has_face += 1
                
        # Run clustering
        distance_matrix = pdist(all_embs, metric='euclidean')
        Z = linkage(distance_matrix, method='complete')
        clusters = fcluster(Z, t=TOLERANCE, criterion='distance')

        counter = Counter(clusters)
        order_id = sorted(counter, key=counter.get, reverse=True)
        
        if LOG_CLUSTER_IMG:
            for i in range(len(all_faces)):
                cluster = clusters[i]
                os.makedirs(f"debug/{cluster}/", exist_ok=True)
                cv2.imwrite(f"debug/{cluster}/{i}.png", all_faces[i])

        results.append([
            video_folder, round(has_face/N, 2), [round(counter[i]/N, 2) for i in order_id], np.mean(face_in_frames)
        ])
        with open('results.json', "w") as fout:
            json.dump(results, fout, indent=2, ensure_ascii=False)

