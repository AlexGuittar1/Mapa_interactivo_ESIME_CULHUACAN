# Mapa Interactivo ESIME Culhuacan


## INTRODUCCION

Este proyecto es una aplicacion web completa que permite a los estudiantes de la Escuela Superior de Ingenieria Mecanica y Electrica (ESIME) Culhuacan navegar dentro del campus de forma interactiva.

Un mapa interactivo es una representacion visual digital de un espacio fisico que responde a las acciones del usuario. A diferencia de un mapa impreso, un mapa interactivo permite hacer zoom, buscar lugares, calcular rutas y ver informacion en tiempo real. Es el mismo concepto que usan aplicaciones como Google Maps o Waze, pero aplicado a un espacio mas pequeno: un campus universitario.

La navegacion dentro de campus es un problema real en instituciones educativas grandes. Cuando un estudiante nuevo llega a ESIME Culhuacan, se enfrenta a un terreno extenso con multiples edificios, laboratorios, areas deportivas y estacionamientos. Sin un sistema de orientacion, puede tardar semanas en aprender donde esta cada lugar.

Los sistemas de rutas son importantes porque optimizan el tiempo de desplazamiento. En una universidad con miles de estudiantes, el tiempo entre clases es limitado (generalmente 10 a 15 minutos). Si un estudiante no conoce el camino mas corto entre el Edificio 1 y el Edificio 3, podria llegar tarde a su siguiente clase. Un sistema de rutas resuelve esto calculando automaticamente el camino mas eficiente.

Ejemplos reales de uso en universidades:

- El MIT (Massachusetts Institute of Technology) tiene una aplicacion interna que permite a los estudiantes navegar entre sus mas de 100 edificios.
- La UNAM cuenta con mapas interactivos de Ciudad Universitaria que muestran rutas peatonales y del Pumabus.
- Universidades europeas como la Politecnica de Madrid usan sistemas similares para guiar a estudiantes de intercambio.

Este proyecto replica y adapta esas ideas para ESIME Culhuacan, resolviendo tres problemas concretos:

1. Orientacion dentro del campus. Los estudiantes nuevos no conocen la ubicacion de edificios, laboratorios o areas comunes. La aplicacion les muestra un mapa con todos los puntos de interes y calcula la ruta mas rapida.

2. Gestion del estacionamiento. Actualmente no existe un sistema que permita saber si hay lugares disponibles antes de llegar. Esta aplicacion muestra en tiempo real cuantos espacios hay libres, permite reservarlos y marca tu ubicacion con GPS para que recuerdes donde dejaste tu coche.

3. Organizacion academica. La aplicacion muestra el horario de clases del estudiante, le notifica cuando esta por comenzar una clase y le ofrece navegacion directa al salon correspondiente.

Al estudiar este proyecto aprenderas como funciona una aplicacion web moderna desde la base de datos hasta la interfaz grafica, incluyendo algoritmos de rutas, geolocalizacion por GPS, comunicacion entre servidor y cliente, y diseno de interfaces responsivas.


## OBJETIVO EDUCATIVO DEL PROYECTO

Este proyecto cubre los siguientes conceptos fundamentales de programacion y desarrollo de software:

Estructura de proyectos. Aprenderas como se organiza un proyecto real con carpetas separadas para el servidor (backend) y la interfaz (frontend), cada una con su propia logica y responsabilidades.

Frontend y Backend. Entenderas la diferencia entre el codigo que se ejecuta en el navegador del usuario (frontend, construido con React) y el codigo que se ejecuta en el servidor (backend, construido con Flask en Python).

APIs y endpoints. Veras como el frontend se comunica con el backend a traves de peticiones HTTP, enviando y recibiendo datos en formato JSON.

Bases de datos. Aprenderas como se almacenan los datos de usuarios, horarios y estacionamiento en una base de datos relacional (SQLite) usando un ORM (SQLAlchemy).

Algoritmos. Comprenderas como funciona el algoritmo de Dijkstra para calcular la ruta mas corta entre dos puntos en un grafo, aplicado directamente al mapa del campus.

Mapas y geolocalizacion. Veras como se integra un mapa interactivo con Leaflet, como se obtiene la ubicacion del usuario con el GPS del navegador y como se miden distancias geograficas con la formula de Haversine.

Manejo de estado. Aprenderas como React gestiona la informacion que cambia en la pantalla (estados), como las notificaciones, la posicion del usuario o los espacios de estacionamiento.

Logica de negocio. Entenderas reglas como: un usuario solo puede reservar un espacio si se encuentra dentro de un radio maximo del estacionamiento, o una reserva expira automaticamente despues de 10 minutos.


## ARQUITECTURA GENERAL DEL SISTEMA

La arquitectura de una aplicacion web describe como estan organizadas sus partes y como se comunican entre si. Este proyecto usa una arquitectura llamada cliente-servidor, que es la mas comun en aplicaciones web.

El diagrama general del sistema es el siguiente:

```
USUARIO (navegador web)
       |
       v
REACT FRONTEND (localhost:5173)
       |
       | Peticiones HTTP (fetch / JSON)
       v
FLASK BACKEND (localhost:5001)
       |
       |--- SQLALCHEMY (ORM) con BINDS multiples
       |         |
       |         |--- BASE DE DATOS MAP (instance/map.db)
       |         |    Edificios, caminos, estacionamiento,
       |         |    lugares guardados
       |         |
       |         |--- BASE DE DATOS SCHOOL (instance/school.db)
       |              Alumnos, materias, grupos, horarios,
       |              inscripciones, profesores
       |
       |--- KML ROUTER (NetworkX + Dijkstra)
       |         |
       |         v
       |    ARCHIVO KML (caminos del campus)
       |
       |--- SERVICIOS
       |    |--- auth_service (autenticacion + bcrypt)
       |    |--- schedule_service (horarios)
       |    |--- parking_service (estacionamiento)
       |    |--- school_adapter (datos institucionales)
       |
       |--- SEGURIDAD
            |--- Hashing bcrypt para contrasenas
            |--- Migracion transparente de hashes legacy
```

Como interactuan frontend y backend:

El frontend (React) se ejecuta en el navegador del usuario. Es responsable de mostrar la interfaz grafica: el mapa, los botones, los formularios, las listas. No tiene acceso directo a la base de datos ni a los algoritmos de rutas.

El backend (Flask) se ejecuta en el servidor (tu computadora durante desarrollo). Es responsable de almacenar datos, ejecutar logica de negocio y calcular rutas. No sabe nada sobre como se ve la interfaz.

Ambos se comunican mediante peticiones HTTP. El frontend envia una peticion (por ejemplo: "dame el horario del alumno con boleta 2024001") y el backend responde con datos en formato JSON (un formato de texto estructurado que ambos entienden).

Flujo completo cuando el usuario calcula una ruta:

```
1. USUARIO hace clic en "Calcular ruta"
       |
2. REACT obtiene coordenadas de origen y destino
       |
3. REACT envia peticion POST a /api/navigation/walking-route
       |      con: start_lat, start_lon, end_lat, end_lon
       |
4. FLASK recibe la peticion en app.py
       |
5. FLASK llama a kml_router.find_shortest_path(origen, destino)
       |
6. KML ROUTER busca los nodos mas cercanos en el grafo
       |
7. NETWORKX ejecuta el algoritmo de Dijkstra
       |
8. KML ROUTER simplifica la ruta con Douglas-Peucker
       |
9. FLASK construye la respuesta JSON con:
       |      path: [[lat, lon], [lat, lon], ...]
       |      distance: 342.5 (metros)
       |      eta_minutes: 4.6
       |
10. REACT recibe el JSON y dibuja la ruta como
        una linea azul (Polyline) sobre el mapa de Leaflet
```

Flujo completo cuando el usuario reserva estacionamiento:

```
1. USUARIO hace clic en un cajon libre
       |
2. REACT muestra modal con opciones: Reservar / Ocupar
       |
3. USUARIO hace clic en "Reservar"
       |
4. REACT solicita ubicacion GPS con navigator.geolocation
       |
5. REACT calcula distancia al estacionamiento (Haversine)
       |
6. Si distancia > 1500m: RECHAZAR con alerta
       |  Si distancia <= 1500m: CONTINUAR
       |
7. REACT envia PUT a /api/parking/spaces/{id}/status
       |      con: status="reserved", user_boleta="2024001"
       |
8. FLASK cambia estado del cajon en la base de datos
       |      Establece reservation_expires_at = ahora + 10 min
       |
9. FLASK responde con exito
       |
10. REACT actualiza la cuadricula visual
        El cajon cambia de verde (libre) a amarillo (reservado)
        Inicia temporizador de 10 minutos
```


## FLUJO DE DATOS EN LA APLICACION

Los datos en esta aplicacion viajan constantemente entre cinco componentes principales. Entender este flujo es fundamental para comprender como funciona cualquier aplicacion web moderna.

Diagrama del ciclo de datos:

```
NAVEGADOR WEB (Chrome, Firefox, Safari)
       |
       | El usuario interactua con la interfaz
       v
REACT (estado local + componentes)
       |
       | fetch() envia peticion HTTP
       v
FLASK API (endpoints en app.py)
       |
       |--- Para datos del mapa: SQLALCHEMY ---> SQLITE (instance/map.db)
       |
       |--- Para datos academicos: SQLALCHEMY ---> SQLITE (instance/school.db)
       |
       |--- Para rutas: KML ROUTER ---> GRAFO DE NETWORKX
       |
       v
RESPUESTA JSON
       |
       | El navegador recibe los datos
       v
REACT actualiza el estado
       |
       | React re-renderiza los componentes afectados
       v
EL USUARIO VE EL RESULTADO EN PANTALLA
```

