# Mapa Interactivo ESIME Culhuacan


## INTRODUCCION

Este proyecto es una aplicacion web completa que permite a los estudiantes de la Escuela Superior de Ingenieria Mecanica y Electrica (ESIME) Culhuacan navegar dentro del campus de forma interactiva.

Imagina que llegas a la escuela por primera vez y no sabes donde esta tu salon, la cafeteria o el gimnasio. Esta aplicacion te muestra un mapa del campus, calcula la ruta mas corta entre dos puntos y ademas te permite reservar un lugar en el estacionamiento desde tu celular.

El proyecto resuelve tres problemas concretos:

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

Logica de negocio. Entenderas reglas como: un usuario solo puede reservar un espacio si esta a menos de 1.5 km de la escuela, o una reserva expira automaticamente despues de 10 minutos.


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

Se eligio porque es la herramienta mas utilizada en la industria para construir interfaces web modernas e interactivas.


### JavaScript

JavaScript es el lenguaje de programacion que ejecuta el navegador web. Todo lo que ves moverse, cambiar de color o responder a un clic en una pagina web esta controlado por JavaScript. En este proyecto, React usa JavaScript internamente.

Se usa porque es el unico lenguaje que los navegadores entienden de forma nativa para logica en la interfaz.


### SQLite

SQLite es un sistema de base de datos que almacena toda la informacion en un solo archivo dentro del proyecto. No requiere instalar un servidor de base de datos separado como MySQL o PostgreSQL.

Se eligio porque es ideal para desarrollo local y aprendizaje: un solo archivo llamado campus.db contiene todas las tablas con usuarios, horarios, estacionamiento y mas.


### SQLAlchemy

SQLAlchemy es un ORM (Object-Relational Mapper) para Python. Un ORM permite trabajar con la base de datos usando clases y objetos de Python en lugar de escribir consultas SQL directamente. Por ejemplo, en vez de escribir SELECT * FROM alumnos WHERE boleta = '2024001', se escribe Alumno.query.filter_by(boleta='2024001').first().

Se eligio porque simplifica enormemente el trabajo con la base de datos y reduce errores.


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

Si aparece un numero como 10.9.2, lo tienes instalado. Se instala automaticamente junto con Node.js.


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

Esto creara una carpeta con todo el codigo del proyecto.


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

Las dependencias son bibliotecas externas que el proyecto necesita. Se instalan con pip, el gestor de paquetes de Python:

```
pip install flask flask-cors flask-sqlalchemy python-dotenv networkx
```

Cada paquete cumple una funcion:

- flask: el framework web del servidor.
- flask-cors: permite que el frontend (en otro puerto) se comunique con el backend.
- flask-sqlalchemy: conecta Flask con la base de datos usando el ORM.
- python-dotenv: carga variables de entorno desde un archivo .env.
- networkx: biblioteca de grafos para calcular rutas con Dijkstra.


### Paso 6. Inicializar la base de datos

El backend crea las tablas automaticamente al arrancar, pero si necesitas generar los espacios de estacionamiento manualmente:

```
cd backend
python3 init_parking.py
```


### Paso 7. Instalar las dependencias del frontend

Regresa a la raiz del proyecto y entra a la carpeta del frontend:

```
cd ../frontend
npm install
```

Este comando lee el archivo package.json y descarga todas las bibliotecas listadas ahi (React, Leaflet, Tailwind, etc.) a una carpeta llamada node_modules.


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

Veras un mensaje indicando que Vite esta sirviendo la aplicacion en http://localhost:5173. Abre esa direccion en tu navegador.


### Acceder a la aplicacion

Abre tu navegador web (Chrome, Firefox, Safari) y visita:

```
http://localhost:5173
```

Veras la pantalla de inicio de sesion. Puedes registrar un usuario nuevo con cualquier numero de boleta para explorar la aplicacion.


## ESTRUCTURA DEL PROYECTO

El proyecto esta dividido en dos grandes carpetas: backend y frontend. A continuacion se muestra el arbol completo con una explicacion de cada parte.

