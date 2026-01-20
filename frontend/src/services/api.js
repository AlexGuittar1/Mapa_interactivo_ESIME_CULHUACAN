const API_URL = "http://localhost:5001";

export const login = async (boleta) => {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ boleta })
    });
    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || 'Login failed');
    }
    return response.json();
};

export const getSchedule = async (boleta) => {
    const response = await fetch(`${API_URL}/api/user/${boleta}/schedule`);
    if (!response.ok) throw new Error('Failed to fetch schedule');
    return response.json();
};

export const getBuildings = async () => {
    const response = await fetch(`${API_URL}/api/buildings`);
    if (!response.ok) throw new Error('Failed to fetch buildings');
    return response.json();
};

export const getParking = async () => {
    const response = await fetch(`${API_URL}/api/parking`);
    if (!response.ok) throw new Error('Failed to fetch parking');
    return response.json();
};

export const getRoute = async (origin, dest) => {
    // Mock implementation for demo if real backend too complex to wire up fully now
    // Expects {lat: x, lon: y, boleta: z, type: 'next_class'} etc
    const response = await fetch(`${API_URL}/ruta`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(origin)
    });
    if (!response.ok) throw new Error('Failed to fetch route');
    return response.json();
};
