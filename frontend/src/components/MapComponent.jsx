import React, { useState, useEffect } from 'react';
import { MapContainer, Marker, Popup, Polyline, ImageOverlay, useMap, TileLayer, useMapEvents } from 'react-leaflet';
import { useNavigate } from 'react-router-dom';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { MAP_CONFIG } from '../mapConfig';
import initialLocations from '../locations.json';
import esimeLogo from '../assets/esime-1.png';
import { Search, User, Compass, Navigation as NavIcon, Car, Bookmark, Map as MapIcon, Plus, ArrowLeft, ArrowUpDown, MoreHorizontal, Send, Clock, X } from 'lucide-react';
import SavedPlacesSheet from './SavedPlacesSheet';

// Icons setup
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Icons
const maroonIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
    className: 'custom-maroon-pin'
});

const blueIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
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

// Map Events to handle clicks for Custom Pins
const MapClickHandler = ({ activeTab, onMapClick }) => {
    useMapEvents({
        click: (e) => {
            if (activeTab === 'agregar') {
                onMapClick(e.latlng);
            }
        },
    });
    return null;
};

const MapController = ({ targetLocation }) => {
    const map = useMap();
    useEffect(() => {
        if (targetLocation) {
            map.flyTo(targetLocation, 18, {
                animate: true,
                duration: 1.5
            });
        }
    }, [targetLocation]);
    return null;
};


