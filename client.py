import socket

# ============================================================
# CONFIGURACIÓN Y EJECUCIÓN DEL CLIENTE
# ============================================================

def ejecutar_cliente(host="localhost", port=5000):
    """
    Conecta el cliente al servidor y permite enviar múltiples mensajes durante una misma sesión.
    """

    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        print(
            f"[CLIENTE] Conectando al servidor "
            f"{host}:{port}..."
        )

        # Establezco la conexión con el servidor.
        client_socket.connect((host, port))

        print("[CLIENTE] Conexión establecida con éxito.\n")

        print("--- Chat Iniciado ---")
        print(
            "Escribí tus mensajes a continuación. "
            "Ingresá 'éxito' para salir.\n"
        )

        while True:
            mensaje = input("Ingrese mensaje: ")

            # No permito enviar mensajes vacíos.
            if not mensaje.strip():
                print(
                    "[AVISO] No se pueden enviar mensajes vacíos.\n"
                )
                continue

            # Envio el mensaje al servidor.
            client_socket.sendall(
                mensaje.encode("utf-8")
            )

            # Si el usuario escribe "éxito", finaliza la sesión después de avisar al servidor.
            if mensaje.strip().lower() == "éxito":
                print(
                    "\n[CLIENTE] Finalizando sesión de chat..."
                )
                break

            # Espera la respuesta del servidor.
            respuesta = client_socket.recv(1024)

            if not respuesta:
                print(
                    "[CLIENTE] El servidor cerró la conexión."
                )
                break

            respuesta = respuesta.decode("utf-8")

            print(
                f"[RESPUESTA SERVIDOR] -> {respuesta}\n"
            )

    except ConnectionRefusedError:
        print(
            f"[ERROR CLIENTE] No se pudo conectar al servidor "
            f"en {host}:{port}."
        )
        print(
            "Asegurate de que 'server.py' esté ejecutándose en otra terminal."
        )

    except OSError as e:
        print(
            f"[ERROR CLIENTE] Error de conexión: {e}"
        )

    except KeyboardInterrupt:
        print(
            "\n[CLIENTE] Sesión interrumpida por el usuario."
        )

    except Exception as e:
        print(
            f"[ERROR CLIENTE] Error inesperado: {e}"
        )

    finally:
        # Cierro el socket del cliente.
        client_socket.close()
        print("[CLIENTE] Socket del cliente cerrado.")


# ============================================================
# PUNTO DE ENTRADA DEL CLIENTE
# ============================================================

if __name__ == "__main__":
    ejecutar_cliente()