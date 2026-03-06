/**
 * API Service — Capa de comunicación con el backend.
 * 
 * Centraliza todas las llamadas HTTP al backend Flask.
 * Compatible con modo local (boleta) y futuro modo Azure AD.
 */

const API_BASE = "http://localhost:5001";

// --- Helpers ---

async function handleResponse(res) {
    const data = await res.json();
    if (!res.ok) {
        throw new Error(data.error || `HTTP ${res.status}`);
    }
    return data;
}

function headers(extra = {}) {
    return {
        "Content-Type": "application/json",
        ...extra,
    };
}

// --- Auth ---

export async function login(boleta) {
    const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({ boleta }),
    });
    return handleResponse(res);
}

export async function checkEmail(email) {
    const res = await fetch(`${API_BASE}/auth/check-email`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({ email }),
    });
    return handleResponse(res);
}

export async function completeProfile(data) {
    const res = await fetch(`${API_BASE}/auth/complete-profile`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify(data),
    });
    return handleResponse(res);
}

export async function register(data) {
    const res = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify(data),
    });
    return handleResponse(res);
}

// --- User ---

export async function updateUser(boleta, data) {
    const res = await fetch(`${API_BASE}/api/user/${boleta}`, {
        method: "PUT",
        headers: headers(),
        body: JSON.stringify(data),
    });
    return handleResponse(res);
}

export async function getSchedule(boleta) {
    const res = await fetch(`${API_BASE}/api/user/${boleta}/schedule`);
    return handleResponse(res);
}

// --- Map Data ---

export async function getBuildings() {
    const res = await fetch(`${API_BASE}/api/buildings`);
    return handleResponse(res);
}

export async function getParking() {
    const res = await fetch(`${API_BASE}/api/parking`);
    return handleResponse(res);
}

export async function getRoute(data) {
    const res = await fetch(`${API_BASE}/api/ruta`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify(data),
    });
    return handleResponse(res);
}

export async function getWalkingRoute(data) {
    const res = await fetch(`${API_BASE}/api/route`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify(data),
    });
    return handleResponse(res);
}

// --- Saved Places ---

export async function getSavedPlaces(boleta) {
    const res = await fetch(`${API_BASE}/api/saved-places?user_boleta=${boleta}`);
    return handleResponse(res);
}

export async function savePlace(data) {
    const res = await fetch(`${API_BASE}/api/saved-places`, {
        method: "POST",
        headers: headers(),
        body: JSON.stringify(data),
    });
    return handleResponse(res);
}

export async function deletePlace(id) {
    const res = await fetch(`${API_BASE}/api/saved-places/${id}`, {
        method: "DELETE",
    });
    return handleResponse(res);
}

export async function updatePlace(id, data) {
    const res = await fetch(`${API_BASE}/api/saved-places/${id}`, {
        method: "PUT",
        headers: headers(),
        body: JSON.stringify(data),
    });
    return handleResponse(res);
}
