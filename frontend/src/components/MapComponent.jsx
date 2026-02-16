import React, { useState, useEffect } from 'react';
import { MapContainer, Marker, Popup, Polyline, ImageOverlay, useMap, TileLayer, useMapEvents } from 'react-leaflet';
import { useNavigate } from 'react-router-dom';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { MAP_CONFIG } from '../mapConfig';
import esimeLogo from '../assets/esime-logo.png';
import { User, Compass, Navigation as NavIcon, Car, Bookmark, Map as MapIcon, Plus, ArrowLeft, ArrowUpDown, MoreHorizontal, Send, X } from 'lucide-react';
import SavedPlacesSheet from './SavedPlacesSheet';
import { savePlace, deletePlace, updatePlace } from '../services/api';

// Configuracion de iconos
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Iconos personalizados del mapa
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

// Componente que muestra la ubicacion del usuario
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
            <Popup><span className="text-black font-bold">Tu</span></Popup>
        </Marker>
    );
};

// Manejador de clicks en el mapa para agregar pins personalizados
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

// Controlador que anima la camara del mapa hacia una ubicacion
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

// Componente principal del mapa
const MapComponent = ({ buildings, locations, customPins, setCustomPins, route, setRoute, navInfo, onSelectPoint, onCalculateRoute, selection, showPins, togglePins }) => {
    const navigate = useNavigate();
    const [userPos, setUserPos] = useState(null);
    const [activeTab, setActiveTab] = useState('explorar');

    // Estado del modo de navegacion
    const [isNavigating, setIsNavigating] = useState(false);
    const [navOrigin, setNavOrigin] = useState("Tu ubicacion");
    const [navDestination, setNavDestination] = useState("");

    // Estado para agregar pins personalizados
    const [pendingPin, setPendingPin] = useState(null);
    const [pinName, setPinName] = useState("");
    const [editingPinId, setEditingPinId] = useState(null);


    // Estado de busqueda y control
    const [searchQuery, setSearchQuery] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [targetLocation, setTargetLocation] = useState(null);
    const [selectingMode, setSelectingMode] = useState(null); // 'origin' or 'destination'

    // Initial search logic
    const handleSearch = (query) => {
        setSearchQuery(query);
        if (!query.trim()) {
            setSearchResults([]);
            setShowSuggestions(false);
            return;
        }

        const lowerQuery = query.toLowerCase();

        // Search in Buildings (using name or nombre)
        const buildingMatches = buildings
            .filter(b => (b.name || b.nombre || "").toLowerCase().includes(lowerQuery))
            .map(b => ({ ...b, name: b.name || b.nombre, type: 'static', id: `b-${b.id}` }));

        // Search in Custom Pins
        const customMatches = customPins
            .filter(p => p.name.toLowerCase().includes(lowerQuery))
            .map(p => ({ ...p, type: 'custom', id: `cust-${p.id}` }));

        setSearchResults([...buildingMatches, ...customMatches]);
        setShowSuggestions(true);
    };

    const handleSelectResult = (result) => {
        const lat = result.lat;
        const lon = result.lon;
        const id = result.id; // Use the ID already constructed in handleSearch

        setVisiblePinIds([id]); // Force visibility
        setTargetLocation([lat, lon]);
        setSearchQuery(result.name);
        setShowSuggestions(false);
        onSelectPoint('destination', result.name);

        setTimeout(() => {
            const mk = markerRefs.current[id];
            if (mk) mk.openPopup();
        }, 800);
    };

    // Estado para visibilidad selectiva de pins
    const [visiblePinIds, setVisiblePinIds] = useState([]);

    // Estado para ocultar pines del sistema (Eliminados por usuario)
    const [hiddenPinIds, setHiddenPinIds] = useState(() => {
        const saved = localStorage.getItem('hidden_sys_pins');
        return saved ? JSON.parse(saved) : [];
    });

    // Referencias para los markers
    const markerRefs = React.useRef({});

    // Logica para filtrar por tipo
    const handleFilterClick = (type) => {
        let searchTerm = type.toLowerCase();
        let exactMatchName = null;

        // Configuration for specific buttons
        if (type === 'Auditorio') exactMatchName = "Auditorio";
        if (type === 'Gimnasio') exactMatchName = "Gimnasio de Basquetbol/Voleibol/Taekwondo";
        if (type === 'Cafeteria') exactMatchName = "Cafeteria Principal";

        let match;
        if (exactMatchName) {
            match = buildings.find(b => (b.name || b.nombre) === exactMatchName);
        }

        // Fallback or generic search
        if (!match) {
            // Correcion de terminos para busqueda generica
            if (type === 'Gimnasio') searchTerm = 'gimnacio';
            if (type === 'Cafeteria') searchTerm = 'cafeteria';

            match = buildings.find(b => (b.name || b.nombre || "").toLowerCase().includes(searchTerm)) ||
                locations.find(l => l.name.toLowerCase().includes(searchTerm));
        }

        if (match) {
            const lat = match.lat || match.latitud;
            const lon = match.lon || match.longitud;
            // Since everything is in 'buildings' and rendered with 'b-' prefix, force 'b-'
            // Exception: if it came from 'locations' (unlikely now), use loc-index?
            // Safer: if match has id, assume b-{id}
            const id = match.id ? `b-${match.id}` : `loc-${locations.indexOf(match)}`;

            setVisiblePinIds([id]);
            setTargetLocation([lat, lon]);

            setTimeout(() => {
                const mk = markerRefs.current[id];
                if (mk) mk.openPopup();
            }, 800);

        } else {
            console.log("No encontrado para", searchTerm);
            if (type === 'Cafeteria') setTargetLocation([19.4326, -99.1332]);
        }
    };



    // Limites del mapa
    const imageBounds = MAP_CONFIG.overlay.bounds;
    const panningBounds = L.latLngBounds([
        [imageBounds[0][0] - 0.006, imageBounds[0][1] - 0.002],
        [imageBounds[1][0] + 0.002, imageBounds[1][1] + 0.002]
    ]);

    // Maneja el click en el mapa para agregar un pin
    const handleMapClick = (latlng) => {
        setPendingPin(latlng);
    };

    // Guarda o Actualiza un pin personalizado
    const handleSavePin = async () => {
        if (!pinName.trim()) {
            alert("Por favor ingresa un nombre.");
            return;
        }

        const storedUser = localStorage.getItem('user');
        if (!storedUser) {
            alert("Error: Inicia sesion nuevamente.");
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
            if (editingPinId !== null) {
                // UPDATE EXISTING PIN
                console.log("Updating pin:", editingPinId);
                const updatedPin = await updatePlace(editingPinId, {
                    name: pinName,
                    lat: pendingPin.lat,
                    lon: pendingPin.lng,
                    type: 'custom'
                });

                if (setCustomPins) {
                    setCustomPins(prev => prev.map(p => p.id === editingPinId ? updatedPin : p));
                }
                alert("Actualizado correctamente");
            } else {
                // CREATE NEW PIN
                if (!pendingPin) return;
                const newPin = await savePlace({
                    user_boleta: user.boleta,
                    name: pinName,
                    lat: pendingPin.lat,
                    lon: pendingPin.lng,
                    type: 'custom'
                });

                if (setCustomPins) {
                    setCustomPins([...customPins, newPin]);
                }
                alert("Guardado");
            }

            // Cleanup
            setPendingPin(null);
            setPinName("");
            setEditingPinId(null);
        } catch (e) {
            console.error("Error saving/updating pin", e);
            alert("Error: " + e.message);
        }
    };

    const handleInitEdit = (pin) => {
        setEditingPinId(pin.id);
        setPinName(pin.name);
        setPendingPin({ lat: pin.lat, lng: pin.lon });

        const mk = markerRefs.current[`cust-${pin.id}`];
        if (mk) mk.closePopup();
    };

    const handleCancelSave = () => {
        setPendingPin(null);
        setPinName("");
        setEditingPinId(null);
    };

    // Inicia el modo navegacion
    const startNavigation = () => {
        setIsNavigating(true);
        onSelectPoint('destination', selection.destination);
    };

    // Inicia el calculo de la ruta
    const handleStartRoute = () => {
        if (onCalculateRoute && navDestination) {
            onCalculateRoute(navOrigin, navDestination, userPos);
        }
    };

    // Sale del modo navegacion
    const exitNavigation = () => {
        setIsNavigating(false);
        setNavDestination("");
        onSelectPoint('clear');
        setRoute(null);
    };

    // Elimina un pin personalizado
    // Elimina un pin personalizado o oculta uno del sistema
    const handleDeletePin = async (id, name, isCustom) => {
        if (confirm(`Eliminar ${name}?`)) {
            if (isCustom) {
                try {
                    await deletePlace(id);
                    // Update parent state via prop
                    if (setCustomPins) {
                        setCustomPins(prev => prev.filter(p => p.id !== id));
                    }
                } catch (e) {
                    console.error("Error deleting pin", e);
                    alert("Error al eliminar: " + e.message);
                }
            } else {
                // Es un pin del sistema -> Ocultar logicamente
                const newHidden = [...hiddenPinIds, id];
                setHiddenPinIds(newHidden);
                localStorage.setItem('hidden_sys_pins', JSON.stringify(newHidden));
            }
        }
    };

    // Maneja el click en la brujula
    const handleCompassClick = () => {
        if (!userPos) {
            alert("Ubicacion no disponible");
            return;
        }

        // Centro aproximado de la escuela
        const schoolCenter = L.latLng(19.33059, -99.11211);
        const dist = schoolCenter.distanceTo(userPos);

        if (dist > 3000) {
            alert("Estas muy lejos de la escuela. Acercate para usar esta funcion.");
        } else {
            setTargetLocation([userPos.lat, userPos.lng]);
        }
    };

    // Intercambia origen y destino
    const handleSwapOriginDest = () => {
        const temp = navOrigin;
        setNavOrigin(navDestination);
        setNavDestination(temp);

        // Update parent selection
        onSelectPoint('origin', navDestination);
        onSelectPoint('destination', temp);
    };

    const redGradientIcon = new L.DivIcon({
        className: 'custom-div-icon', // Wrapper to avoid default styles interfering
        html: "<div class='gradient-red-pin'></div>",
        iconSize: [30, 30],
        iconAnchor: [15, 30],
        popupAnchor: [0, -30]
    });

    // Selecciona un pin para navegacion
    const handlePinSelectForNav = (name) => {
        if (selectingMode === 'origin') {
            setNavOrigin(name);
            onSelectPoint('origin', name);
            setSelectingMode(null); // Show menu again
            return;
        }
        if (selectingMode === 'destination') {
            setNavDestination(name);
            onSelectPoint('destination', name);
            setSelectingMode(null); // Show menu again
            return;
        }

        // Default behavior (Start new navigation to this point)
        setNavDestination(name);
        setIsNavigating(true);
        onSelectPoint('destination', name);
        onSelectPoint('origin', 'Tu ubicacion');
    };

    // Renderiza un marcador en el mapa
    const renderMarker = (name, lat, lon, id, isCustom = false) => {
        const isVisibleById = visiblePinIds.includes(id);

        const shouldShow = showPins ||
            activeTab === 'agregar' ||
            isNavigating ||
            activeTab === 'guardados' ||
            isVisibleById;

        if (!shouldShow) return null;

        const isOrigin = navOrigin === name;
        const isDest = navDestination === name;

        const icon = isCustom ? blueIcon : redGradientIcon;

        return (
            <Marker
                key={id}
                position={[lat, lon]}
                icon={icon}
                zIndexOffset={isCustom ? 9000 : 0}
                ref={(el) => markerRefs.current[id] = el}
                draggable={isCustom && editingPinId === parseInt(id.replace('cust-', ''), 10)}
                eventHandlers={{
                    dragend: (e) => {
                        const marker = e.target;
                        const position = marker.getLatLng();
                        setPendingPin({ lat: position.lat, lng: position.lng });
                    }
                }}
            >
                <Popup>
                    <div className="text-center p-1 flex flex-col gap-2 min-w-35">
                        <h3 className="font-bold text-gray-800 border-b pb-1">{name}</h3>

                        {/* Standard Navigation Actions for ALL pins */}
                        <div className="flex flex-col gap-1.5 mt-1">
                            {selectingMode ? (
                                <button
                                    onClick={() => handlePinSelectForNav(name)}
                                    className="w-full bg-green-600 text-white text-xs py-2 px-3 rounded-lg font-bold shadow-md hover:bg-green-700"
                                >
                                    Seleccionar {selectingMode === 'origin' ? 'Origen' : 'Destino'}
                                </button>
                            ) : isNavigating ? (
                                <>
                                    {/* Origin Selection */}
                                    {isOrigin ? (
                                        <span className="text-xs text-blue-600 font-bold bg-blue-50 py-1 px-2 rounded">📍 Origen Actual</span>
                                    ) : (
                                        <button
                                            onClick={() => {
                                                setNavOrigin(name);
                                                setIsNavigating(true); // Ensure nav mode
                                            }}
                                            className="bg-gray-100 text-gray-700 text-xs py-1.5 px-2 rounded hover:bg-gray-200"
                                        >
                                            Poner como Inicio
                                        </button>
                                    )}

                                    {/* Destination Selection */}
                                    {isDest ? (
                                        <span className="text-xs text-green-600 font-bold bg-green-50 py-1 px-2 rounded">🏁 Destino Actual</span>
                                    ) : (
                                        <button
                                            onClick={() => {
                                                setNavDestination(name);
                                                setIsNavigating(true);
                                                onSelectPoint('destination', name);
                                            }}
                                            className="bg-blue-600 text-white text-xs py-1.5 px-3 rounded-lg font-bold shadow-md hover:bg-blue-700"
                                        >
                                            Ir aquí
                                        </button>
                                    )}
                                </>
                            ) : (
                                /* Normal Mode Actions */
                                <>
                                    <button
                                        onClick={() => handlePinSelectForNav(name)}
                                        className="bg-blue-600 text-white text-xs py-1.5 px-3 rounded-lg font-bold shadow-md hover:bg-blue-700"
                                    >
                                        Ir aquí
                                    </button>

                                    <button
                                        onClick={() => {
                                            setNavOrigin(name);
                                            setIsNavigating(true);
                                            // Ideally open the nav UI with this as origin
                                        }}
                                        className="bg-gray-100 text-gray-700 text-xs py-1 px-2 rounded hover:bg-gray-200 border"
                                    >
                                        Desde aquí
                                    </button>
                                </>
                            )}
                        </div>

                        {/* Custom Pin Actions (Delete + Edit) */}
                        {isCustom && (
                            <div className="flex flex-col gap-1 mt-2 pt-2 border-t">
                                <div className="flex gap-2">
                                    <button
                                        onClick={() => handleInitEdit({
                                            id: parseInt(id.replace('cust-', ''), 10),
                                            name, lat, lon
                                        })}
                                        className="flex-1 bg-yellow-50 text-yellow-700 text-xs py-1 px-2 rounded hover:bg-yellow-100 border border-yellow-200"
                                    >
                                        Editar
                                    </button>
                                    <button
                                        onClick={() => handleDeletePin(id.replace('cust-', ''), name, isCustom)}
                                        className="flex-1 bg-red-50 text-red-600 text-xs py-1 px-2 rounded hover:bg-red-100 border border-red-200"
                                    >
                                        Eliminar
                                    </button>
                                </div>
                            </div>
                        )}
                    </div>
                </Popup>
            </Marker>
        );
    };

    return (
        <div className="relative h-screen w-full flex flex-col bg-white overflow-hidden font-sans">

            {/* INTERFAZ DEL MODO NAVEGACION ENCABEZADO ROJO */}
            {/* INTERFAZ DEL MODO NAVEGACION ENCABEZADO ROJO */}
            {isNavigating && (
                <>
                    {!selectingMode ? (
                        <div className="absolute top-0 left-0 w-full z-1200 bg-red-800 rounded-b-8xl shadow-2xl p-4 pt-12 animate-in slide-in-from-top duration-300">
                            <div className="flex items-center gap-3 mb-4">
                                <button onClick={exitNavigation} className="text-white p-1 hover:bg-white/10 rounded-full">
                                    <ArrowLeft size={24} />
                                </button>
                                <div className="flex-1 flex flex-col gap-2">
                                    {/* Entrada de origen */}
                                    <div
                                        className="bg-black/20 rounded-lg flex items-center px-3 py-2 border border-white/10 cursor-pointer hover:bg-black/30 transition-colors"
                                        onClick={() => setSelectingMode('origin')}
                                    >
                                        <div className="w-4 h-4 rounded-full border-2 border-white/60 mr-3"></div>
                                        <div className="flex-1 text-white text-sm font-semibold truncate">
                                            {navOrigin || "Tu ubicación"}
                                        </div>
                                    </div>
                                    {/* Entrada de destino */}
                                    <div
                                        className="bg-black/20 rounded-lg flex items-center px-3 py-2 border border-white/10 cursor-pointer hover:bg-black/30 transition-colors"
                                        onClick={() => setSelectingMode('destination')}
                                    >
                                        <div className="w-4 h-4 rounded-full border-2 border-red-200 mr-3 bg-red-500"></div>
                                        <div className="flex-1 text-white text-sm font-semibold truncate">
                                            {navDestination || "Seleccionar destino..."}
                                        </div>
                                    </div>
                                </div>
                                <div className="flex flex-col gap-3 text-white">
                                    <MoreHorizontal size={24} />
                                    <button onClick={(e) => { e.stopPropagation(); handleSwapOriginDest(); }} className="hover:bg-white/20 rounded-full p-1 transition-colors">
                                        <ArrowUpDown size={20} />
                                    </button>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="absolute top-0 left-0 w-full z-1200 p-4 pt-12 flex justify-center pointer-events-none">
                            <div className="bg-red-800 text-white px-6 py-3 rounded-full shadow-2xl pointer-events-auto flex items-center gap-4 animate-in slide-in-from-top duration-300">
                                <span className="font-bold text-sm">
                                    {selectingMode === 'origin' ? "Selecciona el Origen" : "Selecciona el Destino"} en el mapa
                                </span>
                                <button
                                    onClick={() => setSelectingMode(null)}
                                    className="bg-white/20 hover:bg-white/30 rounded-full p-1 transition-colors"
                                >
                                    <X size={16} />
                                </button>
                            </div>
                        </div>
                    )}
                </>
            )}

            {/* --- NORMAL TOP UI --- */}
            {!isNavigating && activeTab !== 'guardados' && (
                <div className="absolute top-0 left-0 w-full z-1001 px-4 pt-12 pb-4 flex flex-col gap-3 pointer-events-none">
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
                                <div className="absolute top-full left-0 w-full bg-white rounded-lg shadow-xl mt-2 max-h-60 overflow-y-auto no-scrollbar z-1300">
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
                        {['Cafeteria', 'Gimnasio', 'Auditorio', 'Biblioteca'].map((chip, idx) => (
                            <button
                                key={idx}
                                onClick={() => handleFilterClick(chip)}
                                className="bg-white whitespace-nowrap px-4 py-2 rounded-full shadow-md text-xs font-bold text-gray-800 flex items-center gap-1.5 active:scale-95 transition-transform"
                            >
                                <span className="text-gray-900 text-sm">
                                    {chip === 'Cafeteria' && '🍴'} {chip === 'Gimnasio' && '🏋️'} {chip === 'Auditorio' && '🎭'} {chip === 'Biblioteca' && '📚'}
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
                    {/* Filter out buildings that are already in customPins to avoid overlap */}
                    {buildings
                        .filter(b => !customPins.some(p => p.name === (b.name || b.nombre)))
                        .filter(b => !hiddenPinIds.includes(`b-${b.id}`))
                        .map((b) => renderMarker(b.name || b.nombre, b.lat, b.lon, `b-${b.id}`))}
                    {locations
                        .filter(l => !hiddenPinIds.includes(`loc-${locations.indexOf(l)}`)) // Using index as ID base
                        .map((loc, idx) => renderMarker(loc.name, loc.lat, loc.lon, `loc-${idx}`))}
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

            {pendingPin && (
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-4 rounded-xl shadow-2xl w-64 animate-in fade-in zoom-in duration-200" style={{ zIndex: 1500 }}>
                    <h3 className="font-bold text-gray-800 text-sm mb-3 text-center">
                        {editingPinId ? 'Editar: Arrastra para mover' : 'Nuevo Lugar'}
                    </h3>
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
                                onClick={handleCancelSave}
                                className="flex-1 bg-gray-100 text-gray-700 text-xs font-bold py-2 rounded-lg hover:bg-gray-200 transition-colors"
                            >
                                Cancelar
                            </button>
                            <button
                                onClick={handleSavePin}
                                className="flex-1 bg-[#b91c1c] text-white text-xs font-bold py-2 rounded-lg shadow-md hover:bg-red-700 transition-colors"
                            >
                                {editingPinId ? 'Actualizar' : 'Guardar'}
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* --- ADD PIN INSTRUCTION --- */}
            {activeTab === 'agregar' && !pendingPin && (
                <div className="absolute top-32 left-1/2 transform -translate-x-1/2 bg-black/70 text-white px-4 py-2 rounded-full z-1100 text-sm font-bold shadow-lg animate-bounce pointer-events-none">
                    📍 Toca el mapa para agregar un pin
                </div>
            )}

            {/* --- NAV BOTTOM SHEET (Route Info) --- */}
            {isNavigating && selection?.destination && (route || true) && (
                <div className="absolute bottom-6 left-4 right-4 bg-[#b91c1c] text-white rounded-4xl p-6 shadow-2xl z-1200">
                    <div className="flex items-center justify-between mb-4">
                        <div>
                            <h2 className="text-2xl font-black">
                                {navInfo?.distancia ? `${navInfo.distancia} m` : (route ? 'Calculando...' : '')}
                            </h2>
                            <p className="text-lg font-bold opacity-90">
                                {navInfo?.tiempo || ''}
                            </p>
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
                <div className="absolute bottom-28 right-4 z-1000 flex flex-col items-end gap-3">
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
                    <div className="fixed inset-0 bg-black/50 z-1050" onClick={() => setActiveTab('explorar')} />
                    <div className="fixed inset-x-0 bottom-0 z-1100">
                        <SavedPlacesSheet onClose={() => setActiveTab('explorar')} />
                    </div>
                </>
            )}

            {/* --- BOTTOM NAVIGATION BAR --- */}
            {!isNavigating && (
                <div className="absolute bottom-4 left-4 right-4 z-1001">
                    <div className="bg-[#b30000] rounded-[2.5rem] px-6 py-4 flex justify-between items-center shadow-2xl relative">
                        {/* Nav Items... Same as before */}
                        <button
                            onClick={() => navigate('/parking')}
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
