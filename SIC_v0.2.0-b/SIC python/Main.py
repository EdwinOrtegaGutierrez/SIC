from flask import Flask
from FaceIA import FaceDetection

app = Flask(__name__)

app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)

IA = FaceDetection

@app.route('/facial_recognition')
def facial_recognition():
    return IA.Reconocimiento()

if __name__ == "__main__":
    #app.secret_key = 'super secret key' #NECESARIO PARA MANDAR MENSAJES PRIVADOS
    app.run(
        host = '0.0.0.0', 
        port=80,
        debug=False)