const MapComponent = ({ buildings, parking, route, onNextClassClick, navInfo, onSelectPoint, onCalculateRoute, selection, showPins, togglePins }) => {
    const navigate = useNavigate();
    const [locations] = useState(initialLocations);
    const [userPos, setUserPos] = useState(null);
    const [activeTab, setActiveTab] = useState('explorar');

    // Navigation Mode State
    const [isNavigating, setIsNavigating] = useState(false);
    const [navOrigin, setNavOrigin] = useState("Tu ubicación"); // Default
    const [navDestination, setNavDestination] = useState("");
    const [routeInfo, setRouteInfo] = useState(null); // { time: '1 min', dist: '100 m', name: ... }

    // Custom Pin Adding State
    const [pendingPin, setPendingPin] = useState(null); // { lat, lon }
    const [pinName, setPinName] = useState("");
    const [customPins, setCustomPins] = useState([]); // List of custom pins added in session or fetched

    // Search & Control State
    const [searchQuery, setSearchQuery] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [targetLocation, setTargetLocation] = useState(null);

    // State for selective visibility
    const [visiblePinIds, setVisiblePinIds] = useState([]);


    // Refs for markers to programmatically open popups
    const markerRefs = React.useRef({});

    // Filter Logic
    const handleFilterClick = (type) => {
        let searchTerm = type.toLowerCase();

        // Fix typos/mapping
        if (type === 'Gimnasio') searchTerm = 'gimnacio'; // Matches exact name in JSON
        if (type === 'Cafeteria') searchTerm = 'cafe';

        if (type === 'Salones') {
            // Explicitly find Edificio 1, 2, 3
            const matches = buildings.filter(b =>
                b.nombre === 'Edificio 1' ||
                b.nombre === 'Edificio 2' ||
                b.nombre === 'Edificio 3'
            );

            if (matches.length > 0) {
                const matchIds = matches.map(m => `b-${m.id}`);
                // Show these pins ONLY (or add them? User said "without activating buttons", implying selective)
                setVisiblePinIds(matchIds);

                const lats = matches.map(m => m.lat);
                const lons = matches.map(m => m.lon);
                const minLat = Math.min(...lats);
                const maxLat = Math.max(...lats);
                const minLon = Math.min(...lons);
                const maxLon = Math.max(...lons);

                // Toggle pins OFF globally if we rely on selective visibility, but we can just use the state
                // if (!showPins) togglePins(); // Don't turn on all pins per user request

                setTargetLocation([(minLat + maxLat) / 2, (minLon + maxLon) / 2]);
            }
            return;
        }

        let match = buildings.find(b => b.nombre.toLowerCase().includes(searchTerm)) ||
            locations.find(l => l.name.toLowerCase().includes(searchTerm));

        if (match) {
            const lat = match.lat || match.latitud;
            const lon = match.lon || match.longitud;
            const id = match.id ? (match.type === 'static' ? `loc-${match.id}` : `b-${match.id}`) : `loc-${locations.indexOf(match)}`;

            setVisiblePinIds([id]);
            setTargetLocation([lat, lon]);

            setTimeout(() => {
                const mk = markerRefs.current[id];
                if (mk) mk.openPopup();
            }, 500);

        } else {
            console.log("No match found for", searchTerm);
            if (type === 'Cafeteria') setTargetLocation([19.4326, -99.1332]);
        }
    };

    const handleSearch = (query) => {
        setSearchQuery(query);
        if (query.length > 0) {
            const term = query.toLowerCase();
            const results = [
                ...buildings.map(b => ({ ...b, name: b.nombre, type: 'building', id: `b-${b.id}` })),
                ...locations.map((l, idx) => ({ ...l, type: 'static', id: `loc-${idx}` })),
                ...customPins.map(p => ({ ...p, type: 'custom', id: `cust-${p.id}` }))
            ].filter(item => item.name.toLowerCase().includes(term));
            setSearchResults(results.slice(0, 5));
            setShowSuggestions(true);
        } else {
            setShowSuggestions(false);
        }
    };

    const handleSelectResult = (item) => {
        const lat = item.lat || item.latitud;
        const lon = item.lon || item.longitud;
        const id = item.id;

        setVisiblePinIds([id]); // Show only this one

        setTargetLocation([lat, lon]);
        setSearchQuery(item.name);
        setShowSuggestions(false);
        onSelectPoint('destination', item.name);

        setTimeout(() => {
            const mk = markerRefs.current[id];
            if (mk) mk.openPopup();
        }, 500);
    };

    // Map Bounds
    const imageBounds = MAP_CONFIG.overlay.bounds;
    const panningBounds = L.latLngBounds([
        [imageBounds[0][0] - 0.006, imageBounds[0][1] - 0.002],
        [imageBounds[1][0] + 0.002, imageBounds[1][1] + 0.002]
    ]);

    useEffect(() => {
        // Fetch saved custom pins on load custom pins
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            const user = JSON.parse(storedUser);
            fetch(`http://127.0.0.1:5001/api/saved-places?user_boleta=${user.boleta}`)
                .then(res => res.json())
                .then(data => {
                    if (Array.isArray(data)) {
                        const custom = data.filter(p => p.type === 'custom');
                        setCustomPins(custom);
                    }
                })
                .catch(err => console.error(err));
        }
    }, [activeTab]);

    const handleMapClick = (latlng) => {
        setPendingPin(latlng);
    };

    const handleSavePin = async () => {
        if (!pinName.trim()) {
            alert("Por favor ingresa un nombre.");
            return;
        }
        if (!pendingPin) return;

        const storedUser = localStorage.getItem('user');
        if (!storedUser) {
            alert("Error: Inicia sesión nuevamente.");
            return;
        }

        let user;
        try {
            user = JSON.parse(storedUser);
            if (!user || !user.boleta) {
                alert("Error: Datos de usuario incompletos.");
                return;
            }
        } catch (e) {
            console.error(e);
            alert("Error al leer usuario.");
            return;
        }

        try {
            const res = await fetch(`http://127.0.0.1:5001/api/saved-places`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_boleta: user.boleta,
                    name: pinName,
                    lat: pendingPin.lat,
                    lon: pendingPin.lng,
                    type: 'custom'
                })
            });
            if (res.ok) {
                const newPin = await res.json();
                setCustomPins([...customPins, newPin]);
                setPendingPin(null);
                setPinName("");
                alert("Guardado!");
            } else {
                const err = await res.json();
                alert("Error al guardar: " + (err.error || "Desconocido"));
            }
        } catch (e) {
            console.error("Error saving pin", e);
            alert("Error de conexión: " + e.message);
        }
    };



    const startNavigation = () => {
        setIsNavigating(true);
        // If we want route calculation on start, we trigger it here if destination is known
        onSelectPoint('destination', selection.destination);
    };

    const handleStartRoute = () => {
        if (onCalculateRoute && navDestination) {
            onCalculateRoute(navOrigin, navDestination, userPos);
        }
    };

    const exitNavigation = () => {
        setIsNavigating(false);
        setNavDestination("");
        onSelectPoint('clear'); // Clear route
    };

    const handleDeletePin = async (id, name) => {
        if (confirm(`¿Eliminar "${name}"?`)) {
            try {
                await fetch(`http://127.0.0.1:5001/api/saved-places/${id}`, { method: 'DELETE' });
                setCustomPins(prev => prev.filter(p => p.id !== id));
            } catch (e) {
                console.error("Error deleting pin", e);
            }
        }
    };

    const handleCompassClick = () => {
        // Logic: Check distance.
        if (!userPos) {
            alert("Ubicación no disponible");
            return;
        }

        // Approximate school center (ESIME)
        const schoolCenter = L.latLng(19.33059, -99.11211);
        const dist = schoolCenter.distanceTo(userPos);

        if (dist > 3000) { // 3km threshold
            alert("Estás muy lejos de la escuela. Acércate para usar esta función.");
        } else {
            setTargetLocation([userPos.lat, userPos.lng]);
        }
    };

    const handlePinSelectForNav = (name) => {
        setNavDestination(name);
        setIsNavigating(true);
        // Trigger route calculation
        onSelectPoint('destination', name);
        onSelectPoint('origin', 'Tu ubicación'); // Implicit
    };

    const renderMarker = (name, lat, lon, id, isCustom = false) => {
        // Show pins logic: 
        // 1. If Global "showPins" is true -> show all
        // 2. If activeTab is 'agregar' -> show all (so user knows where to click)
        // 3. If isNavigating -> show all ? Or just relevant? usually all for context
        // 4. If activeTab is 'guardados' -> show all custom
        // 5. IF NOT ANY OF ABOVE, check visiblePinIds.

        const isVisibleById = visiblePinIds.includes(id);

        const shouldShow = showPins ||
            activeTab === 'agregar' ||
            isNavigating ||
            activeTab === 'guardados' ||
            isVisibleById;

        if (!shouldShow) return null;

        return (
            <Marker
                key={id}
                position={[lat, lon]}
                icon={isCustom ? blueIcon : maroonIcon}
                ref={(el) => markerRefs.current[id] = el}
            >
                <Popup>
                    <div className="text-center p-1 flex flex-col gap-2 min-w-[140px]">
                        <h3 className="font-bold text-gray-800 border-b pb-1">{name}</h3>
                        {!isNavigating ? (
                            <button
                                onClick={() => handlePinSelectForNav(name)}
                                className="bg-blue-600 text-white text-xs py-1.5 px-3 rounded-lg font-bold shadow-md hover:bg-blue-700"
                            >
                                Ir aquí
                            </button>
                        ) : (
                            <span className="text-xs text-green-600 font-bold">Destino seleccionado</span>
                        )}

                        {isCustom && !isNavigating && (
                            <div className="flex flex-col gap-1 mt-2 pt-2 border-t">
                                <button
                                    onClick={() => {
                                        setNavOrigin(name);
                                        setIsNavigating(true);
                                    }}
                                    className="bg-gray-100 text-gray-700 text-[10px] py-1 px-2 rounded hover:bg-gray-200"
                                >
                                    Como Inicio
                                </button>
                                <button
                                    onClick={() => {
                                        setNavDestination(name);
                                        setIsNavigating(true);
                                        onSelectPoint('destination', name);
                                    }}
                                    className="bg-gray-100 text-gray-700 text-[10px] py-1 px-2 rounded hover:bg-gray-200"
                                >
                                    Como Destino
                                </button>
                                <button
                                    onClick={() => handleDeletePin(id.replace('cust-', ''), name)}
                                    className="bg-red-100 text-red-600 text-[10px] py-1 px-2 rounded hover:bg-red-200"
                                >
                                    Eliminar
                                </button>
                            </div>
                        )}
                    </div>
                </Popup>
            </Marker>
        );
    };

    return (
        <div className="relative h-screen w-full flex flex-col bg-white overflow-hidden font-sans">

            {/* --- NAVIGATION MODE UI (Red Header) --- */}
            {isNavigating && (
                <div className="absolute top-0 left-0 w-full z-[1200] bg-[#b91c1c] rounded-b-[30px] shadow-2xl p-4 pt-12 animate-in slide-in-from-top duration-300">
                    <div className="flex items-center gap-3 mb-4">
                        <button onClick={exitNavigation} className="text-white p-1 hover:bg-white/10 rounded-full">
                            <ArrowLeft size={24} />
                        </button>
                        <div className="flex-1 flex flex-col gap-2">
                            {/* Origin Input */}
                            <div className="bg-black/20 rounded-lg flex items-center px-3 py-2 border border-white/10">
                                <div className="w-4 h-4 rounded-full border-2 border-white/60 mr-3"></div>
                                <input
                                    type="text"
                                    value={navOrigin}
                                    readOnly // For now default to User Location
                                    className="bg-transparent text-white text-sm font-semibold w-full outline-none placeholder:text-white/50"
                                />
                            </div>
                            {/* Destination Input */}
                            <div className="bg-black/20 rounded-lg flex items-center px-3 py-2 border border-white/10">
                                <div className="w-4 h-4 rounded-full border-2 border-white/60 mr-3 bg-red-500 border-red-200"></div>
                                <input
                                    type="text"
                                    value={navDestination || selection?.destination || ""}
                                    placeholder="Seleccionar destino..."
                                    readOnly
                                    className="bg-transparent text-white text-sm font-semibold w-full outline-none placeholder:text-white/50"
                                />
                            </div>
                        </div>
                        <div className="flex flex-col gap-3 text-white">
                            <MoreHorizontal size={24} />
                            <ArrowUpDown size={20} />
                        </div>
                    </div>
                </div>
            )}

            {/* --- NORMAL TOP UI --- */}
            {!isNavigating && activeTab !== 'guardados' && (
                <div className="absolute top-0 left-0 w-full z-[1001] px-4 pt-12 pb-4 flex flex-col gap-3 pointer-events-none">
                    <div className="bg-white rounded-full shadow-lg flex items-center px-4 py-3 gap-3 pointer-events-auto">
                        <img src={esimeLogo} alt="Logo" className="h-8 w-8 object-contain" />
                        <div className="flex-1 flex items-center relative">
                            <input
                                type="text"
                                value={searchQuery}
                                onChange={(e) => handleSearch(e.target.value)}
                                placeholder="Buscar aquí..."
                                className="w-full text-base outline-none text-gray-700 placeholder:text-gray-400 font-medium"
                            />
                            {showSuggestions && searchResults.length > 0 && (
                                <div className="absolute top-full left-0 w-full bg-white rounded-lg shadow-xl mt-2 overflow-hidden z-[1300]">
                                    {searchResults.map((result, idx) => (
                                        <button
                                            key={idx}
                                            onClick={() => handleSelectResult(result)}
                                            className="w-full text-left px-4 py-3 hover:bg-gray-50 border-b last:border-0 border-gray-100 flex items-center gap-2"
                                        >
                                            <div className="bg-gray-100 p-1 rounded-full text-gray-500">
                                                {result.type === 'custom' ? <Bookmark size={14} /> : <MapIcon size={14} />}
                                            </div>
                                            <span className="text-sm font-medium text-gray-800">{result.name}</span>
                                        </button>
                                    ))}
                                </div>
                            )}
                        </div>
                        <button onClick={() => navigate('/dashboard')} className="p-1 rounded-full hover:bg-gray-100 transition-colors">
                            <User className="h-6 w-6 text-black border-2 border-black rounded-full p-0.5" />
                        </button>
                    </div>
                    {/* Filter Chips */}
                    <div className="flex gap-2 overflow-x-auto no-scrollbar pointer-events-auto pb-1">
                        {['Cafeteria', 'Gimnasio', 'Salones', 'Biblioteca'].map((chip, idx) => (
                            <button
                                key={idx}
                                onClick={() => handleFilterClick(chip)}
                                className="bg-white whitespace-nowrap px-4 py-2 rounded-full shadow-md text-xs font-bold text-gray-800 flex items-center gap-1.5 active:scale-95 transition-transform"
                            >
                                <span className="text-gray-900 text-sm">
                                    {chip === 'Cafeteria' && '🍴'} {chip === 'Gimnasio' && '🏋️'} {chip === 'Salones' && '🏫'} {chip === 'Biblioteca' && '📚'}
                                </span>
                                {chip}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* --- MAP LAYER --- */}
            <div className="flex-1 relative z-0">
                <MapContainer
                    center={MAP_CONFIG.center}
                    zoom={MAP_CONFIG.zoom}
                    maxZoom={MAP_CONFIG.maxZoom}
                    minZoom={16}
                    maxBounds={panningBounds}
                    maxBoundsViscosity={1.0}
                    attributionControl={false}
                    zoomControl={false}
                    className="h-full w-full bg-white"
                >
                    <TileLayer attribution='&copy; OpenStreetMap' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
                    {MAP_CONFIG.overlay.enabled && (
                        <div style={{ transform: `rotate(${MAP_CONFIG.overlay.rotation || 0}deg)`, transformOrigin: 'center' }}>
                            <ImageOverlay url={MAP_CONFIG.overlay.imageUrl} bounds={MAP_CONFIG.overlay.bounds} opacity={MAP_CONFIG.overlay.opacity ?? 1.0} />
                        </div>
                    )}
                    <LocationMarker onLocationUpdate={setUserPos} />
                    <MapController targetLocation={targetLocation} />
                    <MapClickHandler activeTab={activeTab} onMapClick={handleMapClick} />

                    {/* Markers */}
                    {buildings.map((b) => renderMarker(b.nombre, b.lat, b.lon, `b-${b.id}`))}
                    {locations.map((loc, idx) => renderMarker(loc.name, loc.lat, loc.lon, `loc-${idx}`))}
                    {customPins.map((pin) => renderMarker(pin.name, pin.lat, pin.lon, `cust-${pin.id}`, true))}

                    {route && route.length > 0 && (
                        <Polyline positions={route} color="#3b82f6" weight={7} opacity={0.9} />
                    )}

                    {/* Pending Custom Pin Marker (Just the marker, no popup form) */}
                    {pendingPin && (
                        <Marker position={pendingPin} icon={blueIcon} />
                    )}
                </MapContainer>
            </div>

            {/* --- ADD PIN FORM OVERLAY (Compact) --- */}
            {pendingPin && (
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-4 rounded-xl shadow-2xl z-[1500] w-64 animate-in fade-in zoom-in duration-200">
                    <h3 className="font-bold text-gray-800 text-sm mb-3 text-center">Nuevo Lugar</h3>
                    <div className="flex flex-col gap-3">
                        <input
                            type="text"
                            className="w-full border-2 border-gray-200 rounded-lg p-2 text-sm outline-none focus:border-blue-500 transition-colors"
                            placeholder="Nombre..."
                            value={pinName}
                            onChange={(e) => setPinName(e.target.value)}
                            autoFocus
                        />
                        <div className="flex gap-2">
                            <button
                                onClick={() => {
                                    setPendingPin(null);
                                    setPinName("");
                                }}
                                className="flex-1 bg-gray-100 text-gray-700 text-xs font-bold py-2 rounded-lg hover:bg-gray-200 transition-colors"
                            >
                                Cancelar
                            </button>
                            <button
                                onClick={handleSavePin}
                                className="flex-1 bg-[#b91c1c] text-white text-xs font-bold py-2 rounded-lg shadow-md hover:bg-red-700 transition-colors"
                            >
                                Guardar
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* --- ADD PIN INSTRUCTION --- */}
            {activeTab === 'agregar' && !pendingPin && (
                <div className="absolute top-32 left-1/2 transform -translate-x-1/2 bg-black/70 text-white px-4 py-2 rounded-full z-[1100] text-sm font-bold shadow-lg animate-bounce pointer-events-none">
                    📍 Toca el mapa para agregar un pin
                </div>
            )}

            {/* --- NAV BOTTOM SHEET (Route Info) --- */}
            {isNavigating && selection?.destination && (route || true) && (
                <div className="absolute bottom-6 left-4 right-4 bg-[#b91c1c] text-white rounded-[2rem] p-6 shadow-2xl z-[1200]">
                    <div className="flex items-center justify-between mb-4">
                        <div>
                            <h2 className="text-2xl font-black">
                                {route ? `${navInfo?.distancia || 0} m` : 'Calculando...'}
                            </h2>
                            <p className="text-sm font-medium opacity-80">
                                {navDestination || "Destino seleccionado"}
                            </p>
                        </div>
                        <div className="bg-white/20 p-2 rounded-full">
                            <Send size={24} />
                        </div>
                    </div>
                    <button
                        onClick={handleStartRoute}
                        className="w-full bg-white text-[#b91c1c] font-black py-4 rounded-xl text-lg shadow-lg flex items-center justify-center gap-2 hover:bg-gray-100 transition-colors">
                        <NavIcon fill="currentColor" size={20} />
                        Iniciar
                    </button>
                </div>
            )}


            {/* --- FLOATING CONTROLS --- */}
            {!isNavigating && (
                <div className="absolute bottom-28 right-4 z-[1000] flex flex-col items-end gap-3">
                    <button
                        onClick={handleCompassClick}
                        className="bg-white p-3 rounded-full shadow-xl hover:bg-gray-50 active:scale-95 transition-all"
                    >
                        <Compass className="h-6 w-6 text-gray-700" />
                    </button>
                    <button
                        onClick={startNavigation}
                        className="bg-[#002f5b] p-4 rounded-full shadow-xl hover:bg-[#002244] active:scale-95 transition-all border-2 border-white/20"
                    >
                        <div className="bg-[#1a446e] p-1 rounded-full">
                            <NavIcon className="h-6 w-6 text-white fill-white transform rotate-45" />
                        </div>
                    </button>
                </div>
            )}

            {/* --- SAVED PLACES SHEET --- */}
            {activeTab === 'guardados' && (
                <>
                    <div className="fixed inset-0 bg-black/50 z-[1050]" onClick={() => setActiveTab('explorar')} />
                    <div className="fixed inset-x-0 bottom-0 z-[1100]">
                        <SavedPlacesSheet onClose={() => setActiveTab('explorar')} />
                    </div>
                </>
            )}

            {/* --- BOTTOM NAVIGATION BAR --- */}
            {!isNavigating && (
                <div className="absolute bottom-4 left-4 right-4 z-[1001]">
                    <div className="bg-[#b30000] rounded-[2.5rem] px-6 py-4 flex justify-between items-center shadow-2xl relative">
                        {/* Nav Items... Same as before */}
                        <button
                            onClick={() => setActiveTab('estacionamiento')}
                            className={`flex flex-col items-center gap-1 group transition-colors ${activeTab === 'estacionamiento' ? 'opacity-100' : 'opacity-70'}`}
                        >
                            <Car className="h-6 w-6 text-white group-hover:text-white transition-colors" />
                            <span className="text-[10px] text-white font-medium">Estacionamiento</span>
                        </button>

                        <button
                            onClick={() => setActiveTab('guardados')}
                            className={`flex flex-col items-center gap-1 group transition-colors ${activeTab === 'guardados' ? 'opacity-100' : 'opacity-70'}`}
                        >
                            <Bookmark className="h-6 w-6 text-white group-hover:text-white transition-colors animate-pulse-once" fill={activeTab === 'guardados' ? 'currentColor' : 'none'} />
                            <span className="text-[10px] text-white font-medium">Guardados</span>
                        </button>

                        <button
                            onClick={() => {
                                setActiveTab('explorar');
                                togglePins();
                            }}
                            className="flex flex-col items-center gap-1 group"
                        >
                            <div className={`transition-all ${activeTab === 'explorar' && showPins ? 'bg-white/20' : ''} p-1 rounded-full`}>
                                <MapIcon className={`h-6 w-6 ${activeTab === 'explorar' && showPins ? 'text-yellow-400' : 'text-white'} transition-colors`} />
                            </div>
                            <span className={`text-[10px] ${activeTab === 'explorar' && showPins ? 'text-yellow-400 font-bold' : 'text-white/90 font-medium'}`}>Explorar</span>
                        </button>

                        <button
                            onClick={() => setActiveTab('agregar')}
                            className={`flex flex-col items-center gap-1 group transition-colors ${activeTab === 'agregar' ? 'opacity-100' : 'opacity-70'}`}
                        >
                            <div className={`border-2 border-white rounded-full p-0.5 ${activeTab === 'agregar' ? 'bg-white/20' : ''}`}>
                                <Plus className="h-3 w-3 text-white font-bold" />
                            </div>
                            <span className="text-[10px] text-white font-medium">Agregar</span>
                        </button>
                    </div>
                </div>
            )}

        </div>
    );
};

export default MapComponent;
