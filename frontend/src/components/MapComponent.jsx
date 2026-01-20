import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, ImageOverlay } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { MAP_CONFIG } from '../mapConfig';

// Icons setup (Standard Leaflet fix + Custom colors)
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const buildingIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/markers-default.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

const parkingFreeIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

const parkingBusyIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

const MapComponent = ({ buildings, parking, route }) => {
    return (
        <MapContainer
            center={MAP_CONFIG.center}
            zoom={MAP_CONFIG.zoom}
            scrollWheelZoom={true}
            className="h-full w-full z-0"
        >
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            {/* Custom School Map Overlay */}
            {MAP_CONFIG.overlay.enabled && (
                <ImageOverlay
                    url={MAP_CONFIG.overlay.imageUrl}
                    bounds={MAP_CONFIG.overlay.bounds}
                    opacity={0.8}
                />
            )}

            {/* Buildings */}
            {buildings.map((b) => (
                <Marker key={`b-${b.id}`} position={[b.lat, b.lon]} icon={buildingIcon}>
                    <Popup>
                        <div className="text-center">
                            <h3 className="font-bold text-lg">{b.nombre}</h3>
                            <button className="mt-2 text-blue-600 underline">Ver Salones</button>
                        </div>
                    </Popup>
                </Marker>
            ))}

            {/* Parking */}
            {parking.map((p) => (
                <Marker
                    key={`p-${p.id}`}
                    position={p.coords}
                    icon={p.ocupado ? parkingBusyIcon : parkingFreeIcon}
                >
                    <Popup>
                        <div className="text-center">
                            <h3 className="font-bold text-sm">Estacionamiento {p.numero}</h3>
                            <p className={p.ocupado ? "text-red-600 font-bold" : "text-green-600 font-bold"}>
                                {p.ocupado ? "Ocupado" : "Disponible"}
                            </p>
                            <p className="text-xs text-gray-500 capitalize">{p.tipo}</p>
                        </div>
                    </Popup>
                </Marker>
            ))}

            {/* Route Polyline */}
            {route && route.length > 0 && (
                <Polyline positions={route} color="blue" weight={5} opacity={0.7} />
            )}

            {!buildings.length && !parking.length && (
                <Marker position={MAP_CONFIG.center} icon={buildingIcon}>
                    <Popup>ESIME Culhuacan (Centro)</Popup>
                </Marker>
            )}
        </MapContainer>
    );
};

export default MapComponent;
