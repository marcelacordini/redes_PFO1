import socket

def ejecutar_cliente(host="localhost", port=5000):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[CLIENTE] Conectando al servidor {host}:{port}...")
        client_socket.connect((host, port))
        print("[CLIENTE] Conexión establecida con éxito.\n")
        print("--- Chat Iniciado ---")
        print("Escribí tus mensajes a continuación. Ingresá 'éxito' para salir.\n")
        
        while True:
            mensaje = input("Ingrese mensaje: ")
            
            # Si el usuario ingresa 'éxito', avisamos al servidor y salimos
            if mensaje.strip().lower() == "éxito":
                client_socket.sendall(mensaje.encode('utf-8'))
                print("\n[CLIENTE] Finalizando sesión de chat...")
                break
            
            if not mensaje.strip():
                print("[AVISO] No se pueden enviar mensajes vacíos.")
                continue
            
            # Enviar mensaje al servidor
            client_socket.sendall(mensaje.encode('utf-8'))
            
            # Recibir respuesta del servidor
            respuesta = client_socket.recv(1024).decode('utf-8')
            print(f"[RESPUESTA SERVIDOR] -> {respuesta}\n")
            
        client_socket.close()
        print("[CLIENTE] Socket del cliente cerrado.")

    except ConnectionRefusedError:
        print(f"[ERROR CLIENTE] No se pudo conectar al servidor en {host}:{port}.")
        print("Asegurate de que 'server.py' esté ejecutándose en otra terminal.")
    except Exception as e:
        print(f"[ERROR CLIENTE] Error inesperado: {e}")

if __name__ == "__main__":
    ejecutar_cliente()