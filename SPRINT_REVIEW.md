# Sprint Review: Navegación ESIME

**Duración Estimada de Lectura/Presentación:** 12 - 15 Minutos

---

## 1. Visión General del Proyecto
**Navegación ESIME** es una solución tecnológica integral diseñada para optimizar la experiencia estudiantil en la ESIME Culhuacán. El sistema combina un mapa interactivo de alta precisión con un gestor académico personalizado, permitiendo a los alumnos no solo visualizar su ubicación, sino trazar rutas inteligentes hacia sus clases actuales en tiempo real.

El proyecto ha pasado de ser un prototipo de navegación a una plataforma "Premium" que integra identidad institucional, gestión de horarios complejos y una interfaz de usuario moderna y responsiva.

---

## 2. Stack Tecnológico (Arquitectura)

Para lograr un rendimiento óptimo y una experiencia de usuario fluida, seleccionamos tecnologías modernas y robustas:

### Frontend (Interfaz de Usuario)
- **React.js + Vite**: Elegido por su velocidad y modularidad. Permite una navegación estilo SPA (Single Page Application) sin recargas.
- **Tailwind CSS**: Utilizado para todo el estilizado. Nos permitió implementar un diseño "Glassmorphism" (paneles translúcidos), gradientes institucionales y una estética limpia sin escribir CSS pesado.
- **React-Leaflet**: El corazón del mapa. En lugar de usar Google Maps genérico, implementamos `ImageOverlay` para superponer los planos arquitectónicos reales de la ESIME sobre coordenadas geográficas, logrando una precisión que los mapas comerciales no tienen.

### Backend (Lógica y Datos)
- **Python + Flask**: Un servidor ligero pero potente. Gestiona las rutas API, la autenticación y la lógica de negocio.
- **SQLite + SQLAlchemy**: Base de datos relacional ligera. Almacena usuarios, edificios, salones y horarios complejos. Ideal para desarrollo y despliegue rápido.
- **Algoritmos de Grafos**: Implementación propia de estructuras de datos (Grafos y Árboles) para calcular las rutas más cortas entre salones (Edificio 1 a Edificio 4, etc.).

---

## 3. Evolución de la Construcción

El proyecto se construyó en **4 Fases Estratégicas**:

### Fase 1: Cimientos y Calibración
Lo primero fue "digitalizar" la escuela.
- Convertimos planos estáticos en capas interactivas.
- Calibramos coordenadas geográficas (`19.32...`, `-99.11...`) para que el "norte" del mapa coincidiera con la realidad.
- Creamos nodos de navegación (baños, escaleras, salones).

### Fase 2: Lógica de Negocio
Aquí es donde el sistema se volvió "inteligente".
- Implementamos el algoritmo de búsqueda de rutas (Waywalking).
- Conectamos el mapa con la base de datos: si buscas "Laboratorio de Computación", el sistema sabe que está en el Edificio 2, Piso 1.

### Fase 3: Identidad y Datos Reales
El cliente (tú) solicitó una experiencia personalizada.
- **Autenticación**: Creamos un login dual (Manual y Simulación Outlook).
- **Base de Datos Maestra**: Consolidamos la población de datos en un solo script (`setup_database.py`), eliminando la fragmentación.
- **Horarios Híbridos**: Programamos lógica específica para casos especiales, como el grupo **3CV14**, que toma materias de tronco común con 3CV1 pero se especializa con materias de 3CV3, resolviendo conflictos de horario automáticamente.

### Fase 4: Refinamiento Premium (UI/UX)
La fase final fue estética pura ("Hacerlo fino").
- Ajuste de paleta de colores: **Guinda Institucional (`#800000`)** y **Negro Elegante (`#000000`)**.
- Micro-interacciones: Botones que reaccionan al hover, sombras suaves y tipografía moderna.
- Limpieza de código: Eliminación de "código muerto" para entregar un producto profesional.

---

## 4. Estado Actual: Logros del Sprint

Al cierre de este Sprint, tenemos un sistema 100% funcional con las siguientes características validadas:

1.  **Navegación Exacta**: El mapa centra perfectamente la ESIME y permite paneo libre sin perderse.
2.  **Gestión de Usuarios**: 10 usuarios activos, incluyendo perfiles reales (Adrian y Omar) y sintéticos para pruebas.
3.  **Agenda Inteligente**: Los alumnos del grupo **3CV14** visualizan un horario combinado (Lenguajes + 3CV3) sin empalmes en días críticos (Martes/Jueves).
4.  **Estética Institucional**: La interfaz respeta los colores oficiales del IPN (Guinda y Blanco) con toques modernos (Negro mate).

---

## 5. Tecnologías Clave en Código
- **`setup_database.py`**: Script de orquestación maestra. Borra, limpia y reconstruye toda la infraestructura de datos en segundos.
- **`Dashboard.jsx`**: Componente reactivo que decide qué mostrar según la hora del día y la ubicación del usuario.
- **`MapComponent.jsx`**: Controlador lógico que gestiona capas, zoom y eventos táctiles en el mapa.

---

**Conclusión del Sprint**: El sistema está listo para ser presentado como una herramienta madura, estable y visualmente impactante, capaz de resolver problemas reales de logística estudiantil.
