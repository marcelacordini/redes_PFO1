PFO 1 - Programación sobre RedesChat Básico Cliente-Servidor con Sockets y SQLiteEste repositorio contiene la resolución de la Práctica Formativa Obligatoria 1 (PFO1) para la materia Programación sobre Redes.El propósito de esta práctica consiste en desarrollar un sistema de red bajo el paradigma cliente-servidor empleando sockets TCP/IP en Python, estructurado de manera modular para garantizar la persistencia automática de los mensajes intercambiados en una base de datos SQLite.AlumnaNombre: Marcela CordiniCarrera: Tecnicatura en Desarrollo de Software - IFTS 29Objetivos del TrabajoImplementar una aplicación de red robusta que cumpla con los siguientes lineamientos técnicos:Configurar y levantar un socket servidor a la escucha en localhost:5000.Dividir la lógica mediante funciones independientes para la inicialización del socket, la aceptación de conexiones y el almacenamiento en base de datos.Conectar un cliente interactivo capaz de enviar múltiples mensajes de forma consecutiva durante la misma sesión.Almacenar cada mensaje recibido de forma estructurada en SQLite registrando el contenido, la fecha de envío (timestamp) y la dirección IP de origen del cliente.Responder de vuelta al cliente con el formato de confirmación estricto: Mensaje recibido: <timestamp>.Incorporar control de excepciones y manejo de errores (puertos ocupados, problemas de acceso a la base de datos o fallas de conexión).Habilitar una palabra clave de salida (éxito) para cerrar el canal de comunicación de manera limpia.Tecnologías y EntornoPython 3.xSockets TCP/IP (socket)Base de Datos Relacional (sqlite3)Control de Tiempo (datetime)Git y GitHubEstructura del RepositorioPlaintextpfo1-programacion-sobre-redes/
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
Escribí tus mensajes a continuación. Ingresá 'éxito' para salir.

Ingrese mensaje: hola servidor
[RESPUESTA SERVIDOR] -> Mensaje recibido: 2026-09-20 12:15:00

Ingrese mensaje: éxito
[CLIENTE] Finalizando sesión de chat...
Cliente en Ejecución3. Persistencia de Datos (SQLite)Los registros de comunicación se guardan automáticamente en la base de datos chat_pfo1.db dentro de la tabla mensajes, la cual cuenta con el siguiente esquema relacional:ColumnaTipo de DatoDescripciónidINTEGER PRIMARY KEY AUTOINCREMENTIdentificador único autoincremental.contenidoTEXT NOT NULLTexto del mensaje enviado por el cliente.fecha_envioTEXT NOT NULLMarca temporal (timestamp) del momento exacto del registro.ip_clienteTEXT NOT NULLDirección IP del cliente conectado.Registros AlmacenadosManejo de ExcepcionesEl código contempla bloques de control estructurados (try-except) para mitigar fallos comunes en redes locales:ConnectionRefusedError: Detecta si el cliente intenta conectarse antes de que el servidor esté activo, informando al usuario de manera clara.OSError: Controla conflictos si el puerto 5000 se encuentra ocupado por otro proceso al iniciar el servidor.Errores de Base de Datos: Captura excepciones de escritura o lectura en SQLite para evitar caídas imprevistas del núcleo de red.Guía Rápida de Prueba LocalClonar e ingresar al repositorio:Bashgit clone <url-de-tu-repositorio>
cd pfo1-programacion-sobre-redes
Terminal 1 - Iniciar el servidor:Bashpython server.py
Terminal 2 - Iniciar el cliente:Bashpython client.py
Escribe tus mensajes y comprueba la respuesta del servidor. Escribe éxito para finalizar.