```
Mapa_interactivo_ESIME_CULHUACAN/
|
|-- backend/                         Servidor en Python (Flask)
|   |-- app.py                       Punto de entrada principal del servidor
|   |-- config.py                    Configuracion de entornos (local e institucional)
|   |-- models.py                    Definicion de tablas de la base de datos
|   |-- kml_router.py                Motor de calculo de rutas con Dijkstra
|   |-- audit_routes.py              Script de depuracion para probar rutas
|   |-- init_parking.py              Script para generar espacios de estacionamiento
|   |-- seed_parking.py              Script para poblar datos de estacionamiento
|   |-- seed_inscripciones.py        Script para crear inscripciones de prueba
|   |-- fix_inscriptions.py          Script para corregir inscripciones
|   |
|   |-- middleware/                   Funciones que se ejecutan antes de las rutas
|   |   |-- __init__.py              Paquete del modulo de middleware
|   |   |-- auth_middleware.py       Decoradores de autenticacion
|   |
|   |-- repositories/                Capa de acceso a datos
|   |   |-- __init__.py              Fabricas de repositorios
|   |   |-- user_repository.py       Interfaz abstracta de usuarios
|   |   |-- sqlite_repository.py     Implementacion concreta con SQLite
|   |
|   |-- services/                    Logica de negocio separada
|   |   |-- __init__.py              Paquete del modulo de servicios
|   |   |-- auth_service.py          Servicio de autenticacion
|   |   |-- schedule_service.py      Servicio de horarios
|   |
|   |-- scripts/                     Scripts de utilidad
|       |-- import_horarios.py       Importa horarios desde archivo SQL
|
|-- frontend/                        Aplicacion React (interfaz grafica)
|   |-- index.html                   Pagina HTML raiz
|   |-- package.json                 Lista de dependencias del frontend
|   |-- vite.config.js               Configuracion del compilador Vite
|   |-- tailwind.config.js           Configuracion de Tailwind CSS
|   |
|   |-- src/                         Codigo fuente de React
|       |-- main.jsx                 Punto de entrada de React
|       |-- App.jsx                  Componente raiz con las rutas de la app
|       |-- index.css                Estilos globales
|       |-- authConfig.js            Configuracion de Azure AD
|       |-- mapConfig.js             Importa la configuracion del mapa
|       |-- mapConfig.json           Coordenadas y ajustes del mapa
|       |-- locations.json           Listado de ubicaciones estaticas
|       |
|       |-- components/              Componentes reutilizables
|       |   |-- MapComponent.jsx     Componente principal del mapa interactivo
|       |   |-- ParkingSectionMap.jsx Plano visual 2D de una seccion
|       |   |-- SavedPlacesSheet.jsx  Panel de lugares guardados
|       |
|       |-- pages/                   Paginas completas de la aplicacion
|       |   |-- Login.jsx            Pagina de inicio de sesion y registro
|       |   |-- Dashboard.jsx        Perfil del usuario y horario de clases
|       |   |-- MapPage.jsx          Pagina contenedora del mapa
|       |   |-- ParkingPage.jsx      Pagina del sistema de estacionamiento
|       |   |-- ParkingPage.css      Estilos especificos del estacionamiento
|       |
|       |-- context/                 Contextos globales de React
|       |   |-- NotificationContext.jsx  Manejo de notificaciones de clases
|       |
|       |-- services/                Funciones de comunicacion con el backend
|       |   |-- api.js               Todas las llamadas HTTP al servidor
|       |
|       |-- data/                    Datos estaticos
|           |-- key_points.json      Puntos clave del campus (edificios, areas)
```


## CONCEPTOS BASICOS DE PROGRAMACION UTILIZADOS

Antes de analizar el codigo, es importante entender algunos conceptos fundamentales que se usan constantemente en el proyecto. Estos conceptos se explican con analogias simples.


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


### Que es una funcion

Una funcion es un bloque de codigo que realiza una tarea especifica. Es como una receta de cocina: recibe ingredientes (parametros), ejecuta pasos (instrucciones) y produce un resultado (valor de retorno).

Ejemplo en Python:

```python
def calcular_area(base, altura):
    return base * altura

resultado = calcular_area(5, 3)  # resultado es 15
```


### Que es una API

API significa Interfaz de Programacion de Aplicaciones. Es un conjunto de reglas que permiten que dos programas se comuniquen entre si.

En este proyecto, el frontend (React) necesita datos que estan en el servidor (Flask). Para obtenerlos, le envia una peticion HTTP a una direccion especifica. El servidor recibe la peticion, busca los datos en la base de datos y los devuelve en formato JSON.

Es como un mesero en un restaurante: tu (el frontend) le pides algo al mesero (la API), el va a la cocina (el backend), y te trae lo que pediste (los datos).


### Que es un endpoint

Un endpoint es una URL especifica del servidor que responde a un tipo de peticion. Cada endpoint tiene una funcion definida.

Ejemplo: el endpoint /api/user/login espera recibir un numero de boleta y devuelve los datos del usuario si existe.

Es como un numero de ventanilla: si vas a la ventanilla 3, te atienden para inscripciones. Si vas a la ventanilla 5, te atienden para credenciales.


### Que es una base de datos

Una base de datos es un sistema organizado para almacenar informacion de forma permanente. Funciona como un conjunto de tablas (similares a hojas de calculo de Excel) donde cada fila es un registro y cada columna es un dato.

Ejemplo: la tabla alumnos tiene columnas para boleta, nombre, carrera y vehiculo. Cada estudiante registrado ocupa una fila.


### Que es un algoritmo

