import React, { useState, useEffect } from 'react';
import { MapContainer, Marker, Popup, Polyline, ImageOverlay, useMap, TileLayer } from 'react-leaflet';
import { useNavigate } from 'react-router-dom';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { MAP_CONFIG } from '../mapConfig';
import initialLocations from '../locations.json';
import esimeLogo from '../assets/esime-1.png';

// Icons setup
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Maroon Pin Icon - Verified Link for Red Marker
const maroonIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
    className: 'custom-maroon-pin' // Applies filter for Maroon in index.css
});

const userLocationIcon = new L.DivIcon({
    className: 'custom-div-icon',
    html: "<div class='user-location-dot'></div>",
    iconSize: [14, 14],
    iconAnchor: [7, 7]
});

const LocationMarker = ({ onLocationUpdate }) => {
    const [position, setPosition] = useState(null);
    const map = useMap();

    useEffect(() => {
        map.locate({ watch: true, enableHighAccuracy: true });
        map.on('locationfound', (e) => {
            setPosition(e.latlng);
            onLocationUpdate(e.latlng);
        });
        return () => map.stopLocate();
    }, [map, onLocationUpdate]);

    return position === null ? null : (
        <Marker position={position} icon={userLocationIcon}>
            <Popup><span className="text-black font-bold">Tú</span></Popup>
        </Marker>
    );
};

