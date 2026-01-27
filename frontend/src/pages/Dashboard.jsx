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
            localStorage.setItem('user', JSON.stringify(updatedUser)); // Update local storage
        } catch (err) {
            alert("No se pudo actualizar el transporte.");
        } finally {
            setUpdatingVehicle(false);
        }
    };

    if (!user) return null;

    return (
        <div className="min-h-screen bg-black flex flex-col font-sans">
            {/* --- HEADER --- */}
            <div className="bg-[#8B0000] px-4 pt-12 pb-6 flex justify-between items-center rounded-b-[2rem] shadow-2xl relative z-10 border-b border-red-900/30">
                <div className="flex items-center gap-3">
                    {/* Logo/Icon on the left */}
                    <div className="w-12 h-12 relative">
                        <img src={esimeLogo} alt="Logo" className="w-full h-full object-contain drop-shadow-lg" />
                    </div>
                    <h1 className="text-white font-bold text-lg tracking-wide">MI PERFIL</h1>
                </div>
                <button
                    onClick={() => navigate('/map')}
                    className="bg-[#b91c1c] text-[10px] font-bold text-white px-4 py-2 rounded-full shadow-md hover:bg-red-700 transition-colors uppercase tracking-wider border border-white/10"
                >
                    Volver al Mapa
                </button>
            </div>

            {/* --- MAIN CONTENT (White Card) --- */}
            <div className="flex-1 bg-white mx-4 -mt-6 rounded-[2.5rem] pt-12 px-6 pb-20 shadow-2xl z-0 overflow-y-auto">

                {/* User Info */}
                <div className="flex flex-col items-center mb-10">
                    <div className="w-24 h-24 bg-[#8B0000] rounded-full flex items-center justify-center border-4 border-black mb-4 shadow-xl">
                        <span className="text-4xl text-white font-black">{user.nombre.charAt(0)}</span>
                        {/* Alternatively use a real user image if available */}
                    </div>

                    <h2 className="text-lg font-black text-center text-black leading-tight mb-1 uppercase max-w-[80%]">
                        {user.nombre}
                    </h2>
                    <p className="text-[10px] font-bold text-[#b91c1c] uppercase tracking-[0.15em] mb-8">
                        {user.carrera || "Ingeniería en Computación"}
                    </p>

                    <div className="text-center mb-8">
                        <p className="text-[10px] font-extrabold text-black uppercase tracking-wider mb-1">
                            Boleta
                        </p>
                        <p className="text-lg font-bold text-gray-800 tracking-wide">
                            {user.boleta}
                        </p>
                    </div>

                    <div className="text-center w-full">
                        <p className="text-[10px] font-extrabold text-black uppercase tracking-wider mb-3">
                            Transporte
                        </p>

                        <div className="flex flex-wrap justify-center gap-2">
                            {vehicleOptions.map((opt) => (
                                <button
                                    key={opt.id}
                                    onClick={() => handleVehicleChange(opt.id)}
                                    disabled={updatingVehicle}
                                    className={`
                                        flex items-center gap-1.5 px-4 py-2 rounded-full text-[10px] font-bold transition-all border
                                        ${user.vehiculo === opt.id
                                            ? 'bg-[#8B0000] text-white border-[#8B0000] shadow-md'
                                            : 'bg-white text-black border-gray-200 hover:bg-gray-50'}
                                    `}
                                >
                                    <span>{opt.icon}</span>
                                    {opt.label}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Schedule Section */}
                <div className="w-full">
                    <div className="flex items-center gap-2 mb-4">
                        <div className="w-1.5 h-5 bg-[#8B0000] rounded-full"></div>
                        <h3 className="font-black text-gray-900 text-sm uppercase tracking-wider">
                            Horario de Hoy
                        </h3>
                    </div>

                    <div className="space-y-4">
                        {loading ? (
                            <div className="flex justify-center p-4">
                                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-700"></div>
                            </div>
                        ) : schedule.length === 0 ? (
                            <div className="text-center py-6 border-2 border-dashed border-gray-200 rounded-2xl">
                                <p className="text-gray-400 text-xs font-bold uppercase">Sin clases hoy</p>
                            </div>
                        ) : (
                            schedule.map((clase, idx) => (
                                <div key={idx} className="bg-white rounded-[1.5rem] border border-gray-100 shadow-sm p-5 flex items-center justify-between hover:shadow-md transition-shadow">
                                    <div className="flex flex-col gap-1">
                                        <h4 className="font-extrabold text-xs text-black uppercase tracking-tight">
                                            {clase.materia}
                                        </h4>
                                        <div className="flex items-center gap-2">
                                            <span className="bg-red-100 text-red-800 text-[9px] font-black px-2 py-0.5 rounded-md uppercase">
                                                {clase.edificio?.replace('Edificio', 'EDIF')}
                                            </span>
                                            <span className="text-gray-500 text-[9px] font-bold uppercase">
                                                SALÓN {clase.sala}
                                            </span>
                                        </div>
                                    </div>

                                    <div className="bg-[#8B0000] text-white text-[10px] font-black px-3 py-1.5 rounded-xl shadow-lg whitespace-nowrap">
                                        {clase.hora}
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Dashboard;
