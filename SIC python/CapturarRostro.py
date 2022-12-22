import cv2
import os
import imutils

personName = 'Pollo'
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