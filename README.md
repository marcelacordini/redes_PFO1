# 💻 PFO 1 — Programación sobre Redes

## Chat Cliente-Servidor con Sockets TCP/IP y SQLite

Repositorio correspondiente a la **Práctica Formativa Obligatoria 1 (PFO1)** de la materia **Programación sobre Redes**.

El proyecto implementa un sistema de comunicación **cliente-servidor** utilizando **sockets TCP/IP en Python**, con una arquitectura modular y persistencia automática de los mensajes intercambiados mediante **SQLite**.

---

## 👩‍💻 Alumna

* **Nombre:** Marcela Cordini
* **Carrera:** Tecnicatura en Desarrollo de Software
* **Institución:** IFTS 29

---

## 🎯 Objetivos del trabajo

El proyecto tiene como objetivo implementar una aplicación de red que cumpla con los siguientes requerimientos:

* Configurar un socket servidor en `localhost:5000`.
* Separar la lógica mediante funciones independientes.
* Aceptar conexiones de clientes mediante TCP/IP.
* Permitir el envío de múltiples mensajes durante una misma sesión.
* Persistir automáticamente cada mensaje recibido en SQLite.
* Registrar:

  * contenido del mensaje;
  * fecha y hora de envío;
  * dirección IP del cliente.
* Responder al cliente con el formato:

```text
Mensaje recibido: <timestamp>
```

* Incorporar manejo de excepciones y errores.
* Permitir finalizar la sesión mediante la palabra clave `éxito`.

---

## 🛠️ Tecnologías utilizadas

| Tecnología       | Uso                                |
| ---------------- | ---------------------------------- |
| **Python 3.x**   | Lenguaje principal                 |
| **socket**       | Comunicación TCP/IP                |
| **sqlite3**      | Persistencia de datos              |
| **datetime**     | Registro de timestamps             |
| **Git / GitHub** | Control de versiones y repositorio |

---

## 📁 Estructura del repositorio

```text
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
Nota: La base de datos local chat_pfo1.db se genera de forma automatizada al iniciar el servidor por primera vez.Funcionamiento del SistemaLa arquitectura está compuesta por dos scripts principales que operan de manera independiente en la red local:server.py: Encargado de inicializar la estructura de SQLite, abrir el puerto de escucha y procesar la persistencia de datos.client.py: Interfaz de terminal que permite interactuar enviando cadenas de texto y recibiendo las confirmaciones temporales del servidor.Los parámetros de enlace predeterminados son:PlaintextHOST: localhost
PUERTO: 5000
1. Módulo Servidor (server.py)El servidor ejecuta funciones modularizadas para separar responsabilidades:Inicialización y creación de la tabla mensajes en SQLite.Configuración del socket con la directiva SO_REUSEADDR para evitar bloqueos de puertos reutilizados.Bucle de escucha permanente para aceptar nuevas conexiones de clientes y extraer su dirección IP real.Para ponerlo en marcha:Bashpython server.py
Servidor en Ejecución2. Módulo Cliente (client.py)El cliente establece el canal TCP con el servidor y gestiona el flujo de envío mediante un bucle interactivo:Para ejecutarlo se requiere abrir una terminal secundaria:Bashpython client.py
Ejemplo de interacción en consola:Plaintext[CLIENTE] Conectando al servidor localhost:5000...
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
Cliente en Ejecución3. Persistencia de Datos (SQLite)Los registros de comunicación se guardan automáticamente en la base de datos chat_pfo1.db dentro de la tabla mensajes, la cual cuenta con el siguiente esquema relacional:ColumnaTipo de DatoDescripciónidINTEGER PRIMARY KEY AUTOINCREMENTIdentificador único autoincremental.contenidoTEXT NOT NULLTexto del mensaje enviado por el cliente.fecha_envioTEXT NOT NULLMarca temporal (timestamp) del momento exacto del registro.ip_clienteTEXT NOT NULLDirección IP del cliente conectado.Registros AlmacenadosManejo de ExcepcionesEl código contempla bloques de control estructurados (try-except) para mitigar fallos comunes en redes locales:ConnectionRefusedError: Detecta si el cliente intenta conectarse antes de que el servidor esté activo, informando al usuario de manera clara.OSError: Controla conflictos si el puerto 5000 se encuentra ocupado por otro proceso al iniciar el servidor.Errores de Base de Datos: Captura excepciones de escritura o lectura en SQLite para evitar caídas imprevistas del núcleo de red.Guía Rápida de Prueba LocalClonar e ingresar al repositorio:Bashgit clone <url-de-tu-repositorio>
cd pfo1-programacion-sobre-redes
Terminal 1 - Iniciar el servidor:Bashpython server.py
Terminal 2 - Iniciar el cliente:Bashpython client.py
Escribe tus mensajes y comprueba la respuesta del servidor. Escribe éxito para finalizar.