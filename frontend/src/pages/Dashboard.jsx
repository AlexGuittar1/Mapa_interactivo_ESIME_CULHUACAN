import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getSchedule, updateUser } from '../services/api';
import { useNotifications } from '../context/NotificationContext';
import esimeLogo from '../assets/esime-logo.png';
import campanaIcon from '../assets/campana.png';

const Dashboard = () => {
    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [schedule, setSchedule] = useState([]);
    const [loading, setLoading] = useState(true);
    const [updatingVehicle, setUpdatingVehicle] = useState(false);
    const [currentTime, setCurrentTime] = useState(new Date());
    const [showNotifications, setShowNotifications] = useState(false);
    const { setSchedule: setContextSchedule, notifications } = useNotifications();

    useEffect(() => {
        const timer = setInterval(() => setCurrentTime(new Date()), 60000);
        return () => clearInterval(timer);
    }, []);

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
                setContextSchedule(data);
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
            localStorage.setItem('user', JSON.stringify(updatedUser)); // ACTUALIZA EL ALMACENAMIENTO LOCAL
        } catch (err) {
            alert("No se pudo actualizar el transporte.");
        } finally {
            setUpdatingVehicle(false);
        }
    };

    if (!user) return null;

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col font-sans overflow-y-auto">
            {/* --- ENCABEZADO --- */}
            <div className="bg-[#8B0000] px-4 pt-10 pb-6 lg:pb-8 flex justify-between items-center rounded-b-[2rem] lg:rounded-b-[3rem] shadow-2xl relative z-10 border-b border-red-900/30 shrink-0">
                <div className="flex items-center gap-3 lg:ml-8">
                    {/* LOGOTIPO / ICONO A LA IZQUIERDA */}
                    <div className="w-12 h-12 lg:w-16 lg:h-16 relative">
                        <img src={esimeLogo} alt="Logo" className="w-full h-full object-contain drop-shadow-lg" />
                    </div>
                    <h1 className="text-white font-bold text-lg lg:text-2xl tracking-wide">MI PERFIL</h1>
                </div>
                <div className="flex items-center gap-3 lg:mr-8 relative">
                    {/* ICONO DE CAMPANA DE NOTIFICACIONES */}
                    <button
                        onClick={() => setShowNotifications(!showNotifications)}
                        className="bg-[#b91c1c] text-white p-2.5 lg:p-3 rounded-full shadow-md hover:bg-red-700 transition-colors border border-white/10 relative flex justify-center items-center"
                    >
                        <img src={campanaIcon} alt="Notificaciones" className="w-5 h-5 object-contain invert brightness-0" />
                        {notifications.length > 0 && (
                            <span className="absolute -top-1 -right-1 bg-white text-[#8B0000] text-[8px] font-black w-4 h-4 flex items-center justify-center rounded-full shadow-sm">
                                {notifications.length}
                            </span>
                        )}
                    </button>

                    {/* MENU DESPLEGABLE DE NOTIFICACIONES */}
                    {showNotifications && (
                        <div className="absolute top-14 right-0 mt-2 w-72 bg-white rounded-2xl shadow-2xl border border-gray-100 overflow-hidden z-50 animate-slide-down origin-top-right">
                            <div className="bg-gray-50 px-4 py-3 border-b border-gray-100 flex justify-between items-center">
                                <h4 className="font-extrabold text-sm text-gray-800 uppercase tracking-widest">Notificaciones</h4>
                                <span className="text-xs font-bold bg-red-100 text-[#8B0000] px-2 py-0.5 rounded-full">{notifications.length} nuevas</span>
                            </div>
                            <div className="max-h-64 overflow-y-auto custom-scrollbar">
                                {notifications.length === 0 ? (
                                    <div className="p-6 text-center text-gray-400 text-xs font-bold uppercase tracking-wider">
                                        Sin notificaciones
                                    </div>
                                ) : (
                                    notifications.map((notif, idx) => (
                                        <div key={idx} className="p-4 border-b border-gray-50 last:border-0 hover:bg-gray-50 transition-colors">
                                            <p className="text-black font-bold text-xs mb-1">{notif.title}</p>
                                            <div className="flex items-center justify-between mt-2">
                                                <span className="text-gray-500 text-[10px] uppercase font-bold">Salón {notif.salon}</span>
                                                <button
                                                    onClick={() => navigate('/map', { state: { room: notif.salon } })}
                                                    className="text-[#8B0000] text-[10px] uppercase font-extrabold hover:underline"
                                                >
                                                    Ir al mapa →
                                                </button>
                                            </div>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>
                    )}

                    <button
                        onClick={() => navigate('/map')}
                        className="bg-[#b91c1c] text-[10px] lg:text-xs font-bold text-white px-4 lg:px-6 py-2.5 lg:py-3 rounded-full shadow-md hover:bg-red-700 transition-colors uppercase tracking-wider border border-white/10"
                    >
                        Volver al Mapa
                    </button>
                </div>
            </div>

            {/* --- CONTENIDO PRINCIPAL (TARJETA BLANCA) --- */}
            <div className="flex-1 bg-white mx-0 sm:mx-4 lg:mx-auto -mt-6 lg:-mt-6 lg:mb-6 rounded-t-[2.5rem] sm:rounded-[2.5rem] pt-12 lg:pt-12 px-6 lg:px-10 pb-8 shadow-2xl z-0 overflow-visible flex flex-col lg:flex-row max-w-6xl w-full self-center mb-0 sm:mb-4 gap-8">

                {/* --- COLUMNA 1: INFORMACION DE USUARIO Y TRANSPORTE --- */}
                <div className="flex flex-col items-center lg:items-start lg:w-1/3 shrink-0 lg:h-full lg:overflow-y-auto custom-scrollbar lg:pr-6">
                    <div className="w-24 h-24 lg:w-32 lg:h-32 bg-[#8B0000] rounded-full flex items-center justify-center border-4 border-gray-100 mb-4 shadow-xl">
                        <span className="text-4xl lg:text-5xl text-white font-black">{user.nombre.charAt(0)}</span>
                    </div>

                    <h2 className="text-lg lg:text-xl font-black text-center lg:text-left text-black leading-tight mb-1 uppercase w-full">
                        {user.nombre}
                    </h2>
                    <p className="text-[10px] lg:text-[11px] font-bold text-[#b91c1c] uppercase tracking-[0.10em] mb-6 lg:mb-8 text-center lg:text-left w-full">
                        {user.carrera || "Ingeniería en Computación"}
                    </p>

                    <div className="text-center lg:text-left mb-6 lg:mb-8 w-full shrink-0">
                        <p className="text-[10px] lg:text-[11px] font-extrabold text-black uppercase tracking-wider mb-1">
                            Boleta
                        </p>
                        <p className="text-lg font-bold text-gray-800 tracking-wide">
                            {user.boleta}
                        </p>
                    </div>

                    <div className="text-center lg:text-left w-full shrink-0 mb-6 lg:mb-auto">
                        <p className="text-[10px] lg:text-[11px] font-extrabold text-black uppercase tracking-wider mb-3">
                            Transporte
                        </p>

                        <div className="flex flex-wrap justify-center lg:justify-start gap-2">
                            {vehicleOptions.map((opt) => (
                                <button
                                    key={opt.id}
                                    onClick={() => handleVehicleChange(opt.id)}
                                    disabled={updatingVehicle}
                                    className={`
                                        flex items-center gap-1.5 px-4 py-2 rounded-full text-[10px] lg:text-[11px] font-bold transition-all border
                                        ${user.vehiculo === opt.id
                                            ? 'bg-[#8B0000] text-white border-[#8B0000] shadow-md'
                                            : 'bg-white text-black border-gray-200 hover:bg-gray-50 hover:shadow-sm'}
                                    `}
                                >
                                    <span>{opt.icon}</span>
                                    {opt.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* BOTON DE CERRAR SESION (ESCRITORIO: COLUMNA IZQUIERDA, MOVIL: ABAJO) */}
                    <div className="hidden lg:block w-full mt-6 pt-6 border-t border-gray-100 shrink-0">
                        <button
                            onClick={() => {
                                localStorage.removeItem('user');
                                navigate('/');
                            }}
                            className="w-full bg-gradient-to-r from-[#b30000] to-[#8B0000] text-white py-3 px-6 rounded-xl font-bold text-sm shadow-lg hover:shadow-xl hover:-translate-y-0.5 transition-all duration-200 flex items-center justify-center gap-2"
                        >
                            <span>🚪</span>
                            Cerrar Sesión
                        </button>
                    </div>
                </div>

                {/* --- COLUMNA 2: SECCION DE HORARIO ESCOLAR --- */}
                <div className="flex-1 flex flex-col min-h-0 w-full h-full lg:border-l lg:border-gray-100 lg:pl-8">
                    <div className="flex items-center gap-2 mb-4 shrink-0">
                        <div className="w-1.5 h-5 lg:h-6 bg-[#8B0000] rounded-full"></div>
                        <h3 className="font-black text-gray-900 text-sm lg:text-base uppercase tracking-wider">
                            Materias Inscritas
                        </h3>
                    </div>

                    {/* LISTA DE ELEMENTOS DESPLAZABLE */}
                    <div className="flex-1 overflow-y-auto overflow-x-hidden space-y-4 pr-2 lg:pr-4 custom-scrollbar pb-4 block">
                        {loading ? (
                            <div className="flex justify-center p-8">
                                <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-red-700"></div>
                            </div>
                        ) : schedule.length === 0 ? (
                            <div className="text-center py-10 border-2 border-dashed border-gray-200 rounded-2xl bg-gray-50">
                                <p className="text-gray-500 text-sm font-bold uppercase tracking-wider">Sin clases hoy</p>
                            </div>
                        ) : (
                            (() => {
                                const parseTime = (timeStr) => {
                                    if (!timeStr) return new Date();
                                    const [hours, minutes] = timeStr.split(':').map(Number);
                                    const d = new Date();
                                    d.setHours(hours, minutes, 0, 0);
                                    return d;
                                };

                                const sortedSchedule = [...schedule].sort((a, b) => parseTime(a.hora_inicio) - parseTime(b.hora_inicio));

                                return sortedSchedule.map((clase, idx) => {
                                    const start = parseTime(clase.hora_inicio);
                                    // ASUMIENDO 1H 30M SI HORA_FIN VINIERA VACIA O NO EXISTE, DE LO CONTRARIO LO TOMAMOS REAL
                                    const end = clase.hora_fin ? parseTime(clase.hora_fin) : new Date(start.getTime() + 90 * 60000);

                                    let statusClasses = "border-gray-100 shadow-sm hover:shadow-md hover:border-red-100";
                                    let badge = null;

                                    if (currentTime > end) {
                                        // FINALIZADA
                                        statusClasses = "opacity-50 border-gray-100";
                                    } else if (currentTime >= start && currentTime <= end) {
                                        // EN CURSO
                                        statusClasses = "border-green-500 border-2 shadow-md relative";
                                        badge = (
                                            <span className="absolute -top-2 left-6 bg-green-500 text-white text-[9px] font-black uppercase px-3 py-1 rounded-full shadow-sm tracking-wider z-10">
                                                En curso
                                            </span>
                                        );
                                    }

                                    return (
                                        <div key={idx} className={`bg-white rounded-[1.5rem] border p-4 lg:p-6 flex items-center justify-between transition-all cursor-default group relative mt-2 ${statusClasses}`}>
                                            {badge}
                                            <div className="flex flex-col gap-1.5">
                                                <h4 className="font-extrabold text-xs lg:text-sm text-black uppercase tracking-tight group-hover:text-[#8B0000] transition-colors">
                                                    {clase.materia}
                                                </h4>
                                                <div className="flex items-center gap-2">
                                                    <span className="text-gray-500 text-[10px] lg:text-xs font-bold uppercase tracking-wider flex items-center gap-1">
                                                        <svg className="w-3 h-3 text-[#8B0000]" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd"></path></svg>
                                                        SALÓN {clase.salon || 'Por asignar'}
                                                    </span>
                                                </div>
                                            </div>

                                            <div className="bg-[#8B0000] text-white text-[10px] lg:text-xs font-black px-4 py-2 lg:px-5 lg:py-2.5 rounded-xl shadow-md whitespace-nowrap tracking-wider">
                                                {String(clase.hora_inicio).substring(0, 5)}
                                            </div>
                                        </div>
                                    );
                                });
                            })()
                        )}
                    </div>

                    {/* BOTON DE CERRAR SESION (MOVIL: FINAL DE COLUMNA 2) */}
                    <div className="lg:hidden mt-4 pt-4 border-t border-gray-100 shrink-0">
                        <button
                            onClick={() => {
                                localStorage.removeItem('user');
                                navigate('/');
                            }}
                            className="w-full bg-gradient-to-r from-[#b30000] to-[#8B0000] text-white py-3.5 px-6 rounded-xl font-bold text-sm shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2"
                        >
                            <span>🚪</span>
                            Cerrar Sesión
                        </button>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default Dashboard;