const MapComponent = ({ buildings, parking, route, onNextClassClick, navInfo, onSelectPoint, selection }) => {
    const navigate = useNavigate();
    const [locations] = useState(initialLocations);
    const [userPos, setUserPos] = useState(null);

    const imageBounds = MAP_CONFIG.overlay.bounds;
    // Panning bounds expanded south (lower latitude) to allow centering south of campus
    const panningBounds = L.latLngBounds([
        [imageBounds[0][0] - 0.006, imageBounds[0][1] - 0.002],
        [imageBounds[1][0] + 0.002, imageBounds[1][1] + 0.002]
    ]);

    const renderMarker = (name, lat, lon, id) => (
        <Marker key={id} position={[lat, lon]} icon={maroonIcon}>
            <Popup>
                <div className="text-center p-1 flex flex-col gap-2 min-w-[140px]">
                    <h3 className="font-bold text-gray-800 border-b pb-1">{name}</h3>
                    <div className="flex flex-col gap-1 mt-1">
                        <button
                            onClick={() => onSelectPoint('origin', name)}
                            className={`text-[10px] py-1 px-2 rounded-lg border transition-all ${selection?.origin === name ? 'bg-green-600 text-white border-green-700' : 'bg-gray-50 text-gray-600 border-gray-200 hover:bg-gray-100'}`}
                        >
                            {selection?.origin === name ? '✓ Origen' : '📍 Marcar como Inicio'}
                        </button>
                        <button
                            onClick={() => onSelectPoint('destination', name)}
                            className={`text-[10px] py-1 px-2 rounded-lg border transition-all ${selection?.destination === name ? 'bg-red-600 text-white border-red-700' : 'bg-gray-50 text-gray-600 border-gray-200 hover:bg-gray-100'}`}
                        >
                            {selection?.destination === name ? '✓ Destino' : '🏁 Marcar como Destino'}
                        </button>
                    </div>
                </div>
            </Popup>
        </Marker>
    );

    return (
        <div className="relative h-screen w-full flex flex-col map-bg-premium">
            {/* Header Guinda - Restored to h-16 */}
            <header className="header-gradient h-16 w-full flex justify-between items-center px-6 shadow-lg z-[1001] shrink-0">
                <div className="flex items-center gap-3">
                    <img src={esimeLogo} alt="ESIME Logo" className="h-12 w-auto object-contain drop-shadow-md" />
                    <h1 className="text-white font-black text-sm tracking-widest uppercase">MAPA ESIME</h1>
                </div>
                <div className="flex gap-4">
                    <button
                        onClick={() => navigate('/dashboard')}
                        className="text-white/90 hover:text-white font-bold text-xs uppercase tracking-wider transition-colors"
                    >
                        Mi Perfil
                    </button>
                    <button
                        onClick={() => {
                            localStorage.removeItem('user');
                            navigate('/');
                        }}
                        className="bg-white/10 px-4 py-1.5 rounded-full text-white font-bold text-xs uppercase hover:bg-white/20 transition-all"
                    >
                        Salir
                    </button>
                </div>
            </header>

            {/* Map Container */}
            <div className="flex-1 relative z-0 bg-transparent">
                <MapContainer
                    center={MAP_CONFIG.center}
                    zoom={MAP_CONFIG.zoom}
                    maxZoom={MAP_CONFIG.maxZoom}
                    minZoom={16}
                    maxBounds={panningBounds}
                    maxBoundsViscosity={1.0}
                    attributionControl={false}
                    scrollWheelZoom={true}
                    className="h-full w-full bg-transparent"
                >
                    {/* OpenStreetMap Layer (Descomentar para ver el mapa base real) */}
                    {/* 
                    <TileLayer
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    /> 
                    */}

                    {MAP_CONFIG.overlay.enabled && (
                        <div style={{ transform: `rotate(${MAP_CONFIG.overlay.rotation || 0}deg)`, transformOrigin: 'center' }}>
                            <ImageOverlay url={MAP_CONFIG.overlay.imageUrl} bounds={MAP_CONFIG.overlay.bounds} opacity={MAP_CONFIG.overlay.opacity ?? 1.0} />
                        </div>
                    )}

                    <LocationMarker onLocationUpdate={setUserPos} />

                    {buildings.map((b) => renderMarker(b.nombre, b.lat, b.lon, `b-${b.id}`))}
                    {locations.map((loc, idx) => renderMarker(loc.name, loc.lat, loc.lon, `loc-${idx}`))}

                    {route && route.length > 0 && (
                        <Polyline positions={route} color="#ffde00" weight={6} opacity={0.8} dashArray="10, 10" />
                    )}
                </MapContainer>

                {/* Floating Navigation UI - Slightly higher up to avoid zoom edge cutoffs */}
                <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-[1000] w-full max-w-sm px-6">
                    <div className="glass-panel p-5 rounded-[2rem] flex flex-col gap-3 shadow-2xl border-white/50">
                        {(!selection?.origin && !selection?.destination) ? (
                            <p className="text-[9px] text-gray-500 font-black uppercase tracking-[0.2em] text-center mb-0.5">
                                Selecciona puntos para navegar
                            </p>
                        ) : (
                            <div className="flex flex-col gap-1.5 px-1 py-1 bg-white/30 rounded-2xl border border-white/50 mb-1">
                                <div className="flex items-center gap-2 overflow-hidden px-2">
                                    <div className="w-1.5 h-1.5 rounded-full bg-green-500 shrink-0"></div>
                                    <span className="text-[9px] font-bold text-gray-600 uppercase tracking-tighter truncate">
                                        Inicio: {selection.origin || 'Tu ubicación'}
                                    </span>
                                </div>
                                <div className="flex items-center gap-2 overflow-hidden px-2">
                                    <div className="w-1.5 h-1.5 rounded-full bg-red-500 shrink-0"></div>
                                    <span className="text-[9px] font-bold text-gray-600 uppercase tracking-tighter truncate">
                                        Destino: {selection.destination || 'Por definir'}
                                    </span>
                                </div>
                            </div>
                        )}

                        {navInfo && <div className="bg-yellow-100/80 backdrop-blur-sm text-yellow-900 px-4 py-2 rounded-xl text-[9px] font-black text-center uppercase tracking-widest border border-yellow-200">{navInfo}</div>}

                        <button
                            onClick={() => onNextClassClick(userPos)}
                            className="bg-red-800 hover:bg-red-900 text-white py-4 rounded-2xl font-black text-[10px] uppercase tracking-[0.15em] transition-all shadow-xl active:scale-95"
                        >
                            Ir a mi clase próxima
                        </button>

                        <div className="grid grid-cols-2 gap-3">
                            <button className="bg-white/60 hover:bg-white/80 text-gray-600 py-3 rounded-xl text-[8px] font-black uppercase tracking-widest border border-white transition-colors">Estacionamiento</button>
                            <button className="bg-white/60 hover:bg-white/80 text-gray-600 py-3 rounded-xl text-[8px] font-black uppercase tracking-widest border border-white transition-colors">Horario</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MapComponent;