Un algoritmo es una secuencia ordenada de pasos para resolver un problema. Es como las instrucciones para armar un mueble: si sigues los pasos en orden, llegas al resultado correcto.

En este proyecto, el algoritmo mas importante es Dijkstra, que calcula la ruta mas corta entre dos puntos.


### Que es un componente (en React)

Un componente es una pieza independiente de la interfaz que tiene su propia logica y su propia apariencia. React permite dividir la pantalla en componentes mas pequenos que se pueden reutilizar.

Ejemplo: el mapa es un componente, la barra de busqueda es otro componente y cada marcador en el mapa es otro. Juntos forman la pagina completa.


### Que es el estado (state) en React

El estado es la informacion que puede cambiar con el tiempo dentro de un componente. Cuando el estado cambia, React vuelve a dibujar automaticamente el componente para reflejar el cambio.

Ejemplo: cuando el usuario escribe en la barra de busqueda, el texto que escribio es un estado. Cada letra que agrega actualiza el estado y React actualiza lo que se muestra en pantalla.


## EXPLICACION DE CADA ARCHIVO DEL PROYECTO

A continuacion se explica cada archivo del proyecto como si fuera una pequena clase de programacion. Se describe que hace, por que existe y como funciona.


### Backend


#### app.py

Este es el archivo mas importante del backend. Es el punto de entrada de todo el servidor. Cuando ejecutas python3 app.py, Flask lee este archivo y comienza a escuchar peticiones.

Que hace: define todos los endpoints de la API, inicializa la base de datos, carga el enrutador KML y conecta todos los servicios.

Funciones principales:

- init_system(): Se ejecuta al arrancar el servidor. Crea las tablas de la base de datos si no existen, carga el grafo de caminos desde el archivo KML y crea las instancias de los servicios de autenticacion y horarios.

- Endpoint /api/user/login: Recibe un numero de boleta, busca al alumno en la base de datos y devuelve sus datos.

- Endpoint /api/user/register: Recibe los datos de un nuevo alumno (nombre, boleta, carrera, vehiculo) y lo registra en la base de datos.

- Endpoint /api/user/schedule: Recibe una boleta y devuelve el horario de clases del alumno para el dia actual.

- Endpoint /api/navigation/walking-route: Recibe coordenadas de origen y destino, calcula la ruta mas corta usando el enrutador KML y devuelve la lista de puntos del camino, la distancia total y el tiempo estimado.

- Endpoint /api/parking/spaces: Devuelve todas las secciones del estacionamiento con sus espacios y estados actuales.

- Endpoint /api/parking/spaces/<id>/status: Permite cambiar el estado de un espacio (disponible, reservado, ocupado). Maneja la logica de expiracion de reservas (10 minutos).


#### config.py

Este archivo define como se comporta el servidor segun el entorno donde se ejecute.

Que hace: proporciona dos configuraciones diferentes. En modo local usa SQLite y autenticacion por boleta. En modo institucional usa Azure AD y una base de datos externa.

Clases principales:

- LocalConfig: Configuracion para desarrollo. Usa el archivo campus.db como base de datos.

- InstitutionalConfig: Configuracion para produccion. Lee las credenciales de variables de entorno.

- get_config(): Funcion que lee la variable APP_ENV y devuelve la configuracion correspondiente.


#### models.py

Este archivo define la estructura de todas las tablas de la base de datos usando SQLAlchemy. Cada clase representa una tabla.

Modelos definidos:

- EdificioDB: Almacena edificios con su nombre y coordenadas geograficas.

- CaminoDB: Almacena conexiones directas entre dos puntos, usadas para calcular rutas.

- Alumno: Datos del estudiante (boleta, nombre, carrera, vehiculo, proveedor de autenticacion).

- Materia: Asignaturas del plan de estudios con nombre, codigo, creditos y semestre.

- Profesor: Datos del docente (nombre, email, departamento).

- Salon: Espacios fisicos de clase con capacidad y tipo (aula, laboratorio, auditorio).

- Grupo: Organizacion academica (clave de grupo como "1CM54", semestre, turno).

- MateriaGrupo: Tabla relacional que conecta una materia con un grupo y un profesor.

- Horario: Dias y horas en que se imparte cada materia de cada grupo.

- Inscripcion: Registro de que un alumno esta inscrito en una materia de un grupo.

- SavedPlace: Lugares personalizados que el usuario guarda en el mapa.

- ParkingSection: Secciones del estacionamiento (Seccion 1, 2, 3, 4).

- ParkingSpace: Cada cajon individual con su estado, coordenadas y quien lo ocupa o reserva.

- ParkingReservation: Historial de reservas con tiempos de creacion y expiracion.

- ParkingHistory: Bitacora de todos los cambios de estado de los cajones.


#### kml_router.py

