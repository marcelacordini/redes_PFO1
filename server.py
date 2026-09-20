import socket
import sqlite3
from datetime import datetime


# 1. INICIALIZACIÓN DE LA BASE DE DATOS

def init_db(db_name="chat_pfo1.db"):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"[BD] Base de datos '{db_name}' inicializada correctamente.")
    except Exception as e:
        print(f"[ERROR BD] Error al inicializar la base de datos: {e}")

# 2. PERSISTENCIA DE MENSAJES EN SQLITE

def guardar_mensaje(contenido, ip_cliente, db_name="chat_pfo1.db"):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_str = str(ip_cliente)  # Garantizamos que la IP sea texto plano
        
        cursor.execute('''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        ''', (contenido, fecha_actual, ip_str))
        
        conn.commit()
        conn.close()
        print(f"[BD] Mensaje '{contenido}' guardado desde IP {ip_str}.")
    except Exception as e:
        print(f"[ERROR BD] No se pudo guardar el mensaje: {e}")

# 3. INICIALIZACIÓN DEL SOCKET DEL SERVIDOR

def init_socket(host="localhost", port=5000):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"[SERVIDOR] Servidor escuchando en {host}:{port}")
        return server_socket
    except OSError as e:
        print(f"[ERROR SOCKET] No se pudo iniciar el servidor en el puerto {port}: {e}")
        return None

# 4. ATENCIÓN DE CLIENTES Y RECEPCIÓN

def atender_clientes(server_socket):
    while True:
        try:
            print("\n[SERVIDOR] Esperando nueva conexión...")
            conn, addr = server_socket.accept()
            
            # addr es una tupla: (IP, Puerto), extraemos la IP en addr[0]
            ip_cliente = addr[0]
            puerto_cliente = addr[1]
            print(f"[SERVIDOR] Conexión aceptada desde IP: {ip_cliente}, Puerto: {puerto_cliente}")
            
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print(f"[SERVIDOR] El cliente {ip_cliente} cerró la conexión.")
                        break
                    
                    mensaje_texto = data.decode('utf-8').strip()
                    print(f"[RECIBIDO] Mensaje: '{mensaje_texto}' de {ip_cliente}")
                    
                    # Si el cliente envía 'éxito', finalizamos la atención
                    if mensaje_texto.lower() == "éxito":
                        print(f"[SERVIDOR] El cliente {ip_cliente} envió 'éxito'. Cerrando conexión.")
                        break
                    
                    # 1. Guardar en SQLite
                    guardar_mensaje(mensaje_texto, ip_cliente)
                    
                    # 2. Generar y enviar respuesta
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    respuesta = f"Mensaje recibido: {timestamp}"
                    conn.sendall(respuesta.encode('utf-8'))
                    
        except Exception as e:
            print(f"[ERROR SERVIDOR] Ocurrió un error atendiendo al cliente: {e}")

# 5. PUNTO DE ENTRADA PRINCIPAL

if __name__ == "__main__":
    init_db()
    servidor_socket = init_socket(host="localhost", port=5000)
    if servidor_socket:
        try:
            atender_clientes(servidor_socket)
        except KeyboardInterrupt:
            print("\n[SERVIDOR] Servidor detenido manualmente.")
        finally:
            servidor_socket.close()
            print("[SERVIDOR] Socket cerrado.")