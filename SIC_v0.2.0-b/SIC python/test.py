import requests

url = "http://127.0.0.1:80/facial_recognition" # Reemplaza esto con la URL de tu página que contiene el JSON
response = requests.get(url)

if response.ok:
    print(response.text)  # Esto imprimirá el JSON en formato Python
else:
    print("Error al obtener la respuesta:", response.status_code)