Ejemplo concreto de flujo de datos para obtener el horario:

Paso 1. El usuario abre la pagina Dashboard. React ejecuta un hook useEffect que se dispara automaticamente al cargar el componente.

Paso 2. Dentro de useEffect, se llama a la funcion getSchedule(boleta) definida en api.js. Esta funcion usa fetch() para enviar una peticion GET al endpoint /api/user/schedule?boleta=2024001.

Paso 3. Flask recibe la peticion en app.py. El endpoint extrae la boleta de los parametros, llama al schedule_service que busca las inscripciones del alumno en la base de datos.

Paso 4. SQLAlchemy traduce la consulta a SQL: SELECT FROM inscripciones WHERE alumno_id = (SELECT id FROM alumnos WHERE boleta = '2024001'). SQLite ejecuta la consulta y devuelve los registros.

Paso 5. El servicio filtra las clases que corresponden al dia actual (por ejemplo, si hoy es miercoles, solo devuelve las clases del dia 3).

Paso 6. Flask convierte los objetos Python a JSON y los envia como respuesta HTTP.

Paso 7. React recibe el JSON, actualiza el estado con setSchedule(data), y automaticamente re-renderiza la lista de materias en la pantalla del Dashboard.


## TECNOLOGIAS UTILIZADAS

A continuacion se explica cada tecnologia que usa el proyecto, para que sirve y por que se eligio.


### Python

Python es un lenguaje de programacion de proposito general, conocido por su sintaxis clara y legible. En este proyecto se usa para construir todo el servidor backend: la logica de negocio, las rutas de la API, los modelos de datos y los algoritmos de navegacion.

Se eligio porque es el lenguaje mas accesible para estudiantes que estan aprendiendo y porque tiene una enorme cantidad de bibliotecas disponibles.


### Flask

Flask es un framework web minimalista para Python. Un framework es como un esqueleto predefinido que facilita construir aplicaciones. Flask se encarga de recibir las peticiones del navegador, procesarlas y devolver respuestas.

Se eligio por su simplicidad. A diferencia de otros frameworks como Django, Flask no impone una estructura rigida, lo que permite entender cada parte del sistema paso a paso.


### React

React es una biblioteca de JavaScript creada por Meta (Facebook) para construir interfaces de usuario. Permite dividir la pantalla en componentes reutilizables: por ejemplo, un componente para el mapa, otro para la barra de busqueda y otro para la lista de lugares.

Como funciona React internamente: React utiliza un concepto llamado Virtual DOM. El DOM (Document Object Model) es la representacion en memoria de todo lo que aparece en la pantalla. Normalmente, modificar el DOM directamente es lento. React resuelve esto creando una copia virtual (Virtual DOM). Cuando el estado de un componente cambia, React compara la copia virtual con el DOM real, detecta las diferencias y solo actualiza las partes que realmente cambiaron. Esto hace que la interfaz sea muy rapida.

Que son los Hooks: Los hooks son funciones especiales de React que permiten agregar funcionalidad a los componentes. Los mas usados en este proyecto son:

- useState: Permite crear variables que, cuando cambian, hacen que el componente se vuelva a dibujar. Ejemplo: const [query, setQuery] = useState("") crea una variable query con valor inicial vacio. Cuando se llama setQuery("cafeteria"), React actualiza el componente.

- useEffect: Permite ejecutar codigo cuando el componente se muestra por primera vez o cuando ciertos datos cambian. Ejemplo: cargar el horario del usuario cuando la pagina se abre.

- useNavigate: Permite navegar entre paginas de la aplicacion desde el codigo JavaScript en lugar de que el usuario haga clic en un enlace.

Que es React Router: React Router es una biblioteca que permite tener multiples "paginas" dentro de una sola aplicacion. En una aplicacion web tradicional, cada pagina es un archivo HTML diferente. Con React Router, toda la aplicacion es un solo archivo HTML y React cambia el contenido segun la URL. La ruta / muestra el Login, /map muestra el mapa, /dashboard muestra el perfil.

Se eligio React porque es la herramienta mas utilizada en la industria para construir interfaces web modernas e interactivas.


### JavaScript

JavaScript es el lenguaje de programacion que ejecuta el navegador web. Todo lo que ves moverse, cambiar de color o responder a un clic en una pagina web esta controlado por JavaScript. En este proyecto, React usa JavaScript internamente.

Se usa porque es el unico lenguaje que los navegadores entienden de forma nativa para logica en la interfaz.


### SQLite

SQLite es un sistema de base de datos relacional que almacena toda la informacion en archivos individuales dentro del proyecto. No requiere instalar un servidor de base de datos separado como MySQL o PostgreSQL. Toda la logica del motor de base de datos esta contenida en una biblioteca que se ejecuta dentro de tu programa.

En este proyecto se utilizan dos archivos de base de datos separados, cada uno con un proposito diferente:

- instance/map.db: Almacena todos los datos relacionados con el mapa fisico del campus. Esto incluye edificios, caminos peatonales, secciones de estacionamiento, espacios individuales de estacionamiento, reservas, historial de uso y los lugares que cada usuario ha guardado como favoritos.

- instance/school.db: Almacena todos los datos academicos e institucionales. Esto incluye alumnos (con sus credenciales de acceso), materias del plan de estudios, profesores, salones, grupos, horarios de clase e inscripciones.

Esta separacion se eligio por dos razones. Primera, permite que los datos del mapa (que son propios de la aplicacion y del campus fisico) sean independientes de los datos academicos (que pertenecen a la institucion educativa). Segunda, permite reemplazar la base de datos escolar por la base de datos real de cualquier otra escuela sin afectar el funcionamiento del mapa.

La configuracion de estas dos bases de datos se define en config.py usando la funcionalidad de SQLALCHEMY_BINDS de Flask-SQLAlchemy. Cada modelo en el codigo tiene un atributo llamado __bind_key__ que indica en cual base de datos vive. Los modelos con __bind_key__ = 'map' se almacenan en map.db y los modelos con __bind_key__ = 'school' se almacenan en school.db.


### SQLAlchemy

SQLAlchemy es un ORM (Object-Relational Mapper) para Python. Un ORM permite trabajar con la base de datos usando clases y objetos de Python en lugar de escribir consultas SQL directamente.

Como traduce objetos a SQL: Cuando escribes Alumno.query.filter_by(boleta='2024001').first(), SQLAlchemy genera internamente la consulta SQL: SELECT * FROM alumnos WHERE boleta = '2024001' LIMIT 1. Cuando creas un nuevo objeto con db.session.add(nuevo_alumno), SQLAlchemy genera: INSERT INTO alumnos (boleta, nombre, carrera) VALUES ('2024001', 'Juan', 'Computacion').

La ventaja de usar un ORM es que puedes cambiar de base de datos (de SQLite a PostgreSQL, por ejemplo) sin modificar tu codigo Python. Solo cambias la cadena de conexion en config.py.


### Leaflet

Leaflet es una biblioteca de JavaScript para crear mapas interactivos en el navegador. Permite mostrar mapas, agregar marcadores, trazar rutas y detectar clics del usuario sobre el mapa.

Se eligio porque es gratuita, ligera y muy bien documentada. Es la alternativa mas popular a Google Maps para proyectos de codigo abierto.


### Tailwind CSS

Tailwind CSS es un framework de estilos que permite disenar interfaces escribiendo clases directamente en el HTML. En vez de crear archivos CSS separados con reglas como .boton-rojo { background: red }, se escribe className="bg-red-600" directamente en el componente.

Se eligio porque acelera el diseno visual y mantiene los estilos organizados junto al componente que los usa.


### Vite

Vite es una herramienta de desarrollo que compila y sirve el codigo del frontend de forma extremadamente rapida. Cuando guardas un cambio en un archivo React, Vite actualiza el navegador al instante sin recargar toda la pagina.

Se eligio porque es mas rapido que alternativas como Webpack y ofrece una experiencia de desarrollo muy fluida.


### Algoritmo de Dijkstra (NetworkX)

NetworkX es una biblioteca de Python para trabajar con grafos (redes de nodos y conexiones). El algoritmo de Dijkstra, disponible dentro de NetworkX, calcula la ruta mas corta entre dos nodos en un grafo ponderado.

Se eligio porque Dijkstra es el algoritmo estandar para rutas mas cortas y NetworkX proporciona una implementacion lista para usar.


### API de Geolocalizacion del navegador

Los navegadores modernos incluyen una funcion llamada navigator.geolocation que permite obtener la ubicacion GPS del usuario con su permiso. Esta API devuelve las coordenadas de latitud y longitud del dispositivo.

Se usa para saber donde esta el estudiante en tiempo real: para calcular rutas desde su posicion actual y para verificar que esta cerca del estacionamiento al reservar un espacio.


### Azure AD (MSAL)

Microsoft Authentication Library (MSAL) permite que los usuarios inicien sesion con su cuenta institucional de Outlook o Microsoft 365. Esto conecta la aplicacion con el sistema de correo de la escuela.