Este es el cerebro del sistema de navegacion. Lee un archivo KML (formato de datos geograficos usado por Google Earth) y construye un grafo de caminos peatonales del campus.

Que hace: parsea el archivo KML para extraer linestrings (lineas de coordenadas), construye un grafo de NetworkX donde cada interseccion es un nodo y cada segmento de camino es una arista con un peso igual a la distancia en metros.

Funciones principales:

- haversine_distance(): Calcula la distancia en metros entre dos puntos dados por latitud y longitud. Usa la formula de Haversine que toma en cuenta la curvatura de la Tierra.

- simplify_path(): Reduce el numero de puntos de una ruta usando el algoritmo de Douglas-Peucker. Esto hace que las rutas se dibujen mas rapido en el mapa sin perder precision visual.

- find_shortest_path(): Recibe un punto de origen y un punto de destino, los conecta al nodo mas cercano del grafo y calcula la ruta mas corta con Dijkstra. Devuelve la lista de coordenadas del camino y la distancia total.

- fix_t_junctions(): Repara la topologia del grafo detectando nodos que estan sobre una arista pero no estan conectados a ella. Esto es comun cuando un camino secundario nace de la mitad de un camino principal.


#### middleware/auth_middleware.py

Contiene funciones decoradoras que protegen los endpoints. Un decorador es una funcion que envuelve a otra funcion para agregar comportamiento adicional.

- require_auth: Verifica que el usuario haya iniciado sesion antes de permitir el acceso a un endpoint. Si no esta autenticado, devuelve un error 401.

- optional_auth: Similar a require_auth pero no bloquea el acceso. Si el usuario esta autenticado, agrega sus datos a la peticion. Si no, permite el acceso sin datos de usuario.


#### repositories/user_repository.py

Define una clase abstracta que establece los metodos que cualquier implementacion de repositorio de usuarios debe tener. Esto permite cambiar de base de datos sin modificar el resto del codigo.

Metodos definidos: find_by_boleta, find_by_email, create_user, update_user.


#### repositories/sqlite_repository.py

Implementacion concreta del repositorio que usa SQLite para almacenar y recuperar datos de usuarios y horarios. Contiene las consultas reales a la base de datos.


#### services/auth_service.py

Contiene la logica de autenticacion separada de las rutas. Tiene metodos para verificar credenciales y manejar el flujo de login tanto local (por boleta) como institucional (por Azure AD).


#### services/schedule_service.py

Contiene la logica para obtener el horario de un alumno. Busca las inscripciones del alumno, encuentra las materias correspondientes y filtra las clases del dia actual.


#### init_parking.py

Script que se ejecuta una sola vez para crear las secciones y los espacios de estacionamiento en la base de datos. Genera 4 secciones con 90, 90, 85 y 80 espacios respectivamente, cada uno con coordenadas GPS calculadas automaticamente.


#### seed_parking.py

Script complementario para poblar datos de estacionamiento. Util para desarrollo y pruebas.


#### seed_inscripciones.py

Script que crea inscripciones de prueba asociando alumnos con materias y grupos. Se usa durante el desarrollo para tener datos de horarios sin importar datos reales.


#### fix_inscriptions.py

Script de correccion que revisa y repara inscripciones con datos inconsistentes.


#### scripts/import_horarios.py

Lee un archivo SQL con datos de horarios reales y los importa a la base de datos. Parsea el formato de horarios para extraer materia, grupo, profesor, salon, dia y hora.


### Frontend


#### main.jsx

Punto de entrada de la aplicacion React. Monta el componente raiz App dentro del DOM del navegador. Envuelve la aplicacion con el proveedor de MSAL (para autenticacion Microsoft) y React.StrictMode (para detectar errores durante desarrollo).


#### App.jsx

Define las rutas de la aplicacion. Usa React Router para mostrar una pagina diferente segun la URL:

- / muestra la pagina Login
- /map muestra la pagina MapPage
- /dashboard muestra la pagina Dashboard
- /parking muestra la pagina ParkingPage

Tambien incluye el NotificationProvider que hace disponibles las notificaciones en toda la aplicacion.


#### authConfig.js

Contiene la configuracion de Azure AD para iniciar sesion con cuenta institucional de Microsoft. Define el ID del cliente, la URL de redireccion y los permisos solicitados.


#### mapConfig.js y mapConfig.json

mapConfig.json almacena las coordenadas centrales del mapa, el nivel de zoom inicial y los limites del area visible. mapConfig.js simplemente importa y exporta esos datos.


#### services/api.js

Contiene todas las funciones que hacen peticiones HTTP al backend. Cada funcion representa una accion: iniciar sesion, registrarse, obtener horarios, calcular rutas, guardar lugares, gestionar estacionamiento.

Funciones principales:

