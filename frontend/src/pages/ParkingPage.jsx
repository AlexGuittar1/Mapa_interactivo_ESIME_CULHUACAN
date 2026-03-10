import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, ChevronLeft, ChevronRight, CalendarClock, X } from 'lucide-react';
import './ParkingPage.css';

// COMPONENTE SVG PARA EL COCHE (VISTA SUPERIOR)
const CarSvg = ({ horizontal = false }) => (
    <svg
        width="44"
        height="90"
        viewBox="0 0 40 80"
        xmlns="http://www.w3.org/2000/svg"
        className={`transition-transform duration-300 ${horizontal ? 'rotate-90' : ''}`}
        style={{ filter: 'drop-shadow(0px 10px 15px rgba(0,0,0,0.15))' }}
    >
        <rect x="2" y="4" width="36" height="74" rx="10" fill="rgba(0,0,0,0.1)" />
        <rect x="4" y="2" width="32" height="76" rx="12" fill="#ffffff" stroke="#e5e7eb" strokeWidth="1" />
        <path d="M 8 20 Q 20 16 32 20 L 30 28 L 10 28 Z" fill="#1f2937" />
        <path d="M 10 60 L 30 60 L 28 66 Q 20 68 12 66 Z" fill="#1f2937" />
        <rect x="10" y="28" width="20" height="32" rx="4" fill="#f9fafb" stroke="#e5e7eb" strokeWidth="0.5" />
        <rect x="2" y="24" width="4" height="6" rx="2" fill="#ffffff" stroke="#d1d5db" strokeWidth="1" />
        <rect x="34" y="24" width="4" height="6" rx="2" fill="#ffffff" stroke="#d1d5db" strokeWidth="1" />
        <rect x="8" y="3" width="6" height="3" rx="1" fill="#fef08a" />
        <rect x="26" y="3" width="6" height="3" rx="1" fill="#fef08a" />
        <rect x="8" y="74" width="8" height="3" rx="1" fill="#ef4444" />
        <rect x="24" y="74" width="8" height="3" rx="1" fill="#ef4444" />
    </svg>
);

import ParkingSectionMap from '../components/ParkingSectionMap';