Se uso para ofrecer una opcion de autenticacion profesional. En modo local, los usuarios tambien pueden iniciar sesion con su numero de boleta.


### bcrypt

bcrypt es un algoritmo de hashing de contrasenas disenado especificamente para almacenar credenciales de forma segura. A diferencia de algoritmos de proposito general como SHA-256 o MD5, bcrypt fue creado para ser intencionalmente lento: esto dificulta enormemente que un atacante pruebe millones de contrasenas por segundo si obtiene acceso a la base de datos.

Que es un hash: Un hash es una funcion matematica que transforma un dato de cualquier tamano en una cadena de caracteres de tamano fijo. La caracteristica fundamental es que el proceso es irreversible: dada la contrasena "nueva123" puedes calcular su hash facilmente, pero dado el hash es computacionalmente imposible recuperar "nueva123". Esto significa que aunque alguien robe la base de datos, no puede obtener las contrasenas originales.

Como funciona bcrypt internamente:

1. Recibe la contrasena en texto plano, por ejemplo "nueva123".
2. Genera una sal (salt) aleatoria. La sal es una cadena de caracteres que se agrega a la contrasena antes de calcular el hash. Esto asegura que dos usuarios con la misma contrasena tengan hashes completamente diferentes.
3. Ejecuta multiples rondas del algoritmo Blowfish (por defecto 12 rondas, cada ronda el calculo se duplica en tiempo). Esto es lo que hace a bcrypt lento deliberadamente.
4. Produce una cadena como: $2b$12$0K9cVIN3l8kss... donde $2b$ indica bcrypt, $12$ indica 12 rondas, y el resto es la sal concatenada con el hash.

Por que no usar SHA-256 o MD5 para contrasenas: Estos algoritmos fueron disenados para ser rapidos. Un atacante puede calcular miles de millones de hashes SHA-256 por segundo en hardware moderno. bcrypt esta disenado para tomar aproximadamente 100 milisegundos por hash, lo que reduce la velocidad de un ataque de fuerza bruta en un factor de millones.

En este proyecto se usa la biblioteca bcrypt de Python junto con werkzeug.security para soportar migracion transparente de hashes antiguos. El archivo services/auth_service.py contiene tres metodos clave que implementan este sistema:

- _hash_password(password): Recibe una contrasena en texto plano y retorna su hash bcrypt.
- _verify_password(stored_hash, password): Verifica si una contrasena coincide con un hash almacenado. Soporta tanto hashes bcrypt actuales como hashes legacy (pbkdf2, scrypt).
- _needs_rehash(stored_hash): Determina si un hash debe ser actualizado a bcrypt.

Se eligio bcrypt porque es el estandar de la industria para almacenamiento seguro de contrasenas y esta recomendado por OWASP (Open Web Application Security Project).


## REQUISITOS PARA INSTALAR EL PROYECTO

Antes de instalar el proyecto necesitas tener cuatro programas en tu computadora. A continuacion se explica cada uno y como verificar si ya lo tienes instalado.


### Python (version 3.10 o superior)

Python es el lenguaje del servidor. Lo necesitas para ejecutar el backend.

Para verificar si ya lo tienes instalado, abre una terminal y escribe:

```
python3 --version
```

Si aparece algo como Python 3.13.2, lo tienes instalado. Si aparece un error, descargalo desde https://www.python.org/downloads/


### Node.js (version 18 o superior)

Node.js es un entorno que permite ejecutar JavaScript fuera del navegador. Lo necesitas para compilar y servir el frontend con React.

Para verificar si ya lo tienes instalado:

```
node --version
```

Si aparece algo como v22.11.0, lo tienes instalado. Si no, descargalo desde https://nodejs.org/


### npm (se instala con Node.js)

npm es el gestor de paquetes de Node.js. Permite instalar las bibliotecas que usa el frontend (React, Leaflet, etc.).

Para verificar:

```
npm --version
```


### Git

Git es un sistema de control de versiones. Lo necesitas para descargar (clonar) el proyecto desde un repositorio.

Para verificar:

```
git --version
```

Si no lo tienes, descargalo desde https://git-scm.com/


## INSTALACION PASO A PASO

Sigue estos pasos en orden. Cada paso incluye el comando exacto que debes escribir en tu terminal.


### Paso 1. Clonar el repositorio

Clonar significa descargar una copia completa del proyecto a tu computadora. Abre tu terminal y escribe:

```
git clone https://github.com/AlexGuittar1/Mapa_interactivo_ESIME_CULHUACAN.git
```


### Paso 2. Entrar a la carpeta del proyecto

```
cd Mapa_interactivo_ESIME_CULHUACAN
```


### Paso 3. Crear un entorno virtual de Python

Un entorno virtual es una carpeta aislada donde se instalan las dependencias del proyecto sin afectar otras aplicaciones de tu computadora. Es como tener una caja separada para cada proyecto.

```
python3 -m venv .venv
```


### Paso 4. Activar el entorno virtual

En macOS o Linux:

```
source .venv/bin/activate
```

En Windows:

```
.venv\Scripts\activate
```

Sabras que esta activo porque veras (.venv) al inicio de la linea en tu terminal.


### Paso 5. Instalar las dependencias del backend

```
pip install -r requirements.txt
```

Esto instala todas las dependencias listadas en el archivo requirements.txt, que incluye:

- flask: el framework web del servidor.
- flask-cors: permite que el frontend (en otro puerto) se comunique con el backend.
- flask-sqlalchemy: conecta Flask con la base de datos usando el ORM.
- flask-limiter: controla la cantidad de peticiones por segundo para evitar abusos.
- python-dotenv: carga variables de entorno desde un archivo .env.
- networkx: biblioteca de grafos para calcular rutas con Dijkstra.
- bcrypt: algoritmo de hashing seguro para almacenar contrasenas.
- gunicorn: servidor WSGI para despliegue en produccion.


### Paso 6. Inicializar la base de datos

```
cd backend
python3 init_parking.py
```


### Paso 7. Instalar las dependencias del frontend

```
cd ../frontend
npm install
```

Este comando lee el archivo package.json y descarga todas las bibliotecas listadas ahi a una carpeta llamada node_modules.


## COMO EJECUTAR EL PROYECTO

El proyecto necesita dos servidores corriendo al mismo tiempo: uno para el backend y otro para el frontend. Necesitaras dos ventanas de terminal.


### Iniciar el backend

En la primera terminal, asegurate de estar en la carpeta backend con el entorno virtual activado:

```
cd backend
python3 app.py
```

Veras un mensaje indicando que el servidor esta corriendo en http://localhost:5001. Este servidor escucha peticiones del frontend y responde con datos de la base de datos.


### Iniciar el frontend

En la segunda terminal, entra a la carpeta frontend:

```
cd frontend
npm run dev
```

Veras un mensaje indicando que Vite esta sirviendo la aplicacion en http://localhost:5173.


### Acceder a la aplicacion

Abre tu navegador web y visita:

```
http://localhost:5173
```

Veras la pantalla de inicio de sesion. Puedes registrar un usuario nuevo con cualquier numero de boleta para explorar la aplicacion.


## ESTRUCTURA DEL PROYECTO

```
Mapa_interactivo_ESIME_CULHUACAN/
|
|-- backend/                         Servidor en Python (Flask)
|   |-- app.py                       Punto de entrada principal del servidor
|   |-- config.py                    Configuracion de entornos y bases de datos
|   |-- kml_router.py                Motor de calculo de rutas con Dijkstra
|   |-- seed_map_data.py             Pobla datos iniciales del mapa
|   |-- seed_inscripciones.py        Crea inscripciones de prueba
|   |-- init_parking.py              Genera espacios de estacionamiento
|   |-- migrate_post_refactor.py     Script de migracion de datos
|   |-- models/                      Paquete de modelos de datos
|   |   |-- __init__.py              Re-exportacion de todos los modelos
|   |   |-- database.py              Instancia central de SQLAlchemy
|   |   |-- map_models.py            Modelos de mapa (bind: map.db)
|   |   |-- school_models.py         Modelos academicos (bind: school.db)
|   |-- middleware/
|   |   |-- auth_middleware.py       Decoradores de autenticacion
|   |-- repositories/
|   |   |-- user_repository.py       Interfaz abstracta de usuarios
|   |   |-- sqlite_repository.py     Implementacion con SQLite
|   |-- services/
|   |   |-- auth_service.py          Autenticacion y hashing bcrypt
|   |   |-- schedule_service.py      Consulta de horarios
|   |   |-- parking_service.py       Logica de estacionamiento
|   |   |-- school_adapter.py        Adaptador de datos institucionales
|   |   |-- routing_service.py       Servicio de calculo de rutas
|   |-- scripts/
|   |   |-- import_horarios.py       Importa horarios desde SQL
|   |-- instance/
|       |-- map.db                   Base de datos del mapa
|       |-- school.db                Base de datos academica
|
|-- frontend/                        Aplicacion React
|   |-- index.html                   Pagina HTML raiz
|   |-- package.json                 Dependencias del frontend
|   |-- vite.config.js               Configuracion de Vite
|   |-- src/
|       |-- main.jsx                 Punto de entrada de React
|       |-- App.jsx                  Rutas de la aplicacion
|       |-- index.css                Estilos globales
|       |-- authConfig.js            Configuracion de Azure AD
|       |-- mapConfig.js             Configuracion del mapa
|       |-- components/
|       |   |-- MapComponent.jsx     Mapa interactivo completo
|       |   |-- ParkingSectionMap.jsx Plano 2D de seccion
|       |   |-- SavedPlacesSheet.jsx  Panel de lugares guardados
|       |-- pages/
|       |   |-- Login.jsx            Inicio de sesion y registro
|       |   |-- Dashboard.jsx        Perfil y horario
|       |   |-- MapPage.jsx          Contenedor del mapa
|       |   |-- ParkingPage.jsx      Sistema de estacionamiento
|       |-- context/
|       |   |-- NotificationContext.jsx  Notificaciones de clases
|       |-- services/
|       |   |-- api.js               Llamadas HTTP al servidor
|       |-- data/
|           |-- key_points.json      Puntos clave del campus
|
|-- requirements.txt                 Dependencias de Python
```


