import socket
from persona import Persona  # Importa el objeto Persona


registrados = []
rechazados = []

def separar_informacion(datos):
    nombre, apellido, edad, rut = datos.split(";")
    return nombre, apellido, edad, rut


def combinar_nombre(nombre, apellido):
    return f"{str.capitalize(nombre)} {str.capitalize(apellido)}"

def limpiar_rut(rut):
    return rut.replace('.', '').replace('-', '')

def calcular_digito_verificador(rut):
    rut = limpiar_rut(rut)[:-1]
    reversed_digits = map(int, reversed(rut))
    factors = [2, 3, 4, 5, 6, 7]
    s = sum(d * f for d, f in zip(reversed_digits, factors * 2))
    mod = 11 - s % 11
    if mod == 11:
        return '0'
    elif mod == 10:
        return 'k'
    else:
        return str(mod)

def validar_rut(rut):
    rut = limpiar_rut(rut)
    if len(rut) < 2:
        return False
    cuerpo = rut[:-1]
    digito_verificador = rut[-1].lower()
    if not cuerpo.isdigit() or (digito_verificador != 'k' and not digito_verificador.isdigit()):
        return False
    return calcular_digito_verificador(rut) == digito_verificador

def validar_informacion(datos):
    nombre, apellido, edad, rut = separar_informacion(datos)
    if not validar_rut(rut):
        return "El formato rut es inválido"
    elif int(edad) < 18:
        return "Menor de edad"
    else:
        nombre_completo = combinar_nombre(nombre, apellido)
        persona = Persona(nombre_completo, edad, rut)
        registrados.append(persona)
        return "Registro exitoso"


def habilitar_server():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        servidor_socket.bind(('localhost', 15000))
        servidor_socket.listen()
        print("El registro civil está en servicio")
    except socket.error as e:
        print(f"Error al configurar el servidor: {e}")
        servidor_socket = None
    return servidor_socket


def main():
    servidor_socket = habilitar_server()
    if not servidor_socket:
        return 

    while True:
        connection_socket, _ = servidor_socket.accept()
        
        try:
            message = connection_socket.recv(1024).decode()
            print(f"Mensaje recibido: {message}")
        
            modified_message = validar_informacion(message)
            print(f"Mensaje modificado: {modified_message}")
        
            connection_socket.send(modified_message.encode())
            print("Mensaje enviado al cliente")
        
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            connection_socket.close()


if __name__ == "__main__":
    main()