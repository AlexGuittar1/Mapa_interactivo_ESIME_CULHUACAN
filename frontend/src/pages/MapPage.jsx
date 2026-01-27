import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import MapComponent from '../components/MapComponent';
import { getBuildings, getParking, getRoute } from '../services/api';

const MapPage = () => {
    const navigate = useNavigate();
    const [buildings, setBuildings] = useState([]);
    const [parking, setParking] = useState([]);
    const [route, setRoute] = useState(null);
    const [navInfo, setNavInfo] = useState(null);
    const [selection, setSelection] = useState({ origin: null, destination: null });
    const [showPins, setShowPins] = useState(false);

    const togglePins = () => setShowPins(prev => !prev);

    useEffect(() => {
        const user = localStorage.getItem('user');
        if (!user) {
            navigate('/');
            return;
        }
        getBuildings().then(setBuildings).catch(console.error);
        getParking().then(setParking).catch(console.error);
    }, [navigate]);

    const handleSelectPoint = (type, name) => {
        const newSelection = { ...selection, [type]: name };
        setSelection(newSelection);

        // If both are selected, trigger auto-routing
        if (newSelection.origin && newSelection.destination) {
            calculateArbitraryRoute(newSelection.origin, newSelection.destination);
        }
    };

    const calculateArbitraryRoute = (origin, destination) => {
        getRoute({ origen: origin, destino: destination })
            .then(data => {
                const coords = [];
                data.camino.forEach(name => {
                    const b = buildings.find(b => b.nombre === name);
                    if (b) coords.push([b.lat, b.lon]);
                });
                setRoute(coords);
                setNavInfo(`De ${origin} a ${destination}`);
            })
            .catch(err => {
                console.error(err);
                alert("No se pudo encontrar una ruta entre esos puntos.");
            });
    };

    const handleNavigateNextClass = (userPos) => {
        const startLat = userPos ? userPos.lat : 19.33059;
        const startLon = userPos ? userPos.lng : -99.11211;
        const user = JSON.parse(localStorage.getItem('user'));

        getRoute({
            lat: startLat,
            lon: startLon,
            boleta: user.boleta,
            type: 'next_class'
        }).then(data => {
            const coords = [[startLat, startLon]];
            data.camino.forEach(name => {
                const b = buildings.find(b => b.nombre === name);
                if (b) coords.push([b.lat, b.lon]);
            });
            setRoute(coords);
            setNavInfo(data.info || `${data.origen} -> ${data.destino}`);
            // Clear selections if it was next_class
            setSelection({ origin: 'Tu ubicación', destination: data.destino });
        }).catch(err => {
            console.error(err);
            alert("Ruta no encontrada o no hay clases registradas hoy.");
        });
    };

    const handleCalculateRoute = (origin, destination, userPos) => {
        let routeParams = { destino: destination };

        if (!origin || origin === "Tu ubicación") {
            if (userPos) {
                routeParams.origen = null; // Backend handles lat/lon if name is null
                routeParams.lat = userPos.lat;
                routeParams.lon = userPos.lng;
            } else {
                // Fallback if no user location
                routeParams.origen = "Explanada ESIME"; // Default internal origin
                alert("Ubicación no disponible, usando Explanada como origen.");
            }
        } else {
            routeParams.origen = origin;
        }

        getRoute(routeParams).then(data => {
            const coords = [];
            // Backend returns path of names or coords? 
            // Logic in calculateArbitraryRoute implies names. 
            // But if we used lat/lon, the first point might be coordinate.
            // If backend graph returns list of strings (node names):
            if (data.camino) {
                data.camino.forEach(name => {
                    const b = buildings.find(b => b.nombre === name);
                    if (b) coords.push([b.lat, b.lon]);
                });

                // If the path starts with current location (which isn't a named building)
                // We should prepend userPos if logic dictates.
                // Ideally backend adds the "START_NODE" which is nearest building.
                // So we just rely on buildings found.
            }

            // Fallback for demo: if 0 coords (e.g. unknown names), make a straight line
            if (coords.length < 2 && userPos) {
                const destB = buildings.find(b => b.nombre === destination);
                if (destB) {
                    coords.push([userPos.lat, userPos.lng]);
                    coords.push([destB.lat, destB.lon]);
                }
            }

            setRoute(coords);
            setNavInfo(data.info || `De ${origin} a ${destination}`);
        }).catch(err => {
            console.error(err);
            alert("Error calculando ruta. Revisa tu conexión.");
        });
    };

    return (
        <div className="h-screen w-full">
            <MapComponent
                buildings={buildings}
                parking={parking}
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
