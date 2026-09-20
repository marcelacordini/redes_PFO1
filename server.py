import socket
import sqlite3
from datetime import datetime


# ============================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================================

def init_db(db_name="chat_pfo1.db"):
    """
    Inicializa la base de datos SQLite y crea la tabla
    mensajes si todavía no existe.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Creación de la tabla donde se almacenan los mensajes.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

        print(f"[BD] Base de datos '{db_name}' inicializada correctamente.")
        return True

    except sqlite3.Error as e:
        print(f"[ERROR BD] No se pudo inicializar la base de datos: {e}")
        return False


# ============================================================
# GUARDADO DE MENSAJES EN SQLITE
# ============================================================

def guardar_mensaje(contenido, fecha_envio, ip_cliente,
                    db_name="chat_pfo1.db"):
    """
    Guarda un mensaje recibido junto con su fecha/hora y la dirección IP del cliente.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Consulta parametrizada para insertar el mensaje.
        cursor.execute("""
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        """, (contenido, fecha_envio, ip_cliente))

        conn.commit()
        conn.close()

        print(f"[BD] Mensaje guardado correctamente desde IP {ip_cliente}.")
        return True

    except sqlite3.Error as e:
        print(f"[ERROR BD] No se pudo guardar el mensaje: {e}")
        return False


# ============================================================
# CONFIGURACIÓN DEL SOCKET TCP/IP
# ============================================================

def init_socket(host="localhost", port=5000):
    """
    Crea e inicializa el socket del servidor.
    """
    try:
        # AF_INET indica que utilizaremos IPv4.
        # SOCK_STREAM indica que utilizaremos TCP.
        server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        # Permite reutilizar rápidamente el puerto al reiniciar el servidor después de cerrar una conexión.
        server_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        # El servidor queda asociado a localhost:5000.
        server_socket.bind((host, port))

        # El servidor comienza a escuchar conexiones entrantes.
        # El valor 5 indica el máximo de conexiones pendientes.
        server_socket.listen(5)

        print(f"[SERVIDOR] Servidor escuchando en {host}:{port}")

        return server_socket

    except OSError as e:
        print(
            f"[ERROR SOCKET] No se pudo iniciar el servidor "
            f"en {host}:{port}: {e}"
        )
        return None


# ============================================================
# ACEPTAR CONEXIONES Y RECIBIR MENSAJES
# ============================================================

def atender_clientes(server_socket):
    """
    Acepta conexiones de clientes y procesa los mensajes enviados durante la sesión.
    """
    while True:
        try:
            print("\n[SERVIDOR] Esperando nueva conexión...")

            # accept() devuelve:
            # conn -> socket utilizado para comunicarse con el cliente.
            # addr -> tupla con IP y puerto del cliente.
            conn, addr = server_socket.accept()

            ip_cliente = addr[0]
            puerto_cliente = addr[1]

            print(
                f"[SERVIDOR] Conexión aceptada desde "
                f"{ip_cliente}:{puerto_cliente}"
            )

            # with garantiza el cierre de la conexión.
            with conn:

                while True:
                    try:
                        # Recibohasta 1024 bytes.
                        data = conn.recv(1024)

                        # Si no recibo datos, el cliente cerró la conexión.
                        if not data:
                            print(
                                f"[SERVIDOR] El cliente {ip_cliente} "
                                "cerró la conexión."
                            )
                            break

                        mensaje = data.decode("utf-8").strip()

                        print(
                            f"[RECIBIDO] Mensaje: '{mensaje}' "
                            f"de {ip_cliente}"
                        )

                        # La palabra "éxito" finaliza la sesión.
                        if mensaje.lower() == "éxito":
                            print(
                                f"[SERVIDOR] El cliente {ip_cliente} "
                                "finalizó la sesión."
                            )
                            break

                        # Genero el timestamp del mensaje.
                        timestamp = datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )

                        # Guardo el mensaje en SQLite.
                        guardado = guardar_mensaje(
                            mensaje,
                            timestamp,
                            ip_cliente
                        )

                        # Solamente envio la confirmación si el mensaje pudo almacenarse correctamente.
                        if guardado:
                            respuesta = (
                                f"Mensaje recibido: {timestamp}"
                            )

                            conn.sendall(
                                respuesta.encode("utf-8")
                            )
                        else:
                            respuesta = (
                                "Error: no se pudo guardar "
                                "el mensaje en la base de datos."
                            )

                            conn.sendall(
                                respuesta.encode("utf-8")
                            )

                    except UnicodeDecodeError:
                        print(
                            "[ERROR] No se pudo interpretar "
                            "el mensaje recibido."
                        )

                        conn.sendall(
                            "Error: mensaje inválido.".encode("utf-8")
                        )

                    except OSError as e:
                        print(
                            f"[ERROR CONEXIÓN] Problema en la "
                            f"comunicación con {ip_cliente}: {e}"
                        )
                        break

        except OSError as e:
            print(
                f"[ERROR SERVIDOR] Error al aceptar la conexión: {e}"
            )


# ============================================================
# PUNTO DE ENTRADA DEL SERVIDOR
# ============================================================

if __name__ == "__main__":

    # Inicializa la base de datos.
    if not init_db():
        print(
            "[SERVIDOR] No se puede iniciar el servidor "
            "porque la base de datos no está disponible."
        )

    else:
        # Inicializa el socket en localhost:5000.
        servidor_socket = init_socket(
            host="localhost",
            port=5000
        )

        if servidor_socket:
            try:
                # Comienza a aceptar conexiones.
                atender_clientes(servidor_socket)

            except KeyboardInterrupt:
                print(
                    "\n[SERVIDOR] Servidor detenido manualmente."
                )

            finally:
                # Cierro el socket al finalizar el servidor.
                servidor_socket.close()
                print("[SERVIDOR] Socket cerrado.")