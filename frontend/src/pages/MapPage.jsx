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

    return (
        <div className="h-screen w-full">
            <MapComponent
                buildings={buildings}
                parking={parking}
                route={route}
                navInfo={navInfo}
                selection={selection}
                onSelectPoint={handleSelectPoint}
                onNextClassClick={handleNavigateNextClass}
            />
        </div>
    );
};

export default MapPage;
