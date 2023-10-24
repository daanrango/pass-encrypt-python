from flask import Flask, jsonify, request
import base64
from connection import conection_mysql
from encrypt import generar_clave, guardar_contrasena_encriptada, desencriptar_contrasena

app = Flask(__name__)


@app.route('/', methods=['GET'])
def ping():
    return jsonify({"response": "hello world"})


@app.route("/encrypt", methods=["POST"])
def save_password():
    try:
        contrasena = request.json["contrasena"]
        connection = conection_mysql()
        cursor = connection.cursor()
        query = "SELECT clave, contrasena_encriptada FROM passwordsEncrypt"
        cursor.execute(query)
        results = cursor.fetchall()

        for result in results:
            clave_guardada = result[0]
            contrasena_encriptada = result[1]
            contrasena_desencriptada = desencriptar_contrasena(
                clave_guardada, contrasena_encriptada)
            if contrasena_desencriptada == contrasena:
                return jsonify({"mensaje": "La contraseña ya se guardo anteriormente en la base de datos.", "contrasena": contrasena})

        clave = generar_clave()
        contrasena_encriptada = guardar_contrasena_encriptada(
            clave, contrasena)
        query = "INSERT INTO passwordsEncrypt (clave, contrasena_encriptada) VALUES (%s, %s)"
        cursor.execute(query, (clave, contrasena_encriptada))
        connection.commit()
        cursor.close()
        # Solo para la respuesta
        clave = base64.b64encode(clave).decode()
        contrasena_encriptada = base64.b64encode(
            contrasena_encriptada).decode()
        return jsonify({"mensaje": "La contraseña se guardo en la base de datos.", "clave": clave, "contrasena_encriptada": contrasena_encriptada, "contrasena": contrasena})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
