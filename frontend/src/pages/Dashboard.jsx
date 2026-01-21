import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getSchedule, updateUser } from '../services/api';
import esimeLogo from '../assets/esime-1.png';

const Dashboard = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [schedule, setSchedule] = useState([]);
    const [loading, setLoading] = useState(true);
    const [updatingVehicle, setUpdatingVehicle] = useState(false);

    const vehicleOptions = [
        { id: 'ninguno', label: 'Ninguno', icon: '🚶' },
        { id: 'automovil', label: 'Automóvil', icon: '🚗' },
        { id: 'moto', label: 'Motocicleta', icon: '🏍️' },
        { id: 'bicicleta', label: 'Bicicleta', icon: '🚲' }
    ];

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

    const handleVehicleChange = async (newVehicle) => {
        if (!user) return;
        setUpdatingVehicle(true);
        try {
            const updatedUser = await updateUser(user.boleta, { vehiculo: newVehicle });
            setUser(updatedUser);
            localStorage.setItem('user', JSON.stringify(updatedUser));
        } catch (err) {
            alert("No se pudo actualizar el transporte.");
        } finally {
            setUpdatingVehicle(false);
        }
    };

    if (!user) return null;

    return (
        <div className="min-h-screen bg-white flex flex-col">
            <header className="header-gradient h-16 w-full flex justify-between items-center px-6 shadow-lg shrink-0">
                <div className="flex items-center gap-3">
                    <img src={esimeLogo} alt="ESIME Logo" className="h-12 w-auto object-contain drop-shadow-md" />
                    <h1 className="text-white font-black text-sm tracking-widest uppercase">MI PERFIL</h1>
                </div>
                <button
                    onClick={() => navigate('/map')}
                    className="bg-white/10 px-4 py-1.5 rounded-full text-white font-bold text-xs uppercase hover:bg-white/20 transition-all"
                >
                    Volver al Mapa
                </button>
            </header>

            <main className="flex-1 overflow-y-auto p-6 space-y-8 bg-gray-50/50">
                <div className="max-w-2xl mx-auto space-y-6">

                    {/* Perfil Card */}
                    <div className="glass-panel p-8 rounded-[2.5rem] relative overflow-hidden">
                        <div className="absolute top-0 right-0 w-32 h-32 bg-red-800/5 -mr-16 -mt-16 rounded-full"></div>

                        <div className="flex flex-col items-center mb-8">
                            <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-red-700 to-red-900 flex items-center justify-center text-4xl text-white font-black shadow-xl mb-4 border-4 border-white">
                                {user.nombre.charAt(0)}
                            </div>
                            <h2 className="text-xl font-black text-gray-800 tracking-tight">{user.nombre}</h2>
                            <p className="text-red-700 font-bold text-[10px] uppercase tracking-[0.2em] mt-1">{user.carrera || "Ingeniería"}</p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-white/40 p-6 rounded-3xl border border-white/60">
                            <div className="space-y-1 text-center border-b md:border-b-0 md:border-r border-gray-200 pb-4 md:pb-0">
                                <p className="text-[9px] font-black text-gray-400 uppercase tracking-widest">Boleta</p>
                                <p className="font-bold text-gray-700 text-sm">{user.boleta}</p>
                            </div>
                            <div className="space-y-3 text-center">
                                <p className="text-[9px] font-black text-gray-400 uppercase tracking-widest">Transporte</p>
                                <div className="flex flex-wrap justify-center gap-2">
                                    {vehicleOptions.map(opt => (
                                        <button
                                            key={opt.id}
                                            onClick={() => handleVehicleChange(opt.id)}
                                            disabled={updatingVehicle}
                                            className={`px-3 py-1.5 rounded-xl text-[10px] font-bold transition-all flex items-center gap-1.5 ${user.vehiculo === opt.id
                                                ? 'bg-red-800 text-white shadow-md'
                                                : 'bg-white text-gray-500 hover:bg-gray-100 border border-gray-100'
                                                }`}
                                        >
                                            <span>{opt.icon}</span>
                                            <span className="capitalize">{opt.label}</span>
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Schedule Section */}
                    <div className="space-y-4">
                        <div className="flex items-center gap-3 px-2">
                            <div className="w-1.5 h-6 bg-red-800 rounded-full"></div>
                            <h3 className="font-black text-gray-800 text-sm uppercase tracking-widest">Horario de Hoy</h3>
                        </div>

                        {loading ? (
                            <div className="flex justify-center py-10">
                                <div className="w-8 h-8 border-4 border-red-800 border-t-transparent rounded-full animate-spin"></div>
                            </div>
                        ) : schedule.length === 0 ? (
                            <div className="glass-panel p-10 rounded-[2rem] text-center border-dashed border-2">
                                <p className="text-gray-400 font-bold text-xs uppercase tracking-widest italic">No hay clases registradas para hoy.</p>
                            </div>
                        ) : (
                            <div className="space-y-4">
                                {schedule.map((clase, idx) => (
                                    <div key={idx} className="glass-panel p-6 rounded-3xl flex justify-between items-center hover:scale-[1.02] transition-transform shadow-md border-white/80">
                                        <div className="space-y-1">
                                            <p className="font-black text-gray-800 text-sm tracking-tight">{clase.materia}</p>
                                            <div className="flex items-center gap-2">
                                                <span className="bg-red-50 text-red-800 px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-tighter">
                                                    {clase.edificio}
                                                </span>
                                                <span className="text-gray-500 font-bold text-[10px] uppercase tracking-tighter">
                                                    Salón {clase.sala}
                                                </span>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <div className="header-gradient px-4 py-2 rounded-2xl text-white font-black text-[10px] shadow-lg">
                                                {clase.hora}
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