## CONCEPTOS BASICOS DE PROGRAMACION UTILIZADOS

Antes de analizar el codigo, es importante entender algunos conceptos fundamentales que se usan constantemente en el proyecto.


### Que es una variable

Una variable es un espacio con nombre donde guardas un dato para usarlo despues. Es como una caja etiquetada: adentro puedes poner un numero, un texto o una lista.

Ejemplo en Python:

```python
nombre = "Juan"
edad = 17
```

Ejemplo en JavaScript:

```javascript
const nombre = "Juan";
let edad = 17;
```

La diferencia entre const y let en JavaScript es que const no permite cambiar el valor despues de asignarlo, mientras que let si.


### Que es una funcion

Una funcion es un bloque de codigo que realiza una tarea especifica. Es como una receta de cocina: recibe ingredientes (parametros), ejecuta pasos (instrucciones) y produce un resultado (valor de retorno).

```python
def calcular_area(base, altura):
    return base * altura

resultado = calcular_area(5, 3)  # resultado es 15
```

Las funciones existen para evitar repetir codigo. Si necesitas calcular el area en 10 lugares diferentes de tu programa, escribes la funcion una vez y la llamas 10 veces.


### Que es una API

API significa Interfaz de Programacion de Aplicaciones. Es un conjunto de reglas que permiten que dos programas se comuniquen entre si.

En este proyecto, el frontend (React) necesita datos que estan en el servidor (Flask). Para obtenerlos, le envia una peticion HTTP a una direccion especifica. El servidor recibe la peticion, busca los datos en la base de datos y los devuelve en formato JSON.

Es como un mesero en un restaurante: tu (el frontend) le pides algo al mesero (la API), el va a la cocina (el backend), y te trae lo que pediste (los datos).


### Que es un endpoint

Un endpoint es una URL especifica del servidor que responde a un tipo de peticion. Cada endpoint tiene una funcion definida.

Ejemplo: el endpoint /api/user/login espera recibir un numero de boleta y devuelve los datos del usuario si existe. Es como un numero de ventanilla: si vas a la ventanilla 3, te atienden para inscripciones. Si vas a la ventanilla 5, te atienden para credenciales.


### Que es una base de datos

Una base de datos es un sistema organizado para almacenar informacion de forma permanente. Funciona como un conjunto de tablas (similares a hojas de calculo de Excel) donde cada fila es un registro y cada columna es un dato.


### Que es un algoritmo

Un algoritmo es una secuencia ordenada de pasos para resolver un problema. Es como las instrucciones para armar un mueble: si sigues los pasos en orden, llegas al resultado correcto.


### Que es un componente en React

Un componente es una pieza independiente de la interfaz que tiene su propia logica y su propia apariencia. React permite dividir la pantalla en componentes mas pequenos que se pueden reutilizar.

Ejemplo: el mapa es un componente, la barra de busqueda es otro componente y cada marcador en el mapa es otro. Juntos forman la pagina completa.


### Que es el estado en React

El estado es la informacion que puede cambiar con el tiempo dentro de un componente. Cuando el estado cambia, React vuelve a dibujar automaticamente el componente para reflejar el cambio.

Ejemplo: cuando el usuario escribe en la barra de busqueda, el texto que escribio es un estado. Cada letra que agrega actualiza el estado y React actualiza lo que se muestra en pantalla.


## EXPLICACION DE LOS ALGORITMOS


### Algoritmo de Dijkstra

El algoritmo de Dijkstra resuelve el siguiente problema: dado un mapa con multiples caminos entre puntos, encontrar la ruta mas corta entre un punto de inicio y un punto de destino.

Problema que resuelve: Imagina que estas en la entrada de la escuela y quieres llegar a la cafeteria. Hay muchos caminos posibles: puedes ir por la izquierda, por la derecha, rodear el edificio 1, pasar por el estacionamiento, etc. Dijkstra los evalua todos y te dice cual es el camino mas corto en metros.

Por que se usa en este proyecto: Los caminos del campus se representan como un grafo (una red de puntos conectados). Dijkstra es el algoritmo estandar para encontrar la ruta mas corta en grafos con pesos positivos (donde el peso es la distancia en metros).

Como funciona paso a paso:

1. El mapa se representa como un grafo. Cada interseccion es un nodo y cada camino entre intersecciones es una arista. Cada arista tiene un peso que representa la distancia en metros.

2. El algoritmo empieza en el nodo de origen y le asigna una distancia de 0. A todos los demas nodos les asigna una distancia infinita (aun no sabemos como llegar).

3. Revisa todos los vecinos del nodo actual. Para cada vecino, calcula la distancia total desde el origen pasando por el nodo actual. Si esta distancia es menor que la previamente registrada, la actualiza.

4. Marca el nodo actual como visitado y pasa al nodo no visitado con la menor distancia.

5. Repite los pasos 3 y 4 hasta llegar al nodo destino.

6. Al terminar, reconstruye el camino siguiendo los nodos que marcaron las distancias mas cortas.

Ejemplo practico simplificado:

```
Imagina 4 nodos: Entrada, Edificio1, Cafeteria, Gimnasio

Conexiones (con distancia en metros):
  Entrada --- 100m --- Edificio1
  Entrada --- 250m --- Cafeteria
  Edificio1 --- 80m --- Cafeteria
  Edificio1 --- 200m --- Gimnasio
  Cafeteria --- 150m --- Gimnasio

Para ir de Entrada a Gimnasio:
  Ruta directa: Entrada -> Edificio1 -> Gimnasio = 100 + 200 = 300m
  Ruta larga: Entrada -> Cafeteria -> Gimnasio = 250 + 150 = 400m
  Ruta optima: Entrada -> Edificio1 -> Cafeteria -> Gimnasio = 100 + 80 + 150 = 330m

Dijkstra descubre que la ruta mas corta es la directa: 300m.
```

Complejidad computacional: El algoritmo de Dijkstra tiene una complejidad de O((V + E) log V), donde V es el numero de nodos y E es el numero de aristas. En el contexto de este proyecto, con un campus de unos cientos de nodos, la ruta se calcula en milisegundos.


### Formula de Haversine

Problema que resuelve: La formula de Haversine calcula la distancia entre dos puntos sobre la superficie de la Tierra usando sus coordenadas de latitud y longitud. Es necesaria porque la Tierra no es plana: no puedes simplemente restar las coordenadas para obtener la distancia.

Por que se usa en este proyecto: Se usa en dos lugares criticos. En kml_router.py para calcular el peso de cada arista del grafo (la distancia real en metros entre dos puntos del camino). En ParkingPage.jsx para medir la distancia entre el usuario y el estacionamiento.

Como funciona conceptualmente: Imagina que tomas un globo terraqueo y pones un alfiler en la entrada de la escuela y otro en el estacionamiento. La distancia entre ambos no es una linea recta a traves del globo, sino una curva sobre la superficie. La formula de Haversine calcula esa curva usando trigonometria, tomando en cuenta el radio de la Tierra (6,371 km).

Implementacion simplificada:

```python
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Radio de la Tierra en metros
    # Convertir grados a radianes
    lat1, lat2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    # Formula de Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c  # Distancia en metros
```

Complejidad computacional: O(1), es decir, constante. Siempre tarda lo mismo sin importar los valores de entrada.


### Algoritmo de Douglas-Peucker

Problema que resuelve: Cuando Dijkstra calcula una ruta, puede devolver cientos de puntos intermedios. Dibujar todos esos puntos en el mapa es lento e innecesario visualmente. Douglas-Peucker reduce esa cantidad conservando solo los puntos que definen la forma general del camino.

Por que se usa: Mejora el rendimiento al dibujar rutas en el mapa. Una ruta de 200 puntos se puede reducir a 30 puntos sin que el usuario note ninguna diferencia visual.

Como funciona:

1. Traza una linea recta imaginaria entre el primer y ultimo punto del camino.
2. Busca el punto intermedio que esta mas lejos de esa linea recta.
3. Si esa distancia maxima es mayor a un umbral (tolerancia), conserva ese punto y divide el camino en dos mitades.
4. Repite el proceso para cada mitad.
5. Si ningun punto intermedio esta suficientemente lejos de la linea, descarta todos los puntos intermedios de ese segmento.

Analogia: Imagina que dibujas la silueta de una montana con 100 puntos. Douglas-Peucker dice: "Solo necesito los picos y los valles mas pronunciados. Los puntos que estan casi en linea recta se pueden eliminar sin cambiar la forma general."

Complejidad computacional: O(n log n) en el caso promedio, donde n es el numero de puntos.


