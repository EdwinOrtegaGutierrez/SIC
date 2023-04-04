import cv2
import os
import numpy as np
import imutils

def CapturarRostro(personName):
    myPath = os.path.dirname(os.path.abspath(__file__))
    dataPath = f'{myPath}/Data'
    personPath = dataPath + '/' + personName

    if not os.path.exists(personPath):
        print("Creando carpeta: ", personName)
        os.makedirs(personPath)

    camara = cv2.VideoCapture(0)
    faceClassif = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'))
    count = 0

    while True:
        ret, frame = camara.read()
        if ret == False: break
        frame = imutils.resize(frame, width=800)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = frame.copy()

        faces = faceClassif.detectMultiScale(gray, 1.3, 1)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x-50,y-50), (x+w, y+h), (0,255,0), 2)
            rostro = auxFrame[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (150,150), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(personPath + '/rostro_{}.jpg'.format(count), rostro)
            count = count + 1

        cv2.imshow('frame', frame)

        k = cv2.waitKey(1)
        if (k == 27) or (count >= 500): 
            break

    camara.release()
    cv2.destroyAllWindows()

def EntrenadorRF():
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

def Reconocimiento():
    myPath = os.path.dirname(os.path.abspath(__file__))
    dataPath = f'{myPath}/Data'
    imagePath = os.listdir(dataPath)

    face_recognizer = cv2.face.EigenFaceRecognizer_create()

    face_recognizer.read('modeloEigenFace.xml')

    cap = cv2.VideoCapture(0)

    faceClassif = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'))

    while True:
            ret, frame = cap.read()
            if ret == False: break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = gray.copy()
        
            faces = faceClassif.detectMultiScale(gray, 1.3, 5)
            
            for (x,y,w,h) in faces:
                rostro = auxFrame[y:y+h, x:x+w]
                rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
                result = face_recognizer.predict(rostro)
                
                cv2.putText(frame, '{}'.format(result), (x, y-5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
                
                if result[1] < 27700:
                    cv2.putText(frame, '{}'.format(imagePath[result[0]]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
                else:
                    cv2.putText(frame, 'Desconocido', (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
            
            cv2.imshow('frame', frame)
            k = cv2.waitKey(1)
            if k == 27:
                break
            
    cap.release()
    cv2.destroyAllWindows()