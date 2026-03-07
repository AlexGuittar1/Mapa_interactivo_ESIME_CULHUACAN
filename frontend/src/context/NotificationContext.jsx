import React, { createContext, useContext, useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import campanaIcon from '../assets/campana.png';

const NotificationContext = createContext();

export const useNotifications = () => useContext(NotificationContext);

export const NotificationProvider = ({ children }) => {
    const navigate = useNavigate();
    const [notifications, setNotifications] = useState([]);
    const [activePopup, setActivePopup] = useState(null);
    const [schedule, setSchedule] = useState([]);
    const timeoutRefs = useRef({});

    // PARSEADOR Y RECONSTRUCTOR DE HORAS "HH:MM"
    const parseTime = (timeStr) => {
        if (!timeStr) return new Date();
        const [hours, minutes] = timeStr.split(':').map(Number);
        const d = new Date();
        d.setHours(hours, minutes, 0, 0);
        return d;
    };

    // AGREGAR TICKET DE NOTIFICACION A LA BANDEJA SECUNDARIA
    const addNotification = (notif) => {
        setNotifications(prev => [notif, ...prev]);
        setActivePopup(notif);

        // AUTO-CERRAR POPUP NOTIFICADOR AL EXPIRAR 5 SEGUNDOS
        setTimeout(() => {
            setActivePopup(current => current?.id === notif.id ? null : current);
        }, 5000);
    };

    const clearActivePopup = () => setActivePopup(null);

    // CALCULAR EVENTUALIDADES DE NOTIFICACIONES BASADO EN CRONOGRAMA EN CURSO
    useEffect(() => {
        if (!schedule || schedule.length === 0) return;

        const checkAndSchedule = () => {
            const now = new Date();
            const currentDayNumber = now.getDay(); // 0 (Sun) to 6 (Sat)
            // TRADUCCION Y AJUSTE DE DIAS: ESQUEMA BD 1 = Lunes, 2 = Martes... 7 = Domingo
            const dbDayMap = { 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 0: 7 };
            const today = dbDayMap[currentDayNumber];

            schedule.forEach(clase => {
                // BLOQUEO: SOLO AUTORIZAR NOTIFICACION SI LA CLASE EMPAREJA EL DIA
                // (Si clase carece de especiaficacion dia_semana aplicamos comodin diario)
                if (clase.dia_semana && clase.dia_semana !== today) return;

                const startTime = parseTime(clase.hora_inicio);

                // IGNORAR CRONOGRAMAS Y CLASES CADUCADAS OCURRIDAS EN HORAS PASADAS
                if (now.getTime() >= startTime.getTime()) return;

                const timeUntilStart = startTime.getTime() - now.getTime();
                const claseId = `${clase.materia}-${clase.hora_inicio}`;

                // FILTRADO ESTRICTO DE ALCANCE CERCANO A INICIAR (15 MINUTOS A 0)
                // CANCELAR Y DEPURAR TIMEOUTS EVENTUALES PREVIAMENTE FIJADOS POR CLASE
                if (timeoutRefs.current[claseId]) {
                    clearTimeout(timeoutRefs.current[claseId]);
                }

                // PREPROGRAMAR EVENTO PARA DESPACHO JUST-IN-TIME DE INICIO
                // SI LA CLASE DEMORA MAS EN ESTE DIA, ENCOLAR EFECTIVAMENTE LA EMISION
                if (timeUntilStart > 0) {
                    timeoutRefs.current[claseId] = setTimeout(() => {
                        addNotification({
                            id: Date.now(),
                            title: `Tu clase de ${clase.materia} está comenzando.`,
                            materia: clase.materia,
                            salon: clase.salon,
                            timestamp: new Date().toISOString()
                        });
                    }, timeUntilStart);
                }
            });
        };

        // COMPILAR Y EJECUTAR CALCULADORA INICIAL
        checkAndSchedule();

        // REPETICION O FALLBACK CONTINGENTE: RE-EVALUAR CRONOGRAMA CADA 60 SEGUNDOS POR SI ACASO NAVEGADOR RECIBE SUSPENSION
        const fallbackInterval = setInterval(checkAndSchedule, 60000);

        return () => {
            clearInterval(fallbackInterval);
            Object.values(timeoutRefs.current).forEach(clearTimeout);
        };
    }, [schedule]);

    return (
        <NotificationContext.Provider value={{
            notifications,
            activePopup,
            clearActivePopup,
            setSchedule
        }}>
            {children}

            {/* INTERFAZ CENTRALIZADA DE VENTANA EMERGENTE DE NOTIFICACIONES */}
            {activePopup && (
                <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 bg-white border-l-4 border-[#8B0000] rounded-lg shadow-xl p-4 flex flex-col gap-2 w-11/12 max-w-sm animate-slide-down">
                    <div className="flex justify-between items-start">
                        <div className="flex items-center gap-2 text-[#8B0000] font-black uppercase text-sm">
                            <img src={campanaIcon} alt="Notificaciones" className="w-4 h-4 object-contain" /> Notificación
                        </div>
                        <button onClick={clearActivePopup} className="text-gray-400 hover:text-gray-600">
                            ✕
                        </button>
                    </div>
                    <p className="text-gray-800 font-bold text-sm">
                        {activePopup.title}
                    </p>
                    {activePopup.salon && (
                        <div className="mt-2 flex items-center justify-between">
                            <p className="text-gray-500 text-xs flex items-center gap-1 font-bold uppercase">
                                <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd"></path></svg>
                                Salón {activePopup.salon}
                            </p>
                            <button
                                onClick={() => {
                                    clearActivePopup();
                                    navigate('/map', { state: { room: activePopup.salon } });
                                }}
                                className="bg-[#8B0000] text-white text-xs font-bold px-3 py-1.5 rounded-md hover:bg-red-800 transition-colors shadow-sm"
                            >
                                Ir a mi salón
                            </button>
                        </div>
                    )}
                </div>
            )}
        </NotificationContext.Provider>
    );
};
