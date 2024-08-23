import socket

def agregar_civil():
    nombre = input("Ingresar nombre: ")
    apellido = input("Ingresar apellido: ")
    edad = input("Ingresar edad: ")
    rut = input("Ingresar rut: ")
    return concatener_datos(nombre, apellido, edad, rut)


def concatener_datos(nombre, apellido, edad, rut):
    return f"{nombre};{apellido};{edad};{rut}"


def habilitar_cliente():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', 15000))
    except socket.error as e:
        print(f"Error al conectar con el servidor: {e}")
        client_socket = None
    return client_socket


def main():
    client_socket = habilitar_cliente()
    if client_socket:
        message = agregar_civil()
        client_socket.send(message.encode())

        modified_message = client_socket.recv(1024).decode()
        print(f"Respuesta del servidor: {modified_message}")

        client_socket.close()


if __name__ == "__main__":
    main()