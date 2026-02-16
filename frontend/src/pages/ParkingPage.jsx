import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import { useNavigate } from 'react-router-dom';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './ParkingPage.css';

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom icons for parking spaces
const createParkingIcon = (status) => {
    const colors = {
        available: '#10b981', // Verde
        reserved: '#f59e0b',  // Amarillo
        occupied: '#ef4444',  // Rojo
    };

    return L.divIcon({
        className: 'custom-parking-icon',
        html: `<div style="
      background-color: ${colors[status]};
      width: 24px;
      height: 24px;
      border-radius: 50%;
      border: 3px solid white;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    "></div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12],
    });
};

const ParkingPage = () => {
    const navigate = useNavigate();
    const [parkingSpaces, setParkingSpaces] = useState([]);
    const [stats, setStats] = useState({
        total: 0,
        available: 0,
        occupied: 0,
        reserved: 0,
    });
    const [selectedSection, setSelectedSection] = useState('all');
    const [selectedSpace, setSelectedSpace] = useState(null);
    const [loading, setLoading] = useState(true);
    const [viewMode, setViewMode] = useState('map'); // 'map' or 'list'

    const API_URL = 'http://localhost:5001';

    useEffect(() => {
        fetchParkingData();
        // Actualizar cada 10 segundos
        const interval = setInterval(fetchParkingData, 10000);
        return () => clearInterval(interval);
    }, [selectedSection]);

    const fetchParkingData = async () => {
        try {
            const params = selectedSection !== 'all' ? `?section=${selectedSection}` : '';
            const [spacesRes, statsRes] = await Promise.all([
                fetch(`${API_URL}/api/parking/spaces${params}`),
                fetch(`${API_URL}/api/parking/stats`),
            ]);

            const spacesData = await spacesRes.json();
            const statsData = await statsRes.json();

            setParkingSpaces(spacesData.spaces || []);
            setStats(statsData);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching parking data:', error);
            setLoading(false);
        }
    };

    const handleSpaceClick = (space) => {
        setSelectedSpace(space);
    };

    const getStatusColor = (status) => {
        const colors = {
            available: '#10b981',
            reserved: '#f59e0b',
            occupied: '#ef4444',
        };
        return colors[status] || '#9ca3af';
    };

    const getStatusText = (status) => {
        const texts = {
            available: 'Disponible',
            reserved: 'Reservado',
            occupied: 'Ocupado',
        };
        return texts[status] || status;
    };

    if (loading) {
        return (
            <div className="parking-loading">
                <div className="spinner"></div>
                <p>Cargando estacionamiento...</p>
            </div>
        );
    }

    return (
        <div className="parking-page">
            {/* Header */}
            <header className="parking-header">
                <button className="back-button" onClick={() => navigate('/map')}>
                    ← Volver
                </button>
                <div className="header-content">
                    <img src="/esime-logo.png" alt="ESIME Logo" className="header-logo" />
                    <h1>Estacionamiento Profesores</h1>
                </div>
            </header>

            {/* Stats Bar */}
            <div className="stats-bar">
                <div className="stat-card">
                    <div className="stat-icon" style={{ backgroundColor: '#10b981' }}>🟢</div>
                    <div className="stat-info">
                        <span className="stat-number">{stats.available}</span>
                        <span className="stat-label">Libres</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon" style={{ backgroundColor: '#f59e0b' }}>🟡</div>
                    <div className="stat-info">
                        <span className="stat-number">{stats.reserved}</span>
                        <span className="stat-label">Reservados</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon" style={{ backgroundColor: '#ef4444' }}>🔴</div>
                    <div className="stat-info">
                        <span className="stat-number">{stats.occupied}</span>
                        <span className="stat-label">Ocupados</span>
                    </div>
                </div>
                <div className="stat-card total">
                    <div className="stat-icon" style={{ backgroundColor: '#6366f1' }}>🅿️</div>
                    <div className="stat-info">
                        <span className="stat-number">{stats.total}</span>
                        <span className="stat-label">Total</span>
                    </div>
                </div>
            </div>

            {/* Filters */}
            <div className="filters-bar">
                <div className="section-filters">
                    <button
                        className={`filter-btn ${selectedSection === 'all' ? 'active' : ''}`}
                        onClick={() => setSelectedSection('all')}
                    >
                        Todas
                    </button>
                    <button
                        className={`filter-btn ${selectedSection === 'A' ? 'active' : ''}`}
                        onClick={() => setSelectedSection('A')}
                    >
                        Sección A
                    </button>
                    <button
                        className={`filter-btn ${selectedSection === 'B' ? 'active' : ''}`}
                        onClick={() => setSelectedSection('B')}
                    >
                        Sección B
                    </button>
                    <button
                        className={`filter-btn ${selectedSection === 'C' ? 'active' : ''}`}
                        onClick={() => setSelectedSection('C')}
                    >
                        Sección C
                    </button>
                </div>
                <div className="view-toggle">
                    <button
                        className={`toggle-btn ${viewMode === 'map' ? 'active' : ''}`}
                        onClick={() => setViewMode('map')}
                    >
                        🗺️ Mapa
                    </button>
                    <button
                        className={`toggle-btn ${viewMode === 'list' ? 'active' : ''}`}
                        onClick={() => setViewMode('list')}
                    >
                        📋 Lista
                    </button>
                </div>
            </div>

            {/* Main Content */}
            {viewMode === 'map' ? (
                <div className="map-container">
                    <MapContainer
                        center={[19.3298, -99.1117]}
                        zoom={17}
                        style={{ height: '100%', width: '100%' }}
                    >
                        <TileLayer
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                        />
                        {parkingSpaces.map((space) => (
                            <Marker
                                key={space.id}
                                position={[space.lat, space.lon]}
                                icon={createParkingIcon(space.status)}
                                eventHandlers={{
                                    click: () => handleSpaceClick(space),
                                }}
                            >
                                <Popup>
                                    <div className="space-popup">
                                        <h3>{space.space_number}</h3>
                                        <p className="status" style={{ color: getStatusColor(space.status) }}>
                                            {getStatusText(space.status)}
                                        </p>
                                        <div className="distances">
                                            <p>📍 Edificio 1: {space.distances.building_1}m</p>
                                            <p>📍 Edificio 2: {space.distances.building_2}m</p>
                                            <p>📍 Edificio 3: {space.distances.building_3}m</p>
                                        </div>
                                    </div>
                                </Popup>
                            </Marker>
                        ))}
                    </MapContainer>
                </div>
            ) : (
                <div className="list-container">
                    <div className="spaces-list">
                        {parkingSpaces.map((space) => (
                            <div
                                key={space.id}
                                className="space-card"
                                onClick={() => handleSpaceClick(space)}
                            >
                                <div className="space-header">
                                    <div
                                        className="status-indicator"
                                        style={{ backgroundColor: getStatusColor(space.status) }}
                                    ></div>
                                    <h3>{space.space_number}</h3>
                                    <span className="section-badge">Sección {space.section}</span>
                                </div>
                                <div className="space-details">
                                    <p className="status-text">{getStatusText(space.status)}</p>
                                    <div className="distances-grid">
                                        <span>Edificio 1: {space.distances.building_1}m</span>
                                        <span>Edificio 2: {space.distances.building_2}m</span>
                                        <span>Edificio 3: {space.distances.building_3}m</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Bottom Sheet for Selected Space */}
            {selectedSpace && (
                <div className="bottom-sheet">
                    <button className="close-btn" onClick={() => setSelectedSpace(null)}>
                        ✕
                    </button>
                    <div className="sheet-content">
                        <h2>{selectedSpace.space_number}</h2>
                        <p
                            className="status-badge"
                            style={{ backgroundColor: getStatusColor(selectedSpace.status) }}
                        >
                            {getStatusText(selectedSpace.status)}
                        </p>
                        <div className="space-info">
                            <div className="info-row">
                                <span className="label">Sección:</span>
                                <span className="value">{selectedSpace.section}</span>
                            </div>
                            <div className="info-row">
                                <span className="label">Fila:</span>
                                <span className="value">{selectedSpace.row}</span>
                            </div>
                            <div className="info-row">
                                <span className="label">Posición:</span>
                                <span className="value">{selectedSpace.position}</span>
                            </div>
                        </div>
                        <div className="distances-section">
                            <h3>Distancias a Edificios</h3>
                            <div className="distance-list">
                                <div className="distance-item">
                                    <span>📍 Edificio 1</span>
                                    <span>{selectedSpace.distances.building_1}m</span>
                                </div>
                                <div className="distance-item">
                                    <span>📍 Edificio 2</span>
                                    <span>{selectedSpace.distances.building_2}m</span>
                                </div>
                                <div className="distance-item">
                                    <span>📍 Edificio 3</span>
                                    <span>{selectedSpace.distances.building_3}m</span>
                                </div>
                            </div>
                        </div>
                        {selectedSpace.status === 'available' && (
                            <div className="action-buttons">
                                <button className="btn-primary">🧭 Navegar</button>
                                <button className="btn-secondary">⭐ Favorito</button>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default ParkingPage;
