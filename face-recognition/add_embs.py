import face_recognition
import joblib
import redis
import requests
import io
from PIL import Image

import config

path_to_embs = config.PATH_TO_EMBS
path_to_labels = config.PATH_TO_LABELS

embeddings = joblib.load(path_to_embs)
labels = joblib.load(path_to_labels)

subscriber = redis.Redis(host='192.168.0.114', port=6379)
channel = 'redis-channel'
p = subscriber.pubsub()
p.subscribe(channel)
while True:
    message = p.get_message()
    if message and not message['data'] == 1:
        message = message['data'].decode('utf-8')
        id_url = message.split()
        img = requests.get('192.168.0.114:8000/' + id_url[1])
        if img.status_code == '200':
            img = Image.open(io.BytesIO(img))
            face_bounding_box = face_recognition.face_locations(img)
            if len(face_bounding_box) != 0:
                embeddings.append(face_recognition.face_encodings(img, known_face_locations=face_bounding_box)[0])
                labels.append(id_url[0])
        print(message)