## EXPLICACION DETALLADA DE CADA ARCHIVO


### Backend


#### app.py

Problema que resuelve: Es el punto central que conecta todas las partes del backend. Sin este archivo, no habria servidor web, no habria API y el frontend no tendria con quien comunicarse.

Como interactua con otros archivos: Importa models.py para acceder a las tablas de la base de datos. Importa config.py para saber en que entorno ejecutarse. Importa kml_router.py para calcular rutas. Importa los servicios y repositorios para la logica de negocio.

Que pasaria si no existiera: No habria servidor. El frontend no podria obtener datos, calcular rutas ni gestionar estacionamiento.

Endpoints principales:

- /api/user/login (POST): Recibe una boleta, busca al alumno en la base de datos y devuelve sus datos. Si no existe, devuelve error 404.

- /api/user/register (POST): Recibe nombre, boleta, carrera y vehiculo. Crea un nuevo registro en la tabla alumnos. Si la boleta ya existe, devuelve error 409.

- /api/user/schedule (GET): Recibe una boleta, busca las inscripciones del alumno, obtiene las materias y horarios del dia actual, y devuelve la lista ordenada cronologicamente.

- /api/navigation/walking-route (POST): Recibe coordenadas de origen y destino. Llama a kml_router.find_shortest_path(). Devuelve la ruta simplificada, distancia y tiempo estimado.

- /api/parking/spaces (GET): Consulta todas las secciones y espacios de estacionamiento. Agrupa los espacios por seccion y devuelve contadores de disponibles, ocupados y reservados.

- /api/parking/spaces/<id>/status (PUT): Cambia el estado de un cajon. Valida que la accion sea logica (no puedes reservar un cajon ya ocupado). Para reservas, establece expiracion a 10 minutos.


#### models/ (paquete de modelos)

Problema que resuelve: Define la estructura de toda la informacion que maneja el sistema. Sin estos archivos, el programa no sabria que datos almacenar ni como organizarlos.

Estructura interna del paquete:

- models/__init__.py: Re-exporta todos los modelos de ambas bases de datos para que el resto del codigo pueda importarlos con una sola linea (from models import Alumno, ParkingSpace).
- models/database.py: Contiene la instancia central de SQLAlchemy (db = SQLAlchemy()). Esta instancia es compartida por todos los modelos.
- models/map_models.py: Define los modelos que se almacenan en map.db: EdificioDB, CaminoDB, SavedPlace, ParkingSection, ParkingSpace, ParkingReservation y ParkingHistory.
- models/school_models.py: Define los modelos que se almacenan en school.db: Alumno, Materia, Profesor, Salon, Grupo, MateriaGrupo, Horario e Inscripcion.

Como interactua: Todos los archivos del backend importan modelos desde este paquete. app.py los usa para consultar y modificar datos. Los servicios los usan para ejecutar logica de negocio.

Que pasaria si no existiera: No habria tablas en la base de datos. No se podrian guardar usuarios, horarios ni espacios de estacionamiento.

Modelos clave y sus relaciones:

El modelo Alumno es el centro del sistema academico. Un alumno tiene relaciones con inscripciones (sus materias). El campo password_hash almacena la contrasena hasheada con bcrypt. El campo auth_provider indica si el usuario se autentica localmente o via Azure AD.

El modelo MateriaGrupo es una tabla relacional central que conecta Materia + Grupo + Profesor. Esta tabla existe porque una misma materia puede ser impartida por diferentes profesores a diferentes grupos. Cada MateriaGrupo tiene multiples horarios asociados.

El modelo ParkingSpace usa referencias logicas (user_boleta como string) en lugar de claves foraneas reales para conectar con los alumnos. Esto es necesario porque el alumno vive en otra base de datos (school.db) y las claves foraneas de SQLite no pueden cruzar archivos de base de datos.


#### kml_router.py

Problema que resuelve: Traduce un archivo de datos geograficos (KML) a un grafo navegable y calcula las rutas mas cortas entre cualquier par de puntos del campus.

Como interactua: app.py lo inicializa al arrancar el servidor y lo llama cada vez que un usuario solicita una ruta.

Que pasaria si no existiera: No se podrian calcular rutas. El mapa mostraria los edificios pero no sabria como trazar caminos entre ellos.

Flujo interno:

```
1. __init__(): Lee el archivo KML
       |
2. Parsea las coordenadas (latitud, longitud) de cada linestring
       |
3. Construye un grafo de NetworkX:
       cada punto = nodo
       cada segmento entre puntos = arista
       peso de cada arista = distancia Haversine en metros
       |
4. fix_t_junctions(): Repara intersecciones en T
       (puntos que estan sobre un camino pero no conectados)
       |
5. El grafo queda listo para consultas
       |
6. find_shortest_path(origen, destino):
       - Encuentra los nodos del grafo mas cercanos a las coordenadas dadas
       - Ejecuta nx.dijkstra_path() para encontrar la ruta
       - Simplifica la ruta con simplify_path()
       - Devuelve la lista de coordenadas y la distancia total
```


#### services/auth_service.py

Problema que resuelve: Separa la logica de autenticacion de los endpoints. Si en el futuro se cambia el metodo de autenticacion (de boleta a biometrico, por ejemplo), solo se modifica este archivo.

Como interactua: app.py lo llama cuando un usuario intenta iniciar sesion o registrarse. El servicio usa el user_repository para acceder a la base de datos.

Que pasaria si no existiera: La logica de autenticacion estaria mezclada con el codigo de las rutas en app.py, haciendo el codigo mas dificil de mantener y modificar.

Sistema de hashing de contrasenas:

Este archivo implementa un sistema completo de seguridad para contrasenas basado en bcrypt. Nunca almacena contrasenas en texto plano. El flujo funciona asi:

```
REGISTRO DE USUARIO NUEVO:
  1. El usuario escribe su contrasena: "nueva123"
  2. _hash_password("nueva123") la convierte en:
     "$2b$12$0K9cVIN3l8kss..." (hash irreversible)
  3. Solo el hash se guarda en la columna password_hash
  4. La contrasena original nunca se almacena

INICIO DE SESION:
  1. El usuario escribe su contrasena: "nueva123"
  2. _verify_password(hash_almacenado, "nueva123")
  3. bcrypt calcula el hash de "nueva123" con la misma sal
  4. Compara el resultado con el hash almacenado
  5. Si coinciden, la contrasena es correcta
  6. Si el hash es legacy (pbkdf2/scrypt), lo migra a bcrypt

MIGRACION TRANSPARENTE:
  1. Usuario con hash antiguo (pbkdf2) intenta login
  2. _verify_password detecta formato legacy
  3. Verifica con werkzeug (libreria anterior)
  4. Si la contrasena es correcta:
     a. _needs_rehash() retorna True
     b. Se genera nuevo hash bcrypt
     c. Se actualiza la base de datos
  5. En el siguiente login, ya usara bcrypt
```

Este enfoque permite actualizar el algoritmo de seguridad sin obligar a los usuarios a cambiar sus contrasenas. La migracion ocurre de forma invisible durante el login normal.


#### services/schedule_service.py

Problema que resuelve: Separa la logica de consulta de horarios. Busca las inscripciones de un alumno, encuentra las materias correspondientes, filtra las clases del dia actual y las ordena por hora.

Como interactua: app.py lo llama cuando el endpoint /api/user/schedule recibe una peticion. El servicio consulta las tablas inscripciones, materias_grupos y horarios.


### Frontend


#### components/MapComponent.jsx

Este es el componente mas complejo del frontend. Renderiza todo el mapa interactivo con mas de 500 lineas de codigo.

Como Leaflet renderiza mapas: Leaflet crea un contenedor HTML (un div) y dentro dibuja mosaicos de imagen (tiles) que forman el mapa base. Estos mosaicos se descargan de servidores publicos como OpenStreetMap. Cuando el usuario hace zoom o arrastra el mapa, Leaflet calcula que mosaicos necesita y los descarga dinamicamente.

Que es un marcador: Un marcador (Marker) es un icono que se posiciona en coordenadas especificas del mapa. En este proyecto hay marcadores para edificios, puntos de interes, la posicion del usuario y la ubicacion del coche estacionado. Cada marcador puede tener un popup (ventana emergente) con informacion adicional.

Que es una Polyline: Una Polyline es una linea compuesta por multiples segmentos que conectan una serie de puntos. Se usa para dibujar las rutas calculadas sobre el mapa. La ruta devuelta por Dijkstra es una lista de coordenadas que Leaflet conecta con una linea azul.

Como se superpone la imagen del campus: Leaflet tiene un componente llamado ImageOverlay que permite colocar una imagen sobre el mapa alineada con coordenadas geograficas reales. Se define el area geografica que cubre la imagen (esquina suroeste y esquina noreste) y Leaflet la estira para que coincida con el mapa base.

Subcomponentes internos:

- LocationMarker: Usa navigator.geolocation.watchPosition para rastrear la posicion GPS del usuario en tiempo real. Cada actualizacion mueve el circulo azul que representa al usuario en el mapa.

- MapClickHandler: Escucha el evento click del mapa. Cuando el usuario hace clic, captura las coordenadas y crea un marcador temporal pendiente de nombre.

- MapController: Usa el hook useMap() de react-leaflet para animar la camara del mapa cuando se necesita centrar en una ubicacion especifica (por ejemplo, al buscar un edificio).


#### pages/ParkingPage.jsx