- login(boleta): Envia la boleta al servidor y devuelve los datos del usuario.
- register(data): Registra un nuevo usuario.
- getSchedule(boleta): Obtiene el horario de clases del dia actual.
- getWalkingRoute(params): Envia coordenadas al servidor y recibe la ruta calculada.
- getParking(): Obtiene todos los espacios de estacionamiento y sus estados.
- getSavedPlaces(boleta): Obtiene los lugares guardados por el usuario.
- savePlace(data): Guarda un nuevo lugar personalizado.
- deletePlace(id): Elimina un lugar guardado.


#### context/NotificationContext.jsx

Crea un contexto de React que permite compartir el estado de notificaciones entre todos los componentes. Cuando el horario del alumno se carga, analiza si alguna clase esta por comenzar en los proximos 15 minutos y genera una notificacion.


#### components/MapComponent.jsx

Este es el componente mas complejo del frontend. Renderiza todo el mapa interactivo con todas sus funcionalidades.

Funcionalidades incluidas:

- Muestra el mapa del campus con una capa de imagen superpuesta.
- Muestra marcadores para todos los edificios y puntos de interes.
- Muestra la ubicacion del usuario en tiempo real con GPS.
- Permite buscar edificios por nombre en la barra de busqueda.
- Permite agregar marcadores personalizados haciendo clic en el mapa.
- Incluye un modo de navegacion donde el usuario selecciona origen y destino.
- Dibuja la ruta calculada sobre el mapa como una linea azul.
- Muestra un marcador especial donde el usuario estaciono su coche.
- Permite filtrar por tipo de lugar (cafeteria, gimnasio, auditorio, etc.).

Subcomponentes internos:

- LocationMarker: Rastrea la posicion GPS del usuario y la muestra como un circulo azul.
- MapClickHandler: Detecta cuando el usuario hace clic en el mapa para agregar un pin.
- MapController: Anima la camara del mapa hacia una ubicacion objetivo.


#### components/ParkingSectionMap.jsx

Muestra un plano visual 2D de la seccion activa del estacionamiento. Si la seccion tiene una imagen de mapa asignada, la muestra. Si no, muestra un estado vacio con un mensaje explicativo.


#### components/SavedPlacesSheet.jsx

Panel deslizable que muestra los lugares guardados por el usuario. Permite agregar nuevos lugares de la lista de edificios del sistema y ver los que ya ha guardado previamente.


#### pages/Login.jsx

Pagina de inicio de sesion con tres vistas posibles:

1. Login: El usuario ingresa su boleta o inicia sesion con Microsoft.
2. Registro: El usuario crea una nueva cuenta con nombre, boleta, carrera y vehiculo.
3. Completar Perfil: Si el usuario inicia con Microsoft pero no tiene cuenta, completa sus datos.


#### pages/Dashboard.jsx

Pagina de perfil del usuario que muestra:

- Nombre, boleta y carrera del estudiante.
- Selector de vehiculo (ninguno, automovil, motocicleta, bicicleta).
- Lista de materias inscritas con horarios ordenados cronologicamente.
- Indicador de "En curso" para la clase que se esta impartiendo actualmente.
- Panel de notificaciones con alertas de proximas clases.
- Diseno responsive que se adapta a escritorio y movil.


#### pages/MapPage.jsx

Pagina contenedora del mapa. Se encarga de:

- Cargar los puntos de interes y lugares guardados del usuario.
- Manejar la logica de calculo de rutas: resuelve las coordenadas de origen y destino y llama al endpoint del backend.
- Detectar si la navegacion viene de una notificacion para calcular la ruta automaticamente hacia el salon correspondiente.


#### pages/ParkingPage.jsx

Pagina completa del sistema de estacionamiento. Incluye:

- Navegador de secciones con botones para cambiar entre Seccion 1, 2, 3 y 4.
- Cuadricula visual de espacios donde cada cajon muestra su estado (libre, reservado, ocupado).
- Modal de acciones: al hacer clic en un cajon, aparece un panel con las opciones disponibles (reservar, ocupar, liberar).
- Temporizador de reserva: cuando el usuario reserva un espacio, un contador muestra cuanto tiempo le queda.
- Validacion GPS: antes de reservar, verifica que el usuario este a menos de 1.5 km. Antes de ocupar, verifica que este a menos de 50 metros de la seccion.
- Modal de expiracion: cuando una reserva expira, muestra un aviso preguntando si el usuario ya estaciono su coche.
- Modal de advertencia: un minuto antes de que expire la reserva, muestra un aviso preventivo.


## EXPLICACION DE LOS ALGORITMOS


### Algoritmo de Dijkstra

El algoritmo de Dijkstra resuelve el siguiente problema: dado un mapa con multiples caminos entre puntos, encontrar la ruta mas corta entre un punto de inicio y un punto de destino.

