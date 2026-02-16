import React, { useEffect, useState } from 'react';
import keyPoints from '../data/key_points.json';
import { useNavigate } from 'react-router-dom';
import MapComponent from '../components/MapComponent';
import { getBuildings, getParking, getRoute, getWalkingRoute, getSavedPlaces } from '../services/api';
import locations from '../locations.json';

const MapPage = () => {
    const navigate = useNavigate();
    const [buildings, setBuildings] = useState(keyPoints); // Load static key points
    const [parking, setParking] = useState([]);
    const [customPins, setCustomPins] = useState([]);
    const [route, setRoute] = useState(null);
    const [navInfo, setNavInfo] = useState(null);
    const [selection, setSelection] = useState({ origin: null, destination: null });
    const [showPins, setShowPins] = useState(false);

    const togglePins = () => setShowPins(prev => !prev);

    useEffect(() => {
        const userStr = localStorage.getItem('user');
        if (!userStr) {
            navigate('/');
            return;
        }
        const user = JSON.parse(userStr);

        // Buildings are now static keyPoints loaded in initial state
        // getBuildings().then(setBuildings).catch(console.error);
        getParking().then(setParking).catch(console.error);
        getSavedPlaces(user.boleta).then(data => {
            if (Array.isArray(data)) setCustomPins(data);
        }).catch(console.error);
    }, [navigate]);

    const handleSelectPoint = (type, name) => {
        const newSelection = { ...selection, [type]: name };
        setSelection(newSelection);
    };

    const findCoordinates = (name) => {
        if (!name) return null;
        if (name === "Tu ubicacion" || name === "Tu ubicación") return null; // Handle separately

        // Check buildings
        const b = buildings.find(x => (x.name || x.nombre) === name);
        if (b) return { lat: b.lat, lon: b.lon };

        // Check static locations
        const l = locations.find(x => x.name === name);
        if (l) return { lat: l.lat, lon: l.lon };

        // Check custom pins
        const p = customPins.find(x => x.name === name);
        if (p) return { lat: p.lat, lon: p.lon };

        return null;
    };

    const handleNavigateNextClass = (userPos) => {
        const startLat = userPos ? userPos.lat : 19.33059;
        const startLon = userPos ? userPos.lng : -99.11211;
        const user = JSON.parse(localStorage.getItem('user'));

        getRoute({ // Uses legacy route for schedule logic
            lat: startLat,
            lon: startLon,
            boleta: user.boleta,
            type: 'next_class'
        }).then(data => {
            // ... legacy handling or adapt to new ...
            // For now assuming legacy endpoint still returns list of names
            const coords = [];
            if (data.camino) {
                data.camino.forEach(name => {
                    const c = findCoordinates(name);
                    if (c) coords.push([c.lat, c.lon]);
                });
            }
            setRoute(coords);
            setNavInfo(data.info || `${data.origen} -> ${data.destino}`);
            setSelection({ origin: 'Tu ubicación', destination: data.destino });
        }).catch(err => {
            console.error(err);
            alert("Ruta no encontrada o no hay clases registradas hoy.");
        });
    };

    const handleCalculateRoute = (originName, destName, userPos) => {
        let startCoords = null;
        let endCoords = null;

        // Resolve Origin
        if (!originName || originName === "Tu ubicacion" || originName === "Tu ubicación") {
            if (userPos) {
                startCoords = { lat: userPos.lat, lon: userPos.lng };
            } else {
                alert("Ubicación no disponible.");
                return;
            }
        } else {
            startCoords = findCoordinates(originName);
        }

        // Resolve Destination
        endCoords = findCoordinates(destName);

        if (!startCoords || !endCoords) {
            alert("No se pudieron encontrar las coordenadas de origen o destino.");
            return;
        }

        // Call KML Router
        getWalkingRoute(startCoords.lat, startCoords.lon, endCoords.lat, endCoords.lon)
            .then(data => {
                if (data.path && data.path.length > 0) {
                    setRoute(data.path); // [[lat, lon], ...]
                    const minutes = Math.ceil(data.eta_minutes);
                    setNavInfo({
                        distancia: Math.round(data.distance),
                        tiempo: `${minutes} min`,
                        descripcion: `De ${originName || 'Ubicación'} a ${destName}`
                    });
                } else {
                    alert("Ruta no encontrada.");
                }
            })
            .catch(err => {
                console.error(err);
                alert("Error al calcular la ruta.");
            });
    };

    return (
        <div className="h-screen w-full">
            <MapComponent
                buildings={buildings}
                parking={parking}
                locations={locations}
                customPins={customPins}
                setCustomPins={setCustomPins}
                route={route}
                navInfo={navInfo}
                selection={selection}
                onSelectPoint={handleSelectPoint}
                onCalculateRoute={handleCalculateRoute}
                onNextClassClick={handleNavigateNextClass}
                showPins={showPins}
                togglePins={togglePins}
            />
        </div>
    );
};

export default MapPage;
