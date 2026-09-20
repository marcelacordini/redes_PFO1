💻 PFO 1 — Programación sobre Redes
Chat Cliente-Servidor con Sockets TCP/IP y SQLite

Repositorio correspondiente a la Práctica Formativa Obligatoria 1 (PFO1) de la materia Programación sobre Redes.

El proyecto implementa un sistema de comunicación cliente-servidor utilizando sockets TCP/IP en Python, con una arquitectura modular y persistencia automática de los mensajes intercambiados mediante SQLite.

👩‍💻 Alumna

Nombre: Marcela Cordini

Carrera: Tecnicatura en Desarrollo de Software

Institución: IFTS 29

🎯 Objetivos del trabajo

El proyecto tiene como objetivo implementar una aplicación de red que cumpla con los siguientes requerimientos:

Configurar un socket servidor en localhost:5000.

Separar la lógica mediante funciones independientes.

Aceptar conexiones de clientes mediante TCP/IP.

Permitir el envío de múltiples mensajes durante una misma sesión.

Persistir automáticamente cada mensaje recibido en SQLite.

Registrar:

contenido del mensaje;

fecha y hora de envío;

dirección IP del cliente.

Responder al cliente con el formato:

Mensaje recibido: <timestamp>


Incorporar manejo de excepciones y errores.

Permitir finalizar la sesión mediante la palabra clave éxito.

🛠️ Tecnologías utilizadas
Tecnología	Uso
Python 3.x	Lenguaje principal
socket	Comunicación TCP/IP
sqlite3	Persistencia de datos
datetime	Registro de timestamps
Git / GitHub	Control de versiones y repositorio
📁 Estructura del repositorio
redes_PFO1/
│
├── img/
│   ├── base-datos.png
│   ├── cliente-funcionado.png
│   └── servidor-funcionando.png
│
├── .gitignore
├── client.py
├── server.py
└── README.md


Nota: La base de datos chat_pfo1.db se genera automáticamente al iniciar el servidor por primera vez.

🏗️ Funcionamiento del sistema

La aplicación está compuesta por dos scripts principales:

🖥️ server.py

Se encarga de:

Inicializar la base de datos SQLite.

Crear la tabla mensajes.

Configurar el socket TCP.

Escuchar conexiones en localhost:5000.

Aceptar conexiones de clientes.

Obtener la dirección IP del cliente.

Guardar los mensajes recibidos.

Enviar la confirmación correspondiente.

💬 client.py

Se encarga de:

Establecer la conexión TCP con el servidor.

Permitir al usuario ingresar mensajes.

Enviar múltiples mensajes durante una misma sesión.

Mostrar las respuestas recibidas.

Finalizar la conexión cuando se ingresa éxito.

⚙️ Configuración predeterminada
HOST: localhost
PUERTO: 5000

🚀 Ejecución
1. Iniciar el servidor

Abrir una terminal dentro del directorio del proyecto y ejecutar:

python server.py


El servidor quedará escuchando conexiones en:

localhost:5000

2. Iniciar el cliente

Abrir una segunda terminal y ejecutar:

python client.py

💬 Ejemplo de interacción
[CLIENTE] Conectando al servidor localhost:5000...
[CLIENTE] Conexión establecida con éxito.

--- Chat Iniciado ---
Escribí tus mensajes a continuación.
Ingresá 'éxito' para salir.

Ingrese mensaje: hola servidor
[RESPUESTA SERVIDOR] -> Mensaje recibido: 2026-09-20 12:15:00

Ingrese mensaje: ¿Cómo estás?
[RESPUESTA SERVIDOR] -> Mensaje recibido: 2026-09-20 12:15:10

Ingrese mensaje: éxito
[CLIENTE] Finalizando sesión de chat...

🗄️ Persistencia de datos

Los mensajes recibidos se almacenan automáticamente en:

chat_pfo1.db


Dentro de la tabla:

mensajes

Esquema de la tabla
Columna	Tipo	Descripción
id	INTEGER PRIMARY KEY AUTOINCREMENT	Identificador único
contenido	TEXT NOT NULL	Mensaje enviado por el cliente
fecha_envio	TEXT NOT NULL	Fecha y hora del registro
ip_cliente	TEXT NOT NULL	Dirección IP del cliente
🖼️ Evidencias de funcionamiento
Servidor funcionando

Cliente funcionando

Registros almacenados en SQLite

🛡️ Manejo de excepciones

El proyecto incorpora bloques try-except para controlar errores habituales durante la ejecución.

ConnectionRefusedError

Se utiliza para detectar cuando el cliente intenta conectarse y el servidor todavía no está disponible.

OSError

Permite controlar problemas relacionados con el socket, como un puerto ocupado al intentar iniciar el servidor.

Errores de SQLite

Se contemplan excepciones relacionadas con la creación, lectura o escritura de la base de datos para evitar interrupciones inesperadas.

🧪 Guía rápida de prueba
Clonar el repositorio
git clone https://github.com/marcelacordini/redes_PFO1.git
cd redes_PFO1

Terminal 1 — Servidor
python server.py

Terminal 2 — Cliente
python client.py


Luego:

Escribir uno o varios mensajes.

Verificar que el servidor responda con el timestamp correspondiente.

Ingresar éxito para finalizar la sesión.

Comprobar que los mensajes hayan sido almacenados en chat_pfo1.db.

📌 Resultado

El proyecto implementa una comunicación cliente-servidor mediante TCP/IP, permitiendo el intercambio de múltiples mensajes durante una misma conexión y almacenando cada mensaje recibido junto con su timestamp y la IP del cliente en una base de datos SQLite.