Imagina que estas en la entrada de la escuela y quieres llegar a la cafeteria. Hay muchos caminos posibles: puedes ir por la izquierda, por la derecha, rodear el edificio 1, pasar por el estacionamiento, etc. Dijkstra los evalua todos y te dice cual es el camino mas corto en metros.

Como funciona paso a paso:

1. El mapa se representa como un grafo. Cada interseccion es un nodo y cada camino entre intersecciones es una arista. Cada arista tiene un peso que representa la distancia en metros.

2. El algoritmo empieza en el nodo de origen y le asigna una distancia de 0. A todos los demas nodos les asigna una distancia infinita (significando que aun no sabemos como llegar).

3. Revisa todos los vecinos del nodo actual. Para cada vecino, calcula la distancia total desde el origen pasando por el nodo actual. Si esta distancia es menor que la previamente registrada, la actualiza.

4. Marca el nodo actual como visitado (no lo revisara de nuevo) y pasa al nodo no visitado con la menor distancia.

5. Repite los pasos 3 y 4 hasta llegar al nodo destino o hasta haber visitado todos los nodos alcanzables.

6. Al terminar, reconstruye el camino siguiendo los nodos que marcaron las distancias mas cortas.

En el proyecto, el grafo se construye a partir de un archivo KML que contiene las coordenadas reales de los caminos peatonales del campus. Cada punto geografico es un nodo y cada segmento de camino es una arista cuyo peso se calcula con la formula de Haversine.


### Formula de Haversine

La formula de Haversine calcula la distancia entre dos puntos sobre la superficie de la Tierra usando sus coordenadas de latitud y longitud. Es necesaria porque la Tierra no es plana: dos puntos con la misma diferencia de coordenadas pueden estar a distancias reales diferentes segun donde se encuentren.

La formula toma en cuenta la curvatura de la Tierra multiplicando el resultado angular por el radio terrestre (6,371 km). En el proyecto se usa en dos lugares:

1. En kml_router.py para calcular el peso de cada arista del grafo.
2. En ParkingPage.jsx para medir la distancia entre el usuario y el estacionamiento.


### Algoritmo de Douglas-Peucker (simplificacion de rutas)

Cuando Dijkstra calcula una ruta, puede devolver cientos de puntos intermedios. Dibujar todos esos puntos en el mapa es lento e innecesario visualmente. El algoritmo de Douglas-Peucker reduce esa cantidad conservando solo los puntos que definen la forma general del camino.

Funciona asi: traza una linea recta entre el primer y ultimo punto del camino. Busca el punto intermedio que esta mas lejos de esa linea. Si esa distancia es mayor a un umbral (tolerancia), conserva ese punto y repite el proceso para cada mitad. Si ninguno esta suficientemente lejos, descarta todos los puntos intermedios.


## SISTEMA DE MAPA Y NAVEGACION


### Como funciona el mapa

El mapa usa la biblioteca Leaflet a traves del componente react-leaflet. Se configura con las coordenadas centrales del campus y un nivel de zoom especifico definido en mapConfig.json.

Sobre el mapa base se superpone una imagen (overlay) que muestra un plano detallado del campus. Esta imagen se alinea con las coordenadas reales para que los marcadores coincidan con los edificios.


### Como se agregan puntos al mapa

Los puntos de interes (edificios, areas) estan definidos en el archivo key_points.json. Cada punto tiene un nombre, latitud y longitud. Al cargar el mapa, React itera sobre esta lista y crea un marcador de Leaflet para cada punto.

El usuario tambien puede crear sus propios marcadores haciendo clic en el mapa. Al hacer clic, se crea un marcador temporal (pendiente) y aparece un formulario para darle nombre. Al guardar, el punto se envia al backend y se almacena en la tabla saved_places.


### Como se calculan las rutas

1. El usuario selecciona un punto de origen (puede ser su ubicacion actual) y un punto de destino.

2. El frontend obtiene las coordenadas de ambos puntos y las envia al endpoint /api/navigation/walking-route.

3. El backend recibe las coordenadas, las pasa al KMLRouter que busca los nodos mas cercanos en el grafo y ejecuta Dijkstra para encontrar la ruta mas corta.

4. La ruta obtenida se simplifica con Douglas-Peucker para reducir el numero de puntos.

5. El backend devuelve la lista de coordenadas, la distancia total en metros y el tiempo estimado caminando (asumiendo 4.5 km/h).

6. El frontend dibuja la ruta como una linea azul (Polyline) sobre el mapa.


### Como funciona la geolocalizacion

El navegador web tiene una funcion llamada navigator.geolocation.getCurrentPosition que solicita permiso al usuario y luego obtiene sus coordenadas GPS.

En el componente LocationMarker, se usa watchPosition para rastrear la ubicacion en tiempo real. Cada vez que el GPS actualiza la posicion, React actualiza el estado y mueve el marcador azul en el mapa.

