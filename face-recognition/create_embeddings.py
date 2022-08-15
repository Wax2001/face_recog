import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import os
import joblib

path_to_images_dir = 'images'


def main():
    embeddings = []
    labels = []

    for class_dir in os.listdir(path_to_images_dir):
        if not os.path.isdir(os.path.join(path_to_images_dir, class_dir)):
            continue
        for img_path in image_files_in_folder(os.path.join(path_to_images_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_box = face_recognition.face_locations(image)
            if len(face_bounding_box) != 0:
                embeddings.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_box)[0])
                labels.append(class_dir)
                print(img_path)
            print(labels)
    joblib.dump(embeddings, 'embeddings.pkl')
    joblib.dump(labels, 'labels.pkl')
    # print(embeddings[0])


if __name__ == '__main__':
    main()
