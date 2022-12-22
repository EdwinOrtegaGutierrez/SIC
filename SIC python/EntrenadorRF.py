from cProfile import label
import cv2
import os
import numpy as np

myPath = os.path.dirname(os.path.abspath(__file__))
dataPath = f'{myPath}/Data'
peopleList = os.listdir(dataPath)
print('Lista de personas: ', peopleList)

labels = []
facesData = []
label = 0

print("Leyendo imagenes...")
for nameDir in peopleList:
    personPath = dataPath + '/' + nameDir
    for fileName in os.listdir(personPath):
        labels.append(label)
        facesData.append(cv2.imread(personPath+'/'+fileName, 0))
        image =cv2.imread(personPath+'/'+fileName, 0)
        
    label  = label + 1
    
face_recognizer = cv2.face.EigenFaceRecognizer_create()

print("Entrenando IA...")

face_recognizer.train(facesData, np.array(labels))

# TAMBIEN SE PUEDE USAR .YAML
face_recognizer.write('modeloEigenFace.xml')
print("IA ENTRENADA")