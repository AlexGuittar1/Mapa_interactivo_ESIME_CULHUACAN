const API_URL = "http://localhost:5001";

/**
 * Función auxiliar para realizar peticiones fetch y manejar errores.
 * @param {string} endpoint - El punto final de la API.
 * @param {object} options - Opciones de la petición fetch.
 * @param {string} errorMessage - Mensaje de error por defecto.
 */
const apiRequest = async (endpoint, options = {}, errorMessage = 'Error en la petición') => {
    const response = await fetch(`${API_URL}${endpoint}`, {
        headers: { 'Content-Type': 'application/json' },
        ...options,
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || errorMessage);
    }

    return response.json();
};

// Iniciar sesión con el número de boleta
export const login = (boleta) =>
    apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ boleta })
    }, 'Error al iniciar sesión');

// Obtener el horario del usuario mediante su boleta
export const getSchedule = (boleta) =>
    apiRequest(`/api/user/${boleta}/schedule`, {}, 'Error al obtener el horario');

// Verificar si un correo electrónico ya está registrado
export const checkEmail = (email) =>
    apiRequest('/auth/check-email', {
        method: 'POST',
        body: JSON.stringify({ email })
    });

// Completar el registro del perfil del usuario
export const completeProfile = (userData) =>
    apiRequest('/auth/complete-profile', {
        method: 'POST',
        body: JSON.stringify(userData)
    }, 'Error al completar el perfil');

// Registrar nuevo usuario manualmente
export const register = (userData) =>
    apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData)
    }, 'Error al registrar usuario');

// Obtener el listado de edificios
export const getBuildings = () =>
    apiRequest('/api/buildings', {}, 'Error al obtener edificios');

// Obtener información de los estacionamientos
export const getParking = () =>
    apiRequest('/api/parking', {}, 'Error al obtener estacionamientos');

// Obtener una ruta basada en el origen y destino
export const getRoute = (origin, dest) =>
    apiRequest('/ruta', {
        method: 'POST',
        body: JSON.stringify(origin)
    }, 'Error al obtener la ruta');

// Guardar ubicaciones personalizadas
export const saveLocations = (locations) =>
    apiRequest('/api/locations', {
        method: 'POST',
        body: JSON.stringify(locations)
    }, 'Error al guardar ubicaciones');

// Guardar configuración del mapa (bounds, rotation, etc)
export const saveMapConfig = (config) =>
    apiRequest('/api/map-config', {
        method: 'POST',
        body: JSON.stringify(config)
    }, 'Error al guardar configuración del mapa');

// Actualizar datos del usuario (ej. vehículo)
export const updateUser = (boleta, userData) =>
    apiRequest(`/api/user/${boleta}`, {
        method: 'PUT',
        body: JSON.stringify(userData)
    }, 'Error al actualizar usuario');