Esta pagina implementa todo el sistema de estacionamiento con logica compleja de estados, temporizadores y validacion GPS.

Logica de estados de un cajon:

```
Estado: "available" (libre)
  El cajon esta vacio y disponible para cualquier usuario.
  Color visual: verde.

Estado: "reserved" (reservado)
  Un usuario ha reservado este cajon por 10 minutos.
  Nadie mas puede usar este cajon durante ese tiempo.
  Color visual: amarillo.
  Tiene temporizador activo.

Estado: "occupied" (ocupado)
  Un coche esta fisicamente estacionado en este cajon.
  Color visual: rojo.
  Muestra icono de coche.

Transiciones permitidas:
  available -> reserved (reservar)
  available -> occupied (llegar directamente)
  reserved -> occupied (el usuario llego y estaciono)
  reserved -> available (la reserva expiro automaticamente)
  occupied -> available (el usuario libero el espacio)
```

Uso de localStorage para el coche: Cuando el usuario marca un cajon como "occupied", el frontend guarda en localStorage un objeto con las coordenadas GPS del usuario en ese momento. La clave es "mi_coche_gps" y el valor es algo como: {"lat": 19.3294, "lng": -99.1116}. Cuando el usuario abre el mapa principal (MapPage), el componente MapComponent lee este valor de localStorage y muestra un marcador especial de coche en esas coordenadas. Cuando el usuario libera el espacio, se elimina esta entrada de localStorage y el marcador desaparece del mapa.


## SISTEMA DE MAPA Y NAVEGACION

Flujo completo del sistema de mapa:

```
USUARIO abre MapPage
       |
REACT carga MapComponent
       |
LEAFLET renderiza mapa base con tiles de OpenStreetMap
       |
REACT lee key_points.json y crea marcadores por cada edificio
       |
LocationMarker solicita GPS del usuario
       |  (navigator.geolocation.watchPosition)
       |
USUARIO ve su posicion como circulo azul
       |
USUARIO busca "Cafeteria" en barra de busqueda
       |
REACT filtra key_points.json y encuentra coincidencia
       |
MapController anima la camara hacia las coordenadas de Cafeteria
       |
USUARIO selecciona "Mi ubicacion" como origen y "Cafeteria" como destino
       |
REACT envia las coordenadas al backend
       |
FLASK calcula la ruta con KMLRouter + Dijkstra
       |
REACT recibe la ruta y dibuja una Polyline azul sobre el mapa
       |
USUARIO ve la ruta, distancia y tiempo estimado
```


## SISTEMA DE ESTACIONAMIENTO

Flujo completo del ciclo de vida de un cajon:

```
ESTADO INICIAL: available (libre)
       |
PASO 1: RESERVAR
       |  Usuario hace clic en cajon libre
       |  Sistema solicita GPS
       |  Sistema calcula distancia al estacionamiento (Haversine)
       |  Si distancia > 1500m -> RECHAZAR
       |  Si distancia <= 1500m -> Enviar PUT al backend
       |  Backend cambia estado a "reserved"
       |  Backend establece expiracion = ahora + 10 minutos
       |  Frontend inicia temporizador visual
       |
PASO 2: LLEGAR Y OCUPAR
       |  Usuario llega al estacionamiento
       |  Usuario hace clic en su cajon reservado
       |  Sistema solicita GPS
       |  Sistema calcula distancia a la seccion (Haversine)
       |  Si distancia > 50m -> RECHAZAR (no estas cerca del cajon)
       |  Si distancia <= 50m -> Enviar PUT al backend
       |  Backend cambia estado a "occupied"
       |  Frontend guarda coordenadas GPS en localStorage
       |  Frontend muestra icono de coche en el cajon
       |
PASO 3: COCHE VISIBLE EN MAPA PRINCIPAL
       |  Usuario abre MapPage
       |  MapComponent lee localStorage["mi_coche_gps"]
       |  Si existe, muestra marcador de coche en el mapa
       |
PASO 4: LIBERAR ESPACIO
       |  Usuario regresa a ParkingPage
       |  Hace clic en su cajon ocupado
       |  Hace clic en "Liberar Espacio"
       |  Backend cambia estado a "available"
       |  Frontend elimina localStorage["mi_coche_gps"]
       |  Marcador de coche desaparece del mapa
       |
ESTADO FINAL: available (libre de nuevo)
```

Expiracion automatica de reservas:

Si el usuario reserva un cajon pero no llega en 10 minutos, el sistema maneja la expiracion:

1. El frontend ejecuta un setInterval cada 30 segundos que revisa si hay reservas expiradas del usuario actual.
2. Cuando detecta que la hora de expiracion ya paso, muestra un modal preguntando: "Tu reserva ha expirado. Ya estacionaste tu coche?"
3. Si el usuario dice "Si", el cajon cambia a "occupied".
4. Si dice "No" o no responde, el cajon vuelve a "available".
5. Un minuto antes de la expiracion, el sistema muestra un aviso preventivo.


## BASE DE DATOS


### Que es SQL

SQL (Structured Query Language) es el lenguaje universal para comunicarse con bases de datos relacionales. Permite crear tablas, insertar datos, consultarlos, actualizarlos y eliminarlos.

Ejemplos de consultas SQL que este proyecto ejecuta internamente (a traves de SQLAlchemy):

```sql
-- Buscar un alumno por boleta
SELECT * FROM alumnos WHERE boleta = '2024001';

-- Obtener las materias de un alumno
SELECT m.nombre, g.clave, p.nombre
FROM inscripciones i
JOIN materias_grupos mg ON i.materia_grupo_id = mg.id
JOIN materias m ON mg.materia_id = m.id
JOIN grupos g ON mg.grupo_id = g.id
LEFT JOIN profesores p ON mg.profesor_id = p.id
WHERE i.alumno_id = 1;

-- Contar espacios libres por seccion
SELECT ps.name, COUNT(p.id)
FROM parking_spaces p
JOIN parking_sections ps ON p.section_id = ps.id
WHERE p.status = 'available'
GROUP BY ps.name;
```

En este proyecto no escribes SQL directamente. SQLAlchemy traduce tus consultas de Python a SQL automaticamente.


### Que es normalizacion

La normalizacion es el proceso de organizar las tablas de una base de datos para evitar la duplicacion de datos. La regla principal es: cada dato debe almacenarse en un solo lugar.

Ejemplo sin normalizar (incorrecto):

```
TABLA horarios_completos:
  alumno: "Juan"  materia: "Calculo"  profesor: "Dr. Lopez"  salon: "A-201"
  alumno: "Maria" materia: "Calculo"  profesor: "Dr. Lopez"  salon: "A-201"
```

El nombre del profesor "Dr. Lopez" esta duplicado. Si el profesor cambia de nombre, habria que actualizarlo en cada fila.

Ejemplo normalizado (correcto, como esta en este proyecto):

```
TABLA profesores:  id=1, nombre="Dr. Lopez"
TABLA materias:    id=1, nombre="Calculo"
TABLA horarios:    materia_id=1, profesor_id=1, salon_id=5
```

Ahora el nombre del profesor esta en un solo lugar. Los horarios solo guardan una referencia (el id).


### Ventajas de usar un ORM

Un ORM como SQLAlchemy ofrece estas ventajas sobre escribir SQL directamente:

1. Seguridad: Previene ataques de inyeccion SQL automaticamente.
2. Portabilidad: Puedes cambiar de SQLite a PostgreSQL cambiando una sola linea.
3. Legibilidad: El codigo Python es mas facil de leer que SQL complejo.
4. Mantenimiento: Si cambias el nombre de una columna, el ORM te avisa en lugar de fallar silenciosamente.

Ejemplo comparativo:

```python
# Con SQLAlchemy (ORM):
alumno = Alumno.query.filter_by(boleta='2024001').first()

# Sin ORM (SQL directo):
cursor.execute("SELECT * FROM alumnos WHERE boleta = ?", ('2024001',))
alumno = cursor.fetchone()
```


### Tablas del proyecto y relaciones

Diagrama de relaciones separado por base de datos:

```
BASE DE DATOS SCHOOL (instance/school.db)
=========================================
alumnos
  |--- inscripciones ---| materias_grupos |--- horarios --- salones
                        |                 |
                        |--- materias     |
                        |--- grupos       |
                        |--- profesores

BASE DE DATOS MAP (instance/map.db)
====================================
edificios

caminos

saved_places (referencia logica a alumnos.boleta)

parking_sections --- parking_spaces --- parking_reservations
                                   --- parking_history
               (occupied_by y reserved_by son referencias logicas
                a alumnos.boleta, no claves foraneas reales)
```

Las flechas entre tablas indican relaciones de clave foranea. Dentro de cada base de datos, las relaciones son claves foraneas reales que SQLite y SQLAlchemy verifican automaticamente. Entre bases de datos diferentes, las relaciones son logicas: se almacena la boleta del alumno como texto y se valida a nivel de aplicacion.


## ESTRUCTURAS DE DATOS UTILIZADAS EN EL PROYECTO

Esta seccion explica las estructuras de datos fundamentales que el proyecto utiliza internamente. Una estructura de datos es la forma en que un programa organiza la informacion en memoria para poder acceder a ella y modificarla de manera eficiente.


### Tablas hash (diccionarios)

