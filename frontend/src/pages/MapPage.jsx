import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import MapComponent from '../components/MapComponent';
import { getBuildings, getParking, getRoute } from '../services/api';

const MapPage = () => {
    const navigate = useNavigate();
    const [buildings, setBuildings] = useState([]);
    const [parking, setParking] = useState([]);
    const [route, setRoute] = useState(null); // Array of coords
    const [navInfo, setNavInfo] = useState(null);

    useEffect(() => {
        if (!localStorage.getItem('user')) {
            navigate('/');
            return;
        }

        getBuildings().then(setBuildings).catch(console.error);
        getParking().then(setParking).catch(console.error);
    }, [navigate]);

    const handleNavigateNextClass = () => {
        // Mock Current Location (Edificio 2 entrance aprox)
        const userLat = 19.311500;
        const userLon = -99.112000;
        const user = JSON.parse(localStorage.getItem('user'));

        getRoute({
            lat: userLat,
            lon: userLon,
            boleta: user.boleta,
            type: 'next_class'
        }).then(data => {
            // data.camino is list of building names.
            // We need coordinates for the polyline.
            // We match building names to buildings state
            const coords = [];

            // Add start
            coords.push([userLat, userLon]);

            data.camino.forEach(name => {
                const b = buildings.find(b => b.nombre === name);
                if (b) coords.push([b.lat, b.lon]);
            });

            setRoute(coords);
            setNavInfo(`Ruta: ${data.origen} -> ${data.destino} (${data.distancia}m)`);
        }).catch(err => {
            console.error(err);
            alert("No se pudo calcular la ruta o no hay clases próximas.");
        });
    };

    return (
        <div className="h-screen w-full flex flex-col">
            <header className="bg-blue-900 text-white p-4 flex justify-between items-center shadow-md z-10">
                <h1 className="text-xl font-bold">Mapa ESIME</h1>
                <div className="space-x-4">
                    <button onClick={() => navigate('/dashboard')} className="hover:text-blue-200">Mi Perfil</button>
                    <button onClick={() => {
                        localStorage.removeItem('user');
                        navigate('/');
                    }} className="hover:text-blue-200">Salir</button>
                </div>
            </header>

            <div className="flex-1 relative z-0">
                <MapComponent buildings={buildings} parking={parking} route={route} />

                {/* Navigation Control */}
                <div className="absolute bottom-10 left-10 z-[1000] bg-white p-4 rounded-lg shadow-xl border border-gray-200">
                    <p className="font-bold text-gray-700 mb-2">Navegación</p>
                    {navInfo && <div className="mb-2 text-sm text-green-700 font-mono bg-green-50 p-1 rounded">{navInfo}</div>}
                    <button
                        onClick={handleNavigateNextClass}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium text-sm w-full"
                    >
                        Ir a mi siguiente clase
                    </button>
                </div>
            </div>
        </div>
    );
};

export default MapPage;
