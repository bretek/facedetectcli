import face_recognition
import os
import argparse
import pickle

parser = argparse.ArgumentParser("facedetectcli")
parser.add_argument("--learn", nargs=2, default=[None, None])
parser.add_argument("--check", nargs=2, default=[None, None])
args,rest = parser.parse_known_args()

def learnFace(input, output):
    known_face_encodings = []
    for filename in os.listdir(input):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(input, filename)
            image = face_recognition.load_image_file(image_path)

            face_encodings = face_recognition.face_encodings(image)
            if len(face_encodings) > 0:
                known_face_encodings.append(face_encodings[0])

    with open(output, "wb") as f:
        pickle.dump(known_face_encodings, f)

def checkFace(data_folder, input):
    known_face_encodings = []

    image = face_recognition.load_image_file(input)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    for filename in os.listdir(data_folder):
        known_face_encodings = []
        with open(os.path.join(data_folder, filename), "rb") as f:
            known_face_encodings = pickle.load(f)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            if len(matches) > 0:
                print(filename)
            else:
                print("Not recognised")

if args.learn[0] is not None:
    learnFace(args.learn[0], args.learn[1])
elif args.check[0] is not None:
    checkFace(args.check[0], args.check[1])