Una tabla hash (llamada diccionario en Python y objeto en JavaScript) almacena pares de clave-valor. Permite buscar cualquier valor a partir de su clave en tiempo constante O(1), sin importar cuantos elementos contenga.

Donde se usa en el proyecto:

- Los hashes bcrypt de contrasenas. Internamente, bcrypt usa una tabla hash para mapear cada byte de la contrasena a su posicion en el cifrado Blowfish. La sal (salt) se almacena como parte del propio hash, permitiendo verificacion sin almacenar datos adicionales.
- JSON como estructura de intercambio. Toda la comunicacion entre frontend y backend usa JSON, que es esencialmente un diccionario anidado. Ejemplo: cuando el backend devuelve un usuario, lo convierte a un diccionario Python con to_dict() y Flask lo serializa a JSON.
- localStorage en el frontend. Almacena datos del usuario y del coche estacionado como pares clave-valor. La clave "user" contiene un objeto JSON con los datos del alumno. La clave "mi_coche_gps" contiene las coordenadas del coche.
- El estado de React (useState). Internamente, React almacena los estados de cada componente en una tabla hash donde la clave es la posicion del hook en el componente.

Ejemplo concreto:

```python
# Diccionario Python (tabla hash)
usuario = {
    "boleta": "2025350215",
    "nombre": "Omar Sosa",
    "carrera": "Computacion"
}
# Buscar por clave: O(1)
nombre = usuario["nombre"]  # "Omar Sosa"
```


### Grafos ponderados

Un grafo es una estructura de datos compuesta por nodos (vertices) y conexiones entre ellos (aristas). Cuando cada conexion tiene un valor numerico asociado (por ejemplo, la distancia en metros), se llama grafo ponderado.

Donde se usa en el proyecto:

- El motor de rutas (kml_router.py) construye un grafo ponderado donde cada interseccion de caminos es un nodo y cada segmento de camino es una arista con peso igual a la distancia en metros calculada con la formula de Haversine. NetworkX almacena este grafo internamente usando listas de adyacencia (diccionarios de diccionarios).

Ejemplo concreto:

```python
# Representacion interna del grafo en NetworkX
grafo = {
    "Entrada": {"Edificio1": {"weight": 100}, "Cafeteria": {"weight": 250}},
    "Edificio1": {"Entrada": {"weight": 100}, "Cafeteria": {"weight": 80}},
    "Cafeteria": {"Entrada": {"weight": 250}, "Edificio1": {"weight": 80}}
}
```

Complejidad de busqueda de ruta: El algoritmo de Dijkstra recorre este grafo en tiempo O((V + E) log V), donde V es el numero de nodos y E el numero de aristas.


### Tablas relacionales (SQL)

Una tabla relacional organiza datos en filas y columnas, similar a una hoja de calculo. Cada fila es un registro (por ejemplo, un alumno) y cada columna es un atributo (por ejemplo, la boleta). Las tablas se conectan entre si mediante claves foraneas.

Donde se usa en el proyecto:

- Las 15 tablas del sistema se organizan en dos bases de datos SQLite. Cada modelo de SQLAlchemy define una tabla con columnas tipadas (Integer, String, Float, DateTime, Boolean). Las relaciones entre tablas se definen con db.ForeignKey y db.relationship.
- La tabla materias_grupos es un ejemplo clasico de tabla relacional intermedia (tabla puente). Conecta tres entidades: una materia, un grupo y un profesor. Sin esta tabla, habria que duplicar informacion de la materia en cada horario.
- La tabla inscripciones es otra tabla puente que conecta alumnos con materias_grupos. Cada fila representa que un alumno especifico esta inscrito en una materia especifica de un grupo especifico.

Ejemplo concreto de como se relacionan las tablas:

```
Pregunta: "Que clases tiene Omar Sosa hoy miercoles?"

Paso 1: Buscar en ALUMNOS donde boleta = '2025350215'
        Resultado: alumno_id = 2

Paso 2: Buscar en INSCRIPCIONES donde alumno_id = 2
        Resultado: materia_grupo_ids = [103, 104, 105, 106, 107, 108]

Paso 3: Buscar en HORARIOS donde materia_grupo_id IN [103...108]
        Y dia_semana = 3 (miercoles)
        Resultado: lista de horarios del miercoles

Paso 4: Para cada horario, obtener el nombre de la materia
        desde MATERIAS via MATERIAS_GRUPOS
```


### Arreglos y listas

Un arreglo (array) es una secuencia ordenada de elementos accesibles por indice numerico. En Python se llaman listas y en JavaScript arrays. Son la estructura de datos mas basica y frecuente.

Donde se usa en el proyecto:

- Las rutas calculadas por Dijkstra. El resultado es una lista de coordenadas: [[19.3294, -99.1116], [19.3295, -99.1118], ...]. Leaflet recibe este arreglo y dibuja una Polyline conectando cada punto.
- Los espacios de estacionamiento se organizan en arreglos dentro de cada seccion. El frontend agrupa los cajones por fila y por seccion usando arreglos anidados.
- Los resultados de busqueda en el mapa. Cuando el usuario escribe en la barra de busqueda, el frontend filtra el arreglo de key_points.json y devuelve solo los que coinciden.


### Colas de prioridad

Una cola de prioridad es una estructura donde cada elemento tiene un valor de prioridad. El elemento con la prioridad mas alta (o mas baja, segun la implementacion) se extrae primero.

Donde se usa en el proyecto:

- El algoritmo de Dijkstra internamente usa una cola de prioridad (min-heap) para seleccionar siempre el nodo no visitado con la menor distancia acumulada. NetworkX implementa esto usando el modulo heapq de Python.
- El sistema de notificaciones de clases. NotificationContext ordena las clases del dia por hora de inicio y verifica la mas proxima primero.


## SEGURIDAD DEL SISTEMA

Esta seccion explica las medidas de seguridad implementadas en el proyecto y los principios detras de cada una.


### Almacenamiento seguro de contrasenas

Regla fundamental: las contrasenas nunca se almacenan en texto plano. Si un atacante obtiene acceso a la base de datos, no puede leer las contrasenas de los usuarios.

El sistema utiliza bcrypt para convertir cada contrasena en un hash irreversible antes de guardarla. El proceso completo es:

```
Contrasena original:  "nueva123"
                         |
                         v
bcrypt.gensalt() genera sal aleatoria: "$2b$12$Rn7mG..."
                         |
                         v
bcrypt.hashpw() aplica 12 rondas de Blowfish
                         |
                         v
Hash almacenado:  "$2b$12$Rn7mG.../a1b2c3d4e5f6..."
                         |
                         v
Se guarda en la columna password_hash de la tabla alumnos
```

Importante: ni siquiera el administrador del servidor puede ver la contrasena original. Si un usuario olvida su contrasena, no se puede recuperar: hay que generar una nueva.


### Migracion transparente de algoritmos

Cuando se actualiza el algoritmo de hashing (como ocurrio al migrar de pbkdf2 a bcrypt), el sistema implementa una estrategia llamada migracion transparente. El proceso detecta automaticamente el formato del hash almacenado durante el login:

- Si el hash comienza con "$2b$", es bcrypt actual. Se verifica con bcrypt.checkpw().
- Si el hash comienza con "pbkdf2:" o "scrypt:", es un formato anterior. Se verifica con la funcion de werkzeug. Si la contrasena es correcta, se genera un nuevo hash bcrypt y se reemplaza en la base de datos.

De esta forma, los usuarios no necesitan cambiar sus contrasenas manualmente. La migracion ocurre de forma invisible la proxima vez que inician sesion.


### Validacion de datos de entrada

Todos los datos que el usuario envia al servidor se validan antes de procesarlos:

- Las boletas deben ser cadenas de 7 a 15 digitos numericos.
- Los nombres deben tener entre 2 y 100 caracteres.
- Las contrasenas deben tener al menos 6 caracteres.
- Los correos electronicos deben tener formato valido.

Estas validaciones previenen errores y protegen contra ataques de inyeccion.


### Proteccion contra enumeracion de usuarios

Cuando alguien intenta iniciar sesion con una boleta que no existe, el sistema no revela si el problema es la boleta o la contrasena. Siempre responde con un mensaje generico: "Credenciales incorrectas". Esto evita que un atacante pueda determinar que boletas estan registradas en el sistema.


## EJEMPLOS PRACTICOS


### Ejemplo 1. Un estudiante busca su salon

Situacion: Juan es estudiante nuevo. Tiene clase de Calculo en el salon A-201 pero no sabe donde esta.

Lo que hace Juan:

1. Abre la aplicacion en su celular.
2. Inicia sesion con su boleta.
3. Va al Dashboard y ve su horario. La clase de Calculo dice "Salon A-201, Edificio 2".
4. Hace clic en "Navegar" junto a la clase.

Lo que ocurre internamente:

1. React lee la ubicacion GPS de Juan con navigator.geolocation (origen).
2. React busca las coordenadas del Edificio 2 en key_points.json (destino).
3. React envia ambas coordenadas al endpoint /api/navigation/walking-route.
4. Flask recibe la peticion y llama a kml_router.find_shortest_path().
5. KMLRouter busca los nodos del grafo mas cercanos al origen y destino.
6. NetworkX ejecuta Dijkstra y encuentra la ruta optima.
7. KMLRouter simplifica la ruta con Douglas-Peucker.
8. Flask responde con la ruta (lista de coordenadas), distancia (245m) y tiempo (3.2 min).
9. React dibuja una linea azul sobre el mapa y muestra "245m, 3 minutos caminando".
10. Juan sigue la linea azul en su pantalla hasta llegar al Edificio 2.


