import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getSchedule } from '../services/api';

const Dashboard = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [schedule, setSchedule] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (!storedUser) {
            navigate('/');
            return;
        }
        const parsedUser = JSON.parse(storedUser);
        setUser(parsedUser);

        getSchedule(parsedUser.boleta)
            .then(data => {
                setSchedule(data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, [navigate]);

    if (!user) return null;

    return (
        <div className="min-h-screen bg-gray-50 p-6">
            <div className="max-w-4xl mx-auto space-y-6">
                <div className="flex justify-between items-center">
                    <h1 className="text-3xl font-bold text-gray-900">Mi Perfil</h1>
                    <button onClick={() => navigate('/map')} className="text-blue-600 hover:text-blue-800">
                        &larr; Volver al Mapa
                    </button>
                </div>

                <div className="bg-white p-6 rounded-lg shadow">
                    <h2 className="text-xl font-semibold mb-4 text-blue-900">Información del Estudiante</h2>
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <p className="text-gray-500 text-sm">Nombre</p>
                            <p className="font-medium">{user.nombre}</p>
                        </div>
                        <div>
                            <p className="text-gray-500 text-sm">Boleta</p>
                            <p className="font-medium">{user.boleta}</p>
                        </div>
                        <div>
                            <p className="text-gray-500 text-sm">Carrera</p>
                            <p className="font-medium">{user.carrera || "No asignada"}</p>
                        </div>
                        <div>
                            <p className="text-gray-500 text-sm">Transporte</p>
                            <p className="font-medium capitalize">{user.vehiculo}</p>
                        </div>
                    </div>
                </div>

                <div className="bg-white p-6 rounded-lg shadow">
                    <h2 className="text-xl font-semibold mb-4 text-blue-900">Horario del Día</h2>
                    {loading ? (
                        <p>Cargando...</p>
                    ) : schedule.length === 0 ? (
                        <p className="text-gray-500">No hay clases registradas para hoy.</p>
                    ) : (
                        <ul className="space-y-3">
                            {schedule.map((clase, idx) => (
                                <li key={idx} className="p-3 bg-blue-50 rounded-md border border-blue-100 flex justify-between items-center">
                                    <div>
                                        <p className="font-bold text-blue-900">{clase.materia}</p>
                                        <p className="text-sm text-gray-600">Salón {clase.sala} ({clase.edificio})</p>
                                    </div>
                                    <span className="font-mono text-blue-700 bg-white px-2 py-1 rounded shadow-sm">
                                        {clase.hora}
                                    </span>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
