from flask import Flask, request, jsonify

app = Flask(__name__)

# Lista de correos permitidos
correos_autorizados = {"usuario1@example.com", "usuario2@example.com"}

@app.route('/verificar_usuario')
def verificar_usuario():
    correo = request.args.get('correo')
    autorizado = correo in correos_autorizados
    return jsonify({"autorizado": autorizado})