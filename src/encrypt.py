from cryptography.fernet import Fernet


def generar_clave():
    return Fernet.generate_key()


def guardar_contrasena_encriptada(clave, contrasena):
    f = Fernet(clave)
    contrasena_encriptada = f.encrypt(contrasena.encode())
    return contrasena_encriptada


def desencriptar_contrasena(clave, contrasena_encriptada):
    f = Fernet(clave)
    contrasena = f.decrypt(contrasena_encriptada).decode()
    return contrasena


if __name__ == "__main__":
    clave = generar_clave()
    print("Generada clave de encriptación:", clave.decode())

    contrasena = input("Ingresa tu contraseña: ")
    contrasena_encriptada = guardar_contrasena_encriptada(clave, contrasena)
    print("Contraseña encriptada:", contrasena_encriptada)

    input("Presiona Enter para desencriptar la contraseña...")

    contrasena_desencriptada = desencriptar_contrasena(
        clave, contrasena_encriptada)
    print("Contraseña desencriptada:", contrasena_desencriptada)