### Ejemplo 2. Un estudiante reserva estacionamiento

Situacion: Maria va camino a la escuela en su auto. Quiere asegurarse de que haya lugar para estacionar.

Lo que hace Maria:

1. Desde el autobus (a 1.2 km de la escuela), abre la aplicacion.
2. Va a la seccion de Estacionamiento.
3. Ve que la Seccion 2 tiene 15 lugares libres.
4. Hace clic en el cajon 2-014 (libre) y selecciona "Reservar".

Lo que ocurre internamente:

1. React solicita la ubicacion GPS de Maria.
2. React calcula la distancia entre Maria y el centro del estacionamiento usando Haversine: 1,200 metros.
3. Como 1,200m es menor a 1,500m (limite maximo), la reserva procede.
4. React envia PUT a /api/parking/spaces/104/status con status="reserved".
5. Flask cambia el estado del cajon 2-014 a "reserved", registra la boleta de Maria y establece expiracion a las 8:45 (si son las 8:35).
6. React muestra el cajon en amarillo con un temporizador: "9:58, 9:57, 9:56..."
7. Maria llega a la escuela 7 minutos despues.
8. Abre la app, hace clic en su cajon reservado y selecciona "Ya estacione mi coche".
9. React solicita GPS. Maria esta a 30 metros de la Seccion 2 (menos de 50m).
10. Flask cambia el estado a "occupied". React guarda las coordenadas en localStorage.
11. Mas tarde, en el mapa principal, Maria ve un icono de coche indicando donde estaciono.


### Ejemplo 3. Un estudiante recibe una notificacion de clase

Situacion: Pedro esta en la cafeteria y no se ha dado cuenta de que su clase de Fisica empieza en 12 minutos.

Lo que ocurre internamente:

1. El Dashboard de Pedro cargo su horario al abrir la pagina. React almaceno las clases del dia en el estado.
2. NotificationContext tiene un intervalo que revisa cada minuto si alguna clase esta a menos de 15 minutos de comenzar.
3. El contexto detecta que Fisica empieza a las 10:00 y son las 9:48. Diferencia: 12 minutos (menor a 15).
4. React genera una notificacion: "Fisica empieza en 12 minutos. Salon B-305, Edificio 3."
5. La notificacion aparece en el Dashboard con un boton "Navegar".
6. Pedro hace clic en "Navegar".
7. React navega a MapPage pasando las coordenadas del Edificio 3 como parametro.
8. MapPage detecta que recibio coordenadas de destino y calcula la ruta automaticamente desde la ubicacion actual de Pedro.
9. Pedro ve la ruta en el mapa y llega a tiempo a su clase.


## COMO EXTENDER EL PROYECTO

Este proyecto esta disenado para ser modular y extensible. A continuacion se presentan ideas para mejorarlo:

Agregar mas edificios. Edita el archivo key_points.json y agrega nuevas entradas con nombre, latitud y longitud. Los nuevos puntos apareceran automaticamente en el mapa.

Mejorar el sistema de rutas. Agrega mas caminos al archivo KML usando Google Earth o herramientas similares. El enrutador KML reconstruira el grafo automaticamente con los nuevos caminos.

Crear una aplicacion movil nativa. El backend ya expone una API REST completa. Puedes construir una aplicacion en React Native, Flutter o Swift que consuma los mismos endpoints.

Agregar un sistema de reportes. Crea un nuevo modelo en models.py para registrar incidencias (banos fuera de servicio, obras en proceso, etc.) y un endpoint en app.py para consultarlos.

Mejorar el estacionamiento con sensores IoT. Agrega sensores que detecten automaticamente si un cajon esta ocupado. Conecta esos sensores a un endpoint que actualice el estado en la base de datos.

Agregar autenticacion real con Azure AD. Configura las variables AZURE_TENANT_ID, AZURE_CLIENT_ID y AZURE_CLIENT_SECRET con los valores proporcionados por el departamento de TI de la escuela.


## CONSEJOS PARA ESTUDIANTES

Si estas comenzando a estudiar este proyecto, sigue este orden recomendado:

1. Lee primero este README completo. Antes de tocar el codigo, entiende la vision general del proyecto y como se conectan todas las piezas.

2. Ejecuta el proyecto. Sigue los pasos de instalacion y ejecucion. Navega por la aplicacion, crea un usuario, busca edificios, calcula rutas y prueba el estacionamiento. Entender el producto te ayudara a entender el codigo.

3. Empieza por el backend. El backend es mas sencillo conceptualmente. Empieza leyendo models.py para entender la estructura de datos. Luego lee config.py para entender como se configura. Finalmente lee app.py para ver como se exponen los datos.

4. Pasa al frontend. Empieza por App.jsx para ver las rutas. Luego lee Login.jsx (es la pagina mas sencilla). Despues Dashboard.jsx. Deja MapComponent.jsx para el final porque es el mas complejo.

5. Modifica cosas pequenas. Cambia el color de un boton. Agrega un nuevo punto de interes a key_points.json. Modifica el tiempo de reserva de 10 a 15 minutos. Estas modificaciones te daran confianza.

6. Usa las herramientas de desarrollo del navegador. Presiona F12 en Chrome para abrir las herramientas de desarrollo. En la pestana Network puedes ver las peticiones que el frontend envia al backend. En la pestana Console puedes ver los mensajes de error.

7. Lee la documentacion oficial. Cada tecnologia tiene documentacion excelente: React (react.dev), Flask (flask.palletsprojects.com), Leaflet (leafletjs.com), SQLAlchemy (docs.sqlalchemy.org).

8. No intentes entender todo de golpe. Este proyecto tiene miles de lineas de codigo. Es normal no entender todo la primera vez. Enfocate en una seccion a la vez y avanza gradualmente.

9. Experimenta sin miedo. Git te permite deshacer cualquier cambio. Si rompes algo, escribe git checkout . en la terminal para volver al estado anterior.


## Migración y limpieza de datos después de la refactorización

Esta sección documenta los cambios realizados durante la migración posterior a la refactorización del sistema el 10 de marzo de 2026.


### Limpieza de datos realizada

Se eliminaron 9 cuentas de usuario que pertenecían a datos de prueba y versiones anteriores del sistema. Solo se conservaron las cuentas de produccion:

- Adrian Frias (boleta: 2024351279)
- Omar Sosa (boleta: 2025350215)

La limpieza siguió el orden correcto de eliminación para respetar las restricciones de claves foraneas:

1. Inscripciones de los usuarios eliminados (84 registros)
2. Registros de alumnos (9 usuarios eliminados)


### Sistema de hashing de contraseñas implementado

Se migró el sistema de almacenamiento de contraseñas de pbkdf2:sha256 (werkzeug) a bcrypt.

Características de la implementación:

- Algoritmo: bcrypt via la librería bcrypt de Python
- Las contraseñas nunca se almacenan en texto plano
- Las contraseñas no son reversibles
- Ni siquiera el administrador del servidor puede ver la contraseña original
- El sistema verifica contraseñas usando comparación de hash

Migración transparente implementada:

- Si un usuario tiene un hash legacy (pbkdf2 o scrypt), el sistema lo verifica usando werkzeug
- Después de una autenticación exitosa con hash legacy, el hash se actualiza automáticamente a bcrypt
- Los nuevos registros y cambios de contraseña siempre usan bcrypt

Archivos modificados:

- services/auth_service.py: Método _hash_password() para generar hashes bcrypt, método _verify_password() para verificar contraseñas con soporte dual (bcrypt + legacy), método _needs_rehash() para detectar hashes que necesitan actualización
- requirements.txt: Se agregó bcrypt como dependencia


### Limpieza de bases de datos antiguas

Se identificaron y eliminaron 4 bases de datos que pertenecían a versiones anteriores del sistema:

- backend/campus.db: Base de datos original antes de la separación en map.db y school.db
- backend/instance/campus.db: Copia en directorio instance de la base legacy
- backend/instance/campus_backup_20260214_133603.db: Backup manual de la base legacy
- backend/school.db: Duplicado en la raíz del backend (la activa está en instance/)

Se crearon backups automáticos de todos los archivos antes de eliminarlos en backend/backups_pre_migration/.

Bases de datos que permanecen activas:

- instance/map.db: Edificios, rutas, estacionamiento, lugares guardados
- instance/school.db: Alumnos, materias, horarios, inscripciones


### Cambios realizados en los horarios

Se corrigió el horario de la materia Estructura de Datos para el grupo 3CV35.

El problema era que dos días tenían horarios incorrectos que mostraban la clase en turno matutino/vespertino cuando debería ser turno nocturno:

- Martes: se corrigió de 15:00-16:30 a 19:00-20:30
- Viernes: se corrigió de 16:30-18:00 a 20:30-22:00

El horario corregido es:

```
Lunes:    18:00 - 19:30
Martes:   19:00 - 20:30 (corregido)
Miércoles: 20:30 - 22:00
Jueves:   19:00 - 20:30
Viernes:  20:30 - 22:00 (corregido)
```

La corrección aplica para ambos usuarios (Omar Sosa y Adrian Frias) ya que comparten el mismo grupo y materia.

El script de migración utilizado se encuentra en backend/migrate_post_refactor.py.