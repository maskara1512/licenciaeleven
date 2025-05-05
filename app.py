from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

RUTA_DB = "db_keys.json"

# Cargar o crear base de datos
if os.path.exists(RUTA_DB):
    with open(RUTA_DB, "r") as f:
        db = json.load(f)
else:
    db = {}

@app.route("/get_api_key", methods=["GET"])
def get_api_key():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Falta el parámetro 'email'"}), 400

    api_key = db.get(email)
    if api_key:
        return jsonify({"api_key": api_key}), 200
    else:
        return jsonify({"error": "Correo no registrado"}), 404

@app.route("/add_api_key", methods=["POST"])
def add_api_key():
    data = request.get_json()
    email = data.get("email")
    api_key = data.get("api_key")

    if not email or not api_key:
        return jsonify({"error": "Faltan campos 'email' o 'api_key'"}), 400

    db[email] = api_key
    with open(RUTA_DB, "w") as f:
        json.dump(db, f, indent=2)

    return jsonify({"message": "API key guardada correctamente"}), 200

if __name__ == "__main__":
    app.run()
