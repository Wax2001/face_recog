import face_recognition
import cv2
import numpy as np
import joblib
from datetime import datetime
import requests
import logging
import sys
import config
from threading import Thread
import io
import redis
from time import sleep

logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler(sys.stdout))
# video_capture = cv2.VideoCapture('rtsp://admin:petricore@192.168.0.201:554/profile3')
# video_capture = cv2.VideoCapture(0)
video_capture = cv2.VideoCapture('rtsp://192.168.31.91:8000/h264_ulaw.sdp')
known_face_encodings = joblib.load(config.PATH_TO_EMBS)
known_face_labels = joblib.load(config.PATH_TO_LABELS)
print(known_face_labels, set(known_face_labels))
metadata = {}
for i in set(known_face_labels):
    metadata[i] = [True, 0]
UPD = False
# r = redis.Redis(host='localhost', port=6379)
WORK = True

def recogn_faces():
    global UPD, WORK, metadata
    process_this_frame = True
    print('rf up', flush=True)
    local_encodings = known_face_encodings
    local_names = known_face_labels
    while WORK:
        if UPD:
            local_encodings = known_face_encodings
            local_names = known_face_labels
            UPD = False
            print('new upd')
        ret, frame = video_capture.read()

        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            print(datetime.now(), flush=True)
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(local_encodings, face_encoding, tolerance=0.55)
                name = "Unknown"
                face_distances = face_recognition.face_distance(local_encodings, face_encoding)
                #
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = local_names[best_match_index]
                if name != 'Unknown':
                    print('redis-wait', '{} {}'.format(name, datetime.now().strftime('%Y-%m-%dT%H:%M+05:00')))
                    metadata[name][1] += 1
                    # r.rpush('redis-wait', '{} {}'.format(name, datetime.now().strftime('%Y-%m-%dT%H:%M+05:00')))
                    # r = requests.post('https://httpbin.org/post', data={'key': '{}, {}'.format(name, datetime.now())})
                    # logger.info(f"{name} | {datetime.now()} | {r.status_code}")
                print(name, datetime.now())

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        # for (top, right, bottom, left), name in zip(face_locations, face_names):
        #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        #     top *= 4
        #     right *= 4
        #     bottom *= 4
        #     left *= 4
        
        #     # Draw a box around the face
        #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        #     # Draw a label with a name below the face
        #     cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        #     font = cv2.FONT_HERSHEY_DUPLEX
        #     cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        # Display the resulting image
        cv2.imshow('Video', frame)
    
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            WORK = False
    
    video_capture.release()
    cv2.destroyAllWindows()


def upd_embs():
    global UPD, WORK, known_face_labels, known_face_encodings
    ir = redis.Redis(host=config.REDIS_HOST, port=6379)
    print('ue up')
    while WORK:
        try:
            message = ir.lpop('redis-channel')
            if message is not None:
                message = message.decode('utf-8')
                id_url = message.split()
                img = requests.get(config.BACK_SERV + id_url[1])
                if img.status_code == 200:
                    with io.BytesIO(img.content) as buffer:
                        img = face_recognition.load_image_file(buffer)
                        print('h1\n')
                        face_bounding_box = face_recognition.face_locations(img)
                        print('h2\n')
                        if len(face_bounding_box) != 0:
                            known_face_encodings.append(
                                face_recognition.face_encodings(img, known_face_locations=face_bounding_box)[0])
                            known_face_labels.append(id_url[0])
                            print(id_url[0])
                            UPD = True
                        print(len(face_bounding_box))
                print(message, known_face_labels)
        except Exception as e:
            print(e)
            sleep(3)


def send_report():
    global r, metadata
    print('sr up')
    while WORK:
        # print(metadata.values())
        for id in metadata.keys():
            if metadata[id][1] >= 5 and metadata[id][0]:
                rep = requests.post(
                    config.POST_TO,
                    json={
                        "user": int(id), "user_occurences": 5,
                        "check_in_time": datetime.now().strftime('%Y-%m-%dT%H:%M+05:00'), "check_out_time": "2021-12-03T13:20:00+05:00",
                        "post_data:": "check-in",
                    }
                )
                print(rep.status_code)
                if rep.status_code == 201:
                    metadata[id][0] = False
        # sleep(1)

        # send = r.lpop('redis-wait')
        # if send is not None:
        #     spl = send.decode('utf-8').split()
        #     rep = requests.post(
        #         'http://192.168.0.100:8000/api/records/',
        #         json={
        #             "user": int(spl[0]), "user_occurences": 5,
        #             "check_in_time": spl[1], "check_out_time": "2021-12-03T13:20:00+05:00"
        #         }
        #     )
        #     print('sender: ', rep.status_code)


if __name__ == '__main__':
    try:
        print('hgf')
        rf = Thread(target=recogn_faces)
        # ue = Thread(target=upd_embs)
        sr = Thread(target=send_report)

        rf.start()
        # ue.start()
        sr.start()

        rf.join()
        # ue.join()
        sr.join()
    except KeyboardInterrupt:
        WORK = False
        rf.join()
        # ue.join()
        sr.join()
        joblib.dump(known_face_encodings, 'embeddings.pkl')
        joblib.dump(known_face_labels, 'labels.pkl')
        print('Exiting')
        exit()
