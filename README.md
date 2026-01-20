# Mapa Interactivo ESIME Culhuacán

¡Bienvenido! Este proyecto es una aplicación web completa para navegar por la ESIME Culhuacán.
Fue diseñado no solo para ser útil, sino también para **enseñar cómo funciona una aplicación real** por dentro. Si eres estudiante y quieres aprender a programar sistemas web, ¡este proyecto te ayudara mucho!

---

## ¿Qué hace este proyecto?

Imagina que es como un "Google Maps" pero privado para la escuela.
1.  **Te muestra un mapa** de la escuela con todos sus edificios.
2.  **Te dice dónde estacionarte**: Muestra qué lugares están libres u ocupados.
3.  **Te guía a tu clase**: Si tienes clase a las 7:00 AM, te traza la ruta desde la entrada hasta tu salón.
4.  **Inicios de sesión**: Puedes entrar con tu número de boleta o con tu correo institucional (Outlook).

---

## ¿Cómo funciona? (Arquitectura)

Las aplicaciones web modernas se dividen en dos partes principales. Aquí aprenderás ambas:

### 1. El Frontend (Lo que ves)
Es la "cara" de la aplicación. Todo lo que el usuario toca y ve en la pantalla.
*   **Tecnologías**: React, JavaScript, HTML, CSS (Tailwind).
*   **¿Dónde está?**: En la carpeta `frontend/`.
*   **Librería Clave**: `React-Leaflet` (es la que dibuja el mapa y los marcadores).

### 2. El Backend (El cerebro)
Es el servidor que guarda los datos y hace los cálculos difíciles.
*   **Tecnologías**: Python, Flask, SQLite.
*   **¿Dónde está?**: En los archivos `app.py`, `models.py`.
*   **Librerías Clave**: 
    *   `Flask` (para crear el servidor web).
    *   `SQLAlchemy` (para hablar con la base de datos).
    *   `NetworkX` (lo usamos para calcular la "ruta más corta" entre salones, ¡matemáticas aplicadas!).

---

## Instalación paso a paso

Si estás empezando desde cero, sigue estos pasos:

### Prerrequisitos
Necesitas tener instalado en tu computadora:
1.  **Python** (para el cerebro).
2.  **Node.js** (para la cara).

### Paso 1: Descargar y preparar
Abre tu terminal y ubícate en la carpeta del proyecto.

### Paso 2: Crear el "Entorno Virtual" (Python)
Esto es como una caja aislada para que las librerías de este proyecto no se mezclen con otras cosas.
```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows es: .venv\Scripts\activate
```

### Paso 3: Instalar dependencias del Backend
Le decimos a Python que instale las herramientas necesarias (Flask, etc).
```bash
pip install -r requirements.txt
```
*(Si no tienes requirements.txt, instala manual: `pip install flask flask-sqlalchemy flask-cors networkx openpyxl numpy`)*

### Paso 4: Instalar dependencias del Frontend
Ahora instalamos las herramientas de JavaScript (React, Mapas, Estilos).
```bash
cd frontend
npm install
cd ..
```

---

## ▶¿Cómo iniciar la app?

Hemos creado un script que enciende todo por ti (Backend y Frontend al mismo tiempo).

Solamente ejecuta en la terminal:
```bash
./run_app.sh
```

Verás que se abren dos cosas:
1.  El servidor en el puerto **5001**.
2.  La página web en `http://localhost:5173`. ¡Ábrela en tu navegador!

---

## Archivos Importantes (Tu mapa de aprendizaje)

Para que no te pierdas, aquí te explico qué hace cada archivo importante:

*   **`app.py`**: Es el archivo principal de Python. Aquí se definen las "Rutas" (URLs) como `/login` o `/ruta`.
*   **`models.py`**: Define cómo es la Base de Datos. Dice "Un Usuario tiene nombre y boleta" o "Un Edificio tiene coordenadas".
*   **`poblar_bd.py`**: ¡Importante! Este script borra y vuelve a crear la base de datos con datos de prueba. Si modificas algo y no se ve, corre este script.
*   **`frontend/src/pages/`**: Aquí están las pantallas de la app:
    *   `Login.jsx`: La pantalla de entrada.
    *   `MapPage.jsx`: ¡El mapa interactivo!
    *   `Dashboard.jsx`: La pantalla de horarios.
*   **`frontend/src/mapConfig.js`**: Aquí controlas el centro del mapa y el zoom.

---

## Retos para aprender

Si quieres practicar, intenta esto:

1.  **Personalizar el Mapa**:
    *   Sigue la guía en `GUIA_MAPA.md`. Intenta poner una imagen real de la ESIME encima del mapa.

2.  **Agregar un Amigo**:
    *   Abre `poblar_bd.py`, busca donde se agregan usuarios y añade a un compañero con su boleta. Luego corre `python3 poblar_bd.py` y prueba iniciar sesión con él.

3.  **Cambiar colores**:
    *   Los colores de "Ocupado" y "Libre" en el estacionamiento están en `MapComponent.jsx`. Intenta cambiarlos a Azul y Naranja.

---

## Autenticación con Outlook

El proyecto soporta iniciar sesión con cuentas de Microsoft.
Para que esto funcione en la vida real, necesitas registrar la app en **Azure Portal** y poner tu `CLIENT_ID` en el archivo `frontend/src/authConfig.js`.

