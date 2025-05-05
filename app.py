
from flask import Flask, request, jsonify
import json
import os
from cryptography.fernet import Fernet

app = Flask(__name__)

CLAVE_CIFRADO = b'8L_FI3qCduGzj-mJXtU7gK-K1vb3UdFFfxqccZ0AiP0='  # NO CAMBIAR
fernet = Fernet(CLAVE_CIFRADO)

if not os.path.exists("usuarios.json"):
    with open("usuarios.json", "w") as f:
        json.dump({}, f)

with open("usuarios.json", "r") as f:
    db = json.load(f)

@app.route('/')
def home():
    return 'Servidor funcionando correctamente.'

@app.route('/verificar', methods=['POST'])
def verificar():
    data = request.json
    correo = data.get('correo')

    if not correo:
        return jsonify({'error': 'Correo no proporcionado'}), 400

    if correo not in db:
        return jsonify({'valido': False})

    usuario = db[correo]
    creditos = usuario.get("creditos", 0)
    return jsonify({'valido': True, 'creditos': creditos})

@app.route('/clave', methods=['POST'])
def obtener_clave():
    data = request.json
    correo = data.get('correo')

    if not correo:
        return jsonify({'error': 'Correo no proporcionado'}), 400

    usuario = db.get(correo)
    if not usuario or "clave" not in usuario:
        return jsonify({'error': 'Clave no encontrada'}), 404

    claves = usuario["clave"]
    cifradas = [fernet.encrypt(clave.encode()).decode() for clave in claves]
    return jsonify({'claves': cifradas})

@app.route('/asignar_keys', methods=['POST'])
def asignar_keys():
    data = request.json
    correo = data.get('correo')
    claves = data.get('claves')

    if not correo or not claves or not isinstance(claves, list):
        return jsonify({'error': 'Datos inválidos'}), 400

    with open("usuarios.json", "r") as f:
        db = json.load(f)

    if correo not in db:
        db[correo] = {}

    db[correo]["clave"] = claves

    with open("usuarios.json", "w") as f:
        json.dump(db, f, indent=4)

    return jsonify({'mensaje': f'Claves asignadas a {correo} correctamente.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

