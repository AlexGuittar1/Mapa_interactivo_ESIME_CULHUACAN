// Configuración del Mapa
// Aquí puedes personalizar el centro, el zoom y la imagen superpuesta (overlay)

export const MAP_CONFIG = {
    // Coordenadas iniciales del mapa [Latitud, Longitud]
    // Ajusta esto al centro real de tu escuela
    center: [19.311311, -99.111867],

    // Nivel de zoom inicial (13 = ciudad, 18 = calle, 21 = edificio)
    zoom: 18,

    // Configuración para poner una imagen personalizada del mapa (Plano de la escuela)
    // Si tienes una imagen (ej. 'mapa_esime.png') ponla en la carpeta 'frontend/public/'
    overlay: {
        enabled: false, // Cambia a true para activar
        imageUrl: '/mapa_esime.png', // Nombre del archivo en public/
        // Límites de la imagen: [[LatSur, LonOeste], [LatNorte, LonEste]]
        // Debes ajustar esto para que la imagen cuadre con el mapa real
        bounds: [
            [19.310000, -99.113000], // Esquina inferior izquierda
            [19.312500, -99.110500]  // Esquina superior derecha
        ]
    }
};