Si el GPS no esta disponible o el usuario niega el permiso, la aplicacion muestra un mensaje de error pero sigue funcionando. Simplemente no puede usar "Tu ubicacion" como punto de origen.


## SISTEMA DE ESTACIONAMIENTO


### Estructura del estacionamiento

El estacionamiento esta dividido en 4 secciones:

- Seccion 1: 90 espacios
- Seccion 2: 90 espacios
- Seccion 3: 85 espacios
- Seccion 4: 80 espacios

Cada seccion tiene coordenadas GPS centrales definidas en el frontend. Cada espacio individual tiene su propio ID, numero, seccion, estado y campos para rastrear quien lo ocupa o reserva.


### Como se reserva un espacio

1. El usuario abre la pagina de estacionamiento y navega a la seccion deseada.

2. Hace clic en un cajon marcado como "Libre".

3. Aparece un modal con dos opciones: "Reservar (10 minutos)" o "Llegue directamente (Ocupar)".

4. Si elige reservar, el sistema primero obtiene su ubicacion GPS. Si esta a mas de 1.5 km de la escuela, la reserva se rechaza.

5. Si esta dentro del rango, se envia la peticion al backend que cambia el estado del cajon a "reserved", registra la boleta del usuario y establece una hora de expiracion (hora actual mas 10 minutos).

6. El frontend muestra un temporizador que cuenta los minutos restantes.


### Como funciona el temporizador

Cada componente SpaceCard tiene su propio temporizador independiente implementado con setInterval. Cada segundo calcula la diferencia entre la hora actual y la hora de expiracion. Cuando llega a cero, dispara el sistema de alertas.


### Como se detecta la ubicacion del usuario

El sistema usa el GPS del dispositivo para tres validaciones:

1. Para reservar: el usuario debe estar a menos de 1,500 metros del centro del estacionamiento.

2. Para ocupar: el usuario debe estar a menos de 50 metros de la seccion especifica donde esta el cajon.

3. Para guardarlo en el mapa: cuando el usuario marca un cajon como ocupado, sus coordenadas GPS se guardan en localStorage bajo la clave "mi_coche_gps". Esto permite mostrar un marcador de coche en el mapa principal.


### Como se marca un lugar como ocupado

1. Si el usuario tiene una reserva y llega al estacionamiento, hace clic en su cajon reservado.

2. Aparece el boton "Ya estacione mi coche".

3. El sistema verifica que esta a menos de 50 metros de la seccion. Si cumple, cambia el estado a "occupied", registra sus coordenadas GPS y guarda la ubicacion del coche.


### Como se libera un lugar

1. El usuario hace clic en su cajon ocupado.

2. Aparece el boton "Liberar Espacio (Me voy)".

3. El sistema cambia el estado a "available", limpia los campos de ocupante y reservante, y elimina la ubicacion del coche del localStorage.


## BASE DE DATOS


### Que es una base de datos relacional

Una base de datos relacional organiza la informacion en tablas que pueden estar conectadas entre si a traves de relaciones. Cada tabla tiene columnas (los tipos de datos que almacena) y filas (los registros individuales).


### Tablas del proyecto

El proyecto tiene las siguientes tablas principales:

alumnos: Almacena los datos de cada estudiante. Columnas: id, boleta (clave unica), email, nombre, carrera, vehiculo.

materias: Cada asignatura del plan de estudios. Columnas: id, nombre, codigo, creditos, semestre.

profesores: Los docentes. Columnas: id, nombre, email, departamento.

salones: Los espacios fisicos de clase. Columnas: id, nombre, edificio_id (relacion con edificios), capacidad, tipo.

grupos: Agrupaciones academicas. Columnas: id, clave (como "1CM54"), semestre, turno, carrera.

materias_grupos: Conecta una materia con un grupo y un profesor especifico. Es una tabla relacional.

horarios: Dias y horas de cada clase. Columnas: id, materia_grupo_id, dia_semana (1 a 7), hora_inicio, hora_fin, salon_id.

inscripciones: Registra que un alumno esta inscrito en una materia-grupo. Columnas: alumno_id, materia_grupo_id, estado.

edificios: Edificios del campus con coordenadas. Columnas: id, nombre, latitud, longitud.

saved_places: Lugares guardados por el usuario en el mapa. Columnas: user_boleta, name, lat, lon.

parking_sections: Las 4 secciones del estacionamiento. Columnas: id, name, total_spaces.

parking_spaces: Cada cajon individual. Columnas: id, space_number, section_id, status, occupied_by, reserved_by, reservation_expires_at.

parking_reservations: Historial de reservas. Columnas: space_id, user_boleta, reserved_at, expires_at, status.

parking_history: Registro de todos los cambios de estado (disponible, ocupado, reservado) como bitacora.


### Relaciones entre tablas