const ParkingPage = () => {
    const navigate = useNavigate();
    const [sections, setSections] = useState([]);
    const [selectedSectionId, setSelectedSectionId] = useState(null);
    const [loading, setLoading] = useState(true);
    const [actionSpace, setActionSpace] = useState(null);
    const [isUpdating, setIsUpdating] = useState(false);
    const [expiredPrompt, setExpiredPrompt] = useState(null);
    const [expiringWarningPrompt, setExpiringWarningPrompt] = useState(null);
    const [user, setUser] = useState(null);

    const API_URL = import.meta.env.PROD
        ? "https://navcamp-backend.onrender.com"
        : "http://localhost:5001";

    // CONFIGURACION GPS GLOBAL
    const PARKING_CENTER = { lat: 19.329500, lng: -99.111400 };
    const MAX_RESERVATION_DISTANCE = 1500;

    // CONFIGURACION GPS PARA SECCIONES
    const PARKING_SECTIONS_COORDS = {
        'Sección 1': { lat: 19.329415, lng: -99.111664 },
        'Sección 2': { lat: 19.329622, lng: -99.111354 },
        'Sección 3': { lat: 19.329827, lng: -99.110991 },
        'Sección 4': { lat: 19.329246, lng: -99.111603 },
    };
    const OCCUPY_MAX_DISTANCE = 50;

    const haversineDistance = (coords1, coords2) => {
        const R = 6371000; // RADIO DE LA TIERRA EN METROS
        const lat1 = coords1.lat * Math.PI / 180;
        const lat2 = coords2.lat * Math.PI / 180;
        const dLat = (coords2.lat - coords1.lat) * Math.PI / 180;
        const dLon = (coords2.lng - coords1.lng) * Math.PI / 180;

        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1) * Math.cos(lat2) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    };

    useEffect(() => {
        const userStr = localStorage.getItem('user');
        if (userStr) {
            setUser(JSON.parse(userStr));
        } else {
            navigate('/login');
        }
    }, [navigate]);

    useEffect(() => {
        fetchParkingData();
        const interval = setInterval(fetchParkingData, 10000); // CONSULTA PERIODICA CADA 10 SEGUNDOS
        return () => clearInterval(interval);
    }, []);

    const fetchParkingData = async (retries = 3) => {
        try {
            const res = await fetch(`${API_URL}/api/parking/spaces`);
            const data = await res.json();
            setSections(data.sections || []);

            // SI ES LA PRIMERA CARGA, SELECCIONAMOS LA PRIMERA SECCION AUTOMATICAMENTE
            if (data.sections && data.sections.length > 0) {
                setSelectedSectionId(prev => prev === null ? data.sections[0].id : prev);
            }

            setLoading(false);
        } catch (error) {
            console.error('Error fetching parking data:', error);
            if (retries > 0) {
                console.log(`Reintentando... (${retries} intentos restantes)`);
                setTimeout(() => fetchParkingData(retries - 1), 3000);
            } else {
                setLoading(false);
            }
        }
    };

    // VERIFICACION GLOBAL DE EXPIRACIONES DE RESERVA
    useEffect(() => {
        const checkExpirations = setInterval(() => {
            if (!user) return;
            const now = new Date().getTime();
            sections.forEach(sec => {
                sec.spaces.forEach(space => {
                    if (space.status === 'reserved' && space.reserved_by === user.boleta && space.reservation_expires_at) {
                        const diff = new Date(space.reservation_expires_at).getTime() - now;

                        if (diff <= 0) {
                            if (expiredPrompt?.id !== space.id) {
                                setExpiredPrompt(space);
                                setExpiringWarningPrompt(null);
                                setActionSpace(null);
                            }
                        } else if (diff <= 60000) {
                            if (expiringWarningPrompt?.id !== space.id && expiredPrompt?.id !== space.id) {
                                setExpiringWarningPrompt(space);
                            }
                        }
                    }
                });
            });
        }, 1000);
        return () => clearInterval(checkExpirations);
    }, [sections, user, expiredPrompt, expiringWarningPrompt]);

    const updateSpaceStatus = async (spaceId, newStatus) => {
        setIsUpdating(true);

        const doUpdate = async (userCoords = null) => {
            try {
                // Construir cuerpo de la peticion incluyendo coordenadas GPS si estan disponibles
                const requestBody = { status: newStatus, user_boleta: user?.boleta };
                if (userCoords) {
                    requestBody.user_lat = userCoords.lat;
                    requestBody.user_lng = userCoords.lng;
                }

                const res = await fetch(`${API_URL}/api/parking/spaces/${spaceId}/status`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestBody)
                });
                const data = await res.json();

                if (res.ok) {
                    if (newStatus === 'occupied' && userCoords) {
                        const miCoche = { ...userCoords, name: "Lugar de estacionamiento", spaceId };
                        localStorage.setItem("mi_coche_gps", JSON.stringify(miCoche));
                    } else if (newStatus === 'available') {
                        localStorage.removeItem("mi_coche_gps");
                    }
                    await fetchParkingData();
                    setActionSpace(null);
                    setExpiredPrompt(null);
                    setExpiringWarningPrompt(null);
                } else {
                    alert(data.error || "Ocurrió un error al actualizar el espacio.");
                }
            } catch (error) {
                console.error("Error updating status:", error);
                alert("No se pudo conectar con el servidor.");
            } finally {
                setIsUpdating(false);
            }
        };

        if (newStatus === 'reserved' || newStatus === 'occupied') {
            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const userCoords = { lat: position.coords.latitude, lng: position.coords.longitude };

                        // VALIDACIONES DE GEOFENCES PREVIAS A LA LLAMADA A LA API
                        if (newStatus === 'reserved') {
                            // RESERVAR: Debe estar a menos de 1.5 km del estacionamiento general
                            const distance = haversineDistance(userCoords, PARKING_CENTER);
                            if (distance > MAX_RESERVATION_DISTANCE) {
                                alert("Debes estar a menos de 1.5 km del estacionamiento para poder reservar un lugar.\nNo es posible utilizar esta función desde tu ubicación actual.");
                                setIsUpdating(false);
                                return;
                            }
                        } else if (newStatus === 'occupied') {
                            // OCUPAR: Debe estar a menos de 50m de la sección específica
                            let targetSectionName = null;
                            for (const sec of sections) {
                                if (sec.spaces.some(s => s.id === spaceId)) {
                                    targetSectionName = sec.name;
                                    break;
                                }
                            }
                            if (targetSectionName && PARKING_SECTIONS_COORDS[targetSectionName]) {
                                const secCoords = PARKING_SECTIONS_COORDS[targetSectionName];
                                const distanceToSection = haversineDistance(userCoords, secCoords);
                                if (distanceToSection > OCCUPY_MAX_DISTANCE) {
                                    alert(`Debes estar a menos de 50 metros de ${targetSectionName} para marcar este espacio como ocupado.\nNo es posible utilizar esta función desde tu ubicación actual.`);
                                    setIsUpdating(false);
                                    return;
                                }
                            }
                        }

                        // TODO VALIDO, EJECUTAR RESERVA U OCUPACION CON COORDENADAS
                        doUpdate(userCoords);
                    },
                    (error) => {
                        alert("No se pudo obtener tu ubicación. Activa tu GPS para usar este servicio.");
                        setIsUpdating(false);
                    },
                    { timeout: 10000, enableHighAccuracy: true }
                );
            } else {
                alert("Tu navegador no soporta geolocalización. Necesaria para estaciones.");
                setIsUpdating(false);
            }
        } else {
            // LIBERAR NO EVALUA UBICACION
            doUpdate();
        }
    };

    // COMPONENTE INDIVIDUAL DE ESPACIO CON TEMPORIZADOR INDEPENDIENTE
    const SpaceCard = ({ space }) => {
        const [timeLeft, setTimeLeft] = useState(null);

        useEffect(() => {
            if (space.status === 'reserved' && space.reservation_expires_at) {
                const interval = setInterval(() => {
                    // NOTA: ASUMIENDO QUE PYTHON MANDA FECHAS COMO NAIVE DATETIME EN ZONA HORARIA LOCAL
                    const expiresStr = space.reservation_expires_at;
                    const expires = new Date(expiresStr).getTime();
                    const now = new Date().getTime();
                    const diff = expires - now;

                    if (diff <= 0) {
                        clearInterval(interval);
                        setTimeLeft(0);
                        // EL MODAL DE EXPIRADO SE MANEJA EN EL HOOK GLOBAL DE VERIFICACION
                    } else {
                        setTimeLeft(Math.floor(diff / 1000));
                    }
                }, 1000);
                return () => clearInterval(interval);
            } else {
                setTimeLeft(null);
            }
        }, [space]); // LAS DEPENDENCIAS COMPLETAS NO SON NECESARIAS REPETIDAMENTE

        const formatTime = (seconds) => {
            if (seconds === null) return "";
            const m = Math.floor(seconds / 60);
            const s = seconds % 60;
            return `${m}:${s < 10 ? '0' : ''}${s}`;
        };

        const isMine = space.reserved_by === user?.boleta || space.occupied_by === user?.boleta;

        // MANEJADOR DEL CLIC PARA ABRIR ACCIONES LOGICAS PERMITIDAS
        const handleClick = () => {
            if (space.status === 'available') setActionSpace(space);
            if (isMine) setActionSpace(space);
            if (space.status === 'occupied' && !isMine) {
                // NO HACER NADA AL DAR CLIC EN EL COCHE DE OTRO USUARIO
            }
        };

        let bgColor = 'bg-white hover:border-green-300 hover:shadow-lg cursor-pointer';
        let content = <div className="bg-[#10b981] text-white px-3 py-1.5 rounded-lg font-black text-sm tracking-widest shadow-md">LIBRE</div>;

        if (space.status === 'reserved') {
            bgColor = isMine ? 'bg-amber-100 border-amber-300 shadow-md cursor-pointer' : 'bg-gray-100 opacity-70 cursor-not-allowed';
            content = (
                <div className="flex flex-col items-center gap-2">
                    <CalendarClock className={`w-8 h-8 ${isMine ? 'text-amber-600' : 'text-gray-400'}`} strokeWidth={2} />
                    {isMine && timeLeft !== null && (
                        <span className="font-extrabold text-amber-800 bg-amber-200 px-2 py-0.5 rounded-full text-xs shadow-inner">
                            {formatTime(timeLeft)}
                        </span>
                    )}
                </div>
            );
        } else if (space.status === 'occupied') {
            bgColor = isMine ? 'bg-red-100 border-red-300 shadow-md cursor-pointer' : 'bg-gray-100 opacity-60 cursor-not-allowed';
            content = <CarSvg horizontal={false} />;
        }

        return (
            <div
                onClick={handleClick}
                className={`w-full max-w-[120px] aspect-[2/3] rounded-[1.5rem] flex flex-col items-center justify-between py-4 border border-gray-200 outline-none transition-all ${bgColor}`}
            >
                <div className="w-full px-2 flex justify-between items-center -mt-2">
                    <span className="font-extrabold text-xs tracking-wider text-gray-700">{space.space_number}</span>
                    {isMine && <span className="w-2 h-2 rounded-full bg-blue-500 shadow-sm shadow-blue-300"></span>}
                </div>
                <div className="flex-1 flex items-center justify-center w-full">
                    {content}
                </div>
            </div>
        );
    };

    // VARIABLES CICLICAS DE SECCION
    const activeSection = sections.find(s => s.id === selectedSectionId) || null;
    const activeSpaces = activeSection?.spaces || [];

    const handleNextSection = () => {
        const currIdx = sections.findIndex(s => s.id === selectedSectionId);
        if (currIdx < sections.length - 1) setSelectedSectionId(sections[currIdx + 1].id);
    };
    const handlePrevSection = () => {
        const currIdx = sections.findIndex(s => s.id === selectedSectionId);
        if (currIdx > 0) setSelectedSectionId(sections[currIdx - 1].id);
    };

    // Auto-scroll selected tab into view
    const tabsContainerRef = useRef(null);
    useEffect(() => {
        if (tabsContainerRef.current && selectedSectionId) {
            const activeBtn = tabsContainerRef.current.querySelector('[data-active="true"]');
            if (activeBtn) {
                activeBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
            }
        }
    }, [selectedSectionId]);



    return (
        <div className="h-dvh bg-gray-50 flex flex-col font-sans overflow-hidden">

            {/* --- ENCABEZADO --- */}
            <div className="pt-12 pb-6 px-6 flex flex-col items-center relative shrink-0">
                <button
                    onClick={() => navigate('/map')}
                    className="absolute left-6 top-12 bg-white w-12 h-12 rounded-full shadow-lg flex items-center justify-center transform transition-transform hover:-translate-x-1"
                >
                    <ArrowLeft className="w-6 h-6 text-black" />
                </button>
                <h1 className="font-black text-2xl tracking-tighter uppercase text-black mt-2">
                    Estacionamiento
                </h1>
                <p className="font-semibold text-xs tracking-widest uppercase text-gray-500 mt-1">
                    Disponibilidad
                </p>
            </div>

            {/* --- NAVEGADOR DE SECCIONES (MEJORADO Y DESPLAZABLE) --- */}
            <div className="px-4 sm:px-6 shrink-0 z-10 w-full mt-2 flex justify-center w-full max-w-full">
                <div className="bg-white shadow-2xl shadow-gray-200/60 rounded-[2.5rem] p-2 sm:p-3 flex items-center w-full sm:w-fit sm:max-w-[calc(100vw-3rem)] lg:max-w-full mx-auto border border-gray-100 relative overflow-hidden">

                    {/* BOTON ANTERIOR */}
                    <button onClick={handlePrevSection} className="p-2 sm:p-3 bg-gray-50 rounded-full text-gray-500 hover:text-black hover:bg-gray-100 transition-all disabled:opacity-30 shrink-0 shadow-sm" disabled={!sections.length || sections[0]?.id === selectedSectionId}>
                        <ChevronLeft className="w-5 h-5 sm:w-6 sm:h-6" />
                    </button>

                    {/* CONTENEDOR CON DESPLAZAMIENTO FLUIDO */}
                    <div ref={tabsContainerRef} className="flex-1 overflow-x-auto no-scrollbar scroll-smooth mx-1 sm:mx-2 flex items-center gap-1.5 sm:gap-3 px-1 sm:px-2 min-w-0 pointer-events-auto touch-pan-x">
                        {sections.map(sec => (
                            <button
                                key={sec.id}
                                data-active={selectedSectionId === sec.id}
                                onClick={() => setSelectedSectionId(sec.id)}
                                className={`px-3 py-1.5 sm:px-6 sm:py-3.5 rounded-full whitespace-nowrap text-xs sm:text-base font-black transition-all duration-300 shrink-0 ${selectedSectionId === sec.id
                                    ? 'bg-gradient-to-r from-[#b30000] to-[#800000] text-white shadow-xl shadow-red-900/20 scale-100 ring-2 ring-red-100 ring-offset-2'
                                    : 'text-gray-500 bg-gray-50 hover:bg-gray-100 hover:text-gray-800'
                                    }`}
                            >
                                {sec.name}
                            </button>
                        ))}
                    </div>

                    {/* BOTON SIGUIENTE */}
                    <button onClick={handleNextSection} className="p-2 sm:p-3 bg-gray-50 rounded-full text-gray-500 hover:text-black hover:bg-gray-100 transition-all disabled:opacity-30 shrink-0 shadow-sm" disabled={!sections.length || sections[sections.length - 1]?.id === selectedSectionId}>
                        <ChevronRight className="w-5 h-5 sm:w-6 sm:h-6" />
                    </button>
                </div>
            </div>

            {/* --- CONTENIDO DE INTERFAZ HIBRIDA --- */}
            <div className="flex-1 overflow-hidden mt-6 pb-24 w-full px-4 sm:px-8 max-w-[1600px] mx-auto flex flex-col lg:flex-row gap-6">

                {/* MAPA VISUAL (ARRIBA EN MOVIL, DERECHA EN ESCRITORIO) */}
                <div className="w-full lg:w-5/12 xl:w-1/3 shrink-0 h-[300px] lg:h-full lg:order-2">
                    <ParkingSectionMap section={activeSection} />
                </div>

                {/* CUADRICULA DE ESPACIOS (ABAJO EN MOVIL, IZQUIERDA EN ESCRITORIO CON DESPLAZAMIENTO) */}
                <div className="flex-1 overflow-y-auto custom-scrollbar lg:order-1 relative rounded-3xl bg-white/50 border border-gray-100 shadow-sm p-4 sm:p-6 backdrop-blur-sm">
                    {loading ? (
                        <div className="flex items-center justify-center h-full">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-red-700"></div>
                        </div>
                    ) : (
                        <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 xl:grid-cols-6 gap-4 sm:gap-6 justify-items-center auto-rows-max w-full">
                            {activeSpaces.map((space) => (
                                <SpaceCard key={space.id} space={space} />
                            ))}
                        </div>
                    )}
                </div>

            </div>

            {/* MODAL DE ACCIONES / HOJA INFERIOR PARA ACCIONES REGULARES */}
            {actionSpace && !expiredPrompt && (
                <div className="absolute inset-0 z-50 flex items-end sm:items-center justify-center bg-black/50 backdrop-blur-sm" onClick={() => setActionSpace(null)}>
                    <div
                        className="bg-white w-full max-w-md sm:rounded-[2rem] rounded-t-[2rem] p-6 shadow-2xl transform transition-transform animate-slideUp sm:animate-none"
                        onClick={e => e.stopPropagation()}
                    >
                        <div className="flex justify-between items-center mb-6">
                            <div>
                                <h3 className="font-black text-xl text-gray-900 flex items-center gap-2">
                                    Cajón {actionSpace.space_number}
                                    {actionSpace.status === 'available' && <span className="bg-green-100 text-green-700 text-xs px-2 py-0.5 rounded-full uppercase tracking-wider">Libre</span>}
                                    {actionSpace.status === 'reserved' && <span className="bg-amber-100 text-amber-700 text-xs px-2 py-0.5 rounded-full uppercase tracking-wider">Tu Reserva</span>}
                                    {actionSpace.status === 'occupied' && <span className="bg-red-100 text-red-700 text-xs px-2 py-0.5 rounded-full uppercase tracking-wider">Tu Auto</span>}
                                </h3>
                                <p className="text-sm font-bold text-gray-500 mt-1">
                                    {actionSpace.status === 'available' ? 'Reserva por 10 mins o marcalo como ocupado directamente.' :
                                        actionSpace.status === 'reserved' ? '¿Ya llegaste a tu lugar u ocupaste otro?' :
                                            '¿Te retiras del campus?'}
                                </p>
                            </div>
                            <button onClick={() => setActionSpace(null)} className="p-2 bg-gray-100 rounded-full hover:bg-gray-200">
                                <X className="w-5 h-5 text-gray-600" />
                            </button>
                        </div>

                        <div className="flex flex-col gap-4 mb-2">
                            {actionSpace.status === 'available' && (
                                <>
                                    <button disabled={isUpdating} onClick={() => updateSpaceStatus(actionSpace.id, 'reserved')}
                                        className="w-full flex items-center justify-center gap-3 bg-amber-500 hover:bg-amber-600 text-white font-black py-4 rounded-2xl shadow-md transition-colors disabled:opacity-50">
                                        Reservar (10 minutos)
                                    </button>
                                    <button disabled={isUpdating} onClick={() => updateSpaceStatus(actionSpace.id, 'occupied')}
                                        className="w-full flex items-center justify-center gap-3 bg-red-600 hover:bg-red-700 text-white font-black py-4 rounded-2xl shadow-md transition-colors disabled:opacity-50">
                                        Llegué directamente (Ocupar)
                                    </button>
                                </>
                            )}

                            {actionSpace.status === 'reserved' && (
                                <>
                                    <button disabled={isUpdating} onClick={() => updateSpaceStatus(actionSpace.id, 'occupied')}
                                        className="w-full flex items-center justify-center gap-3 bg-red-600 hover:bg-red-700 text-white font-black py-4 rounded-2xl shadow-md transition-colors disabled:opacity-50">
                                        ¡Ya estacioné mi coche!
                                    </button>
                                    <button disabled={isUpdating} onClick={() => updateSpaceStatus(actionSpace.id, 'available')}
                                        className="w-full flex items-center justify-center gap-3 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 rounded-2xl shadow-sm transition-colors disabled:opacity-50">
                                        Cancelar reserva (liberar)
                                    </button>
                                </>
                            )}

                            {actionSpace.status === 'occupied' && (
                                <>
                                    <button disabled={isUpdating} onClick={() => updateSpaceStatus(actionSpace.id, 'available')}
                                        className="w-full flex items-center justify-center gap-3 bg-[#10b981] hover:bg-[#059669] text-white font-black py-4 rounded-2xl shadow-md transition-colors disabled:opacity-50">
                                        Liberar Espacio (Me voy)
                                    </button>
                                    <p className="text-center text-xs text-gray-400 font-medium px-4">
                                        Nota: Si liberas el espacio se te bloqueará la reserva de este mismo cajón durante 1 hora.
                                    </p>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* MODAL DE AVISO DE EXPIRACION */}
            {expiredPrompt && (
                <div className="absolute inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-md px-4" onClick={(e) => e.stopPropagation()}>
                    <div className="bg-white w-full max-w-sm rounded-3xl p-6 shadow-2xl flex flex-col items-center animate-pop" onClick={e => e.stopPropagation()}>
                        <div className="w-16 h-16 bg-red-100 text-red-600 rounded-full flex items-center justify-center mb-4">
                            <CalendarClock className="w-8 h-8" />
                        </div>
                        <h2 className="text-xl font-black text-center text-gray-900 mb-2">¡Tu reserva expiró!</h2>
                        <p className="text-center text-gray-600 font-medium mb-8">
                            El tiempo de gracia de 10 minutos para llegar al cajón <b>{expiredPrompt.space_number}</b> ha concluido. <br /><br />¿Ya te encuentras estacionado aquí físicamente?
                        </p>
                        <div className="flex gap-4 w-full">
                            <button disabled={isUpdating} onClick={() => updateSpaceStatus(expiredPrompt.id, 'available')}
                                className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-3 rounded-xl transition-colors">
                                NO
                            </button>
                            <button disabled={isUpdating} onClick={() => updateSpaceStatus(expiredPrompt.id, 'occupied')}
                                className="flex-1 bg-red-600 hover:bg-red-700 text-white font-black py-3 rounded-xl shadow-md shadow-red-500/30 transition-colors">
                                SÍ, LO OCUPÉ
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* MODAL DE ADVERTENCIA DE PROXIMA EXPIRACION */}
            {expiringWarningPrompt && !expiredPrompt && (
                <div className="absolute inset-0 z-[60] flex items-center justify-center bg-black/60 backdrop-blur-md px-4" onClick={(e) => e.stopPropagation()}>
                    <div className="bg-white w-full max-w-sm rounded-3xl p-6 shadow-2xl flex flex-col items-center animate-pop" onClick={e => e.stopPropagation()}>
                        <div className="w-16 h-16 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center mb-4">
                            <CalendarClock className="w-8 h-8" />
                        </div>
                        <h2 className="text-xl font-black text-center text-gray-900 mb-2">¡Tu reserva expira pronto!</h2>
                        <p className="text-center text-gray-600 font-medium mb-8">
                            Tienes menos de 1 minuto restante para llegar al cajón <b>{expiringWarningPrompt.space_number}</b>.<br /><br />
                            Marca el espacio como ocupado o libera la reserva.
                        </p>
                        <div className="flex flex-col gap-3 w-full">
                            <button disabled={isUpdating} onClick={() => updateSpaceStatus(expiringWarningPrompt.id, 'occupied')}
                                className="w-full bg-red-600 hover:bg-red-700 text-white font-black py-4 rounded-2xl shadow-md transition-colors disabled:opacity-50">
                                Marcar como ocupado
                            </button>
                            <button disabled={isUpdating} onClick={() => updateSpaceStatus(expiringWarningPrompt.id, 'available')}
                                className="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-4 rounded-2xl shadow-sm transition-colors disabled:opacity-50">
                                Liberar reserva
                            </button>
                        </div>
                    </div>
                </div>
            )}

        </div>
    );
};

export default ParkingPage;
