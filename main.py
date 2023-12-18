import face_recognition
import os
from fastapi import FastAPI 


app = FastAPI()


def es_rostro_suficientemente_grande(top, right, bottom, left, umbral_area):
    area = (bottom - top) * (right - left)
    return area > umbral_area


dataPath = "./imgs"
dataPathScan = "./imgs_scan"

@app.get("/{user_code}")
def index(user_code: str):
    peopleList = os.listdir(dataPath)
    face_knows = []
    face_knows_name = []
    for nameDir in peopleList:
        if ".png" not in nameDir or nameDir == '.DS_Store':
            continue
        personPath = os.path.join(dataPath, nameDir)
        known_i = face_recognition.load_image_file(personPath)
        face_locations = face_recognition.face_locations(known_i)
        for face_location in face_locations:
            top, right, bottom, left = face_location
            if es_rostro_suficientemente_grande(top, right, bottom, left, umbral_area=10000):  # Ajusta el umbral según sea necesario
                img_encoding = face_recognition.face_encodings(known_i, [face_location])[0]
                face_knows.append(img_encoding)
                face_knows_name.append(nameDir)

    print(dataPathScan+"/"+user_code+".png")
    unknown_image = face_recognition.load_image_file(dataPathScan+"/"+user_code+".png")
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    results = face_recognition.compare_faces(face_knows, unknown_encoding,0.4)
    print(peopleList)
    print(results)


    try: 
        indice = results.index(True)
        print(f"El elemento está en el índice: {indice}")
        return {"persona":face_knows_name[indice]}
    except ValueError:
        print("El elemento no está en la lista.")
        return {"persona":"no encontrada"}
    