Las tablas estan conectadas mediante claves foraneas. Una clave foranea es una columna que referencia el id de otra tabla.

Ejemplo: la tabla horarios tiene una columna salon_id que apunta al id de la tabla salones. Esto permite saber en que salon se imparte cada clase sin duplicar la informacion del salon en la tabla de horarios.

Relaciones principales:

- Un alumno tiene muchas inscripciones. Cada inscripcion conecta al alumno con una materia-grupo.
- Una materia-grupo tiene muchos horarios. Cada horario define un dia y hora especifica.
- Un horario pertenece a un salon. Un salon pertenece a un edificio.
- Una seccion de estacionamiento tiene muchos espacios. Cada espacio puede tener un ocupante y un reservante (ambos son alumnos).


### Que es una clave primaria

Una clave primaria es una columna que identifica de forma unica cada fila de una tabla. Normalmente es un numero entero que se incrementa automaticamente (1, 2, 3...). En todas las tablas del proyecto, la columna id es la clave primaria.


### Que es una clave foranea

Una clave foranea es una columna que establece una relacion con otra tabla. Contiene el valor de la clave primaria de la tabla relacionada.

Ejemplo: en la tabla parking_spaces, la columna section_id es una clave foranea que apunta al id de la tabla parking_sections. Esto indica a que seccion pertenece cada cajon.


## COMO EXTENDER EL PROYECTO

Este proyecto esta disenado para ser modular y extensible. A continuacion se presentan ideas para mejorarlo:

Agregar mas edificios. Edita el archivo key_points.json y agrega nuevas entradas con nombre, latitud y longitud. Los nuevos puntos apareceran automaticamente en el mapa.

Mejorar el sistema de rutas. Agrega mas caminos al archivo KML usando Google Earth o herramientas similares. El enrutador KML reconstruira el grafo automaticamente con los nuevos caminos.

Crear una aplicacion movil nativa. El backend ya expone una API REST completa. Puedes construir una aplicacion en React Native, Flutter o Swift que consuma los mismos endpoints.

Agregar un sistema de reportes. Crea un nuevo modelo en models.py para registrar incidencias (baños fuera de servicio, obras en proceso, etc.) y un endpoint en app.py para consultarlos.

Mejorar el sistema de estacionamiento. Agrega sensores IoT que detecten automaticamente si un cajon esta ocupado. Conecta esos sensores a un endpoint que actualice el estado en la base de datos.

Agregar autenticacion real con Azure AD. Configura las variables de entorno AZURE_TENANT_ID, AZURE_CLIENT_ID y AZURE_CLIENT_SECRET con los valores proporcionados por el departamento de TI de la escuela.

Agregar un sistema de favoritos mejorado. Permite al usuario categorizar sus lugares guardados (clases frecuentes, puntos de comida, areas de descanso) y ordena la lista por frecuencia de uso.


## CONSEJOS PARA ESTUDIANTES

Si estas comenzando a estudiar este proyecto, sigue este orden recomendado:

1. Lee primero este README completo. Antes de tocar el codigo, entiende la vision general del proyecto y como se conectan todas las piezas.

2. Ejecuta el proyecto. Sigue los pasos de instalacion y ejecucion. Navega por la aplicacion, crea un usuario, busca edificios, calcula rutas y prueba el estacionamiento. Entender el producto te ayudara a entender el codigo.

3. Empieza por el backend. El backend es mas sencillo conceptualmente. Empieza leyendo models.py para entender la estructura de datos. Luego lee config.py para entender como se configura. Finalmente lee app.py para ver como se exponen los datos.

4. Pasa al frontend. Empieza por App.jsx para ver las rutas. Luego lee Login.jsx (es la pagina mas sencilla). Despues Dashboard.jsx. Deja MapComponent.jsx para el final porque es el mas complejo.

5. Modifica cosas pequenas. Cambia el color de un boton. Agrega un nuevo punto de interes a key_points.json. Modifica el tiempo de reserva de 10 a 15 minutos. Estas modificaciones te daran confianza.

6. Usa las herramientas de desarrollo del navegador. Presiona F12 en Chrome para abrir las herramientas de desarrollo. En la pestana Network puedes ver las peticiones que el frontend envia al backend. En la pestana Console puedes ver los mensajes de error o de depuracion.

7. Lee la documentacion oficial. Cada tecnologia tiene documentacion excelente: React (react.dev), Flask (flask.palletsprojects.com), Leaflet (leafletjs.com), SQLAlchemy (docs.sqlalchemy.org).

8. No intentes entender todo de golpe. Este proyecto tiene mas de 3,000 lineas de codigo. Es normal no entender todo la primera vez. Enfocate en una seccion a la vez y avanza gradualmente.

9. Experimenta sin miedo. Git te permite deshacer cualquier cambio. Si rompes algo, escribe git checkout . en la terminal para volver al estado anterior.
