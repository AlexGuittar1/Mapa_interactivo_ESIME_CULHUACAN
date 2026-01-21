import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../authConfig";
import { login, checkEmail, completeProfile, register } from '../services/api';

const Login = () => {
    const navigate = useNavigate();
    const { instance } = useMsal();

    // Estados: LOGIN, REGISTER, COMPLETE_PROFILE
    const [view, setView] = useState('LOGIN');
    const [error, setError] = useState(null);

    // Login inputs
    const [boleta, setBoleta] = useState('');

    // Register/Profile inputs
    const [email, setEmail] = useState('');
    const [nombre, setNombre] = useState('');
    const [regBoleta, setRegBoleta] = useState('');
    const [carrera, setCarrera] = useState('Ingeniería en Sistemas Computacionales');
    const [vehiculo, setVehiculo] = useState('ninguno');

    const handleMicrosoftLogin = () => {
        setError(null);
        instance.loginPopup(loginRequest)
            .then(async (response) => {
                const msEmail = response.account.username;
                const msName = response.account.name;

                setEmail(msEmail);
                setNombre(msName); // Pre-fill name from Outlook

                // Verificar existencia
                try {
                    const check = await checkEmail(msEmail);
                    if (check.exists) {
                        localStorage.setItem('user', JSON.stringify(check.user));
                        navigate('/map');
                    } else {
                        setView('COMPLETE_PROFILE');
                    }
                } catch (err) {
                    setError("Error de conexión con el servidor");
                }
            })
            .catch(e => {
                console.error(e);
                setError("Error al autenticar con Microsoft");
            });
    };

    const handleBoletaLogin = async (e) => {
        e.preventDefault();
        setError(null);
        try {
            const user = await login(boleta);
            localStorage.setItem('user', JSON.stringify(user));
            navigate('/map');
        } catch (err) {
            setError("Usuario no encontrado, verifique su boleta o regístrese.");
        }
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setError(null);

        // Use validation logic if needed
        const payload = {
            boleta: regBoleta,
            nombre: nombre,
            email: email || `user_${regBoleta}@esime.mx`, // Email ficticio si es registro manual
            carrera,
            vehiculo
        };

        try {
            const newUser = await register(payload);
            localStorage.setItem('user', JSON.stringify(newUser));
            navigate('/map');
        } catch (err) {
            setError(err.message || "Error al registrar usuario.");
        }
    };

    const handleProfileCompletion = async (e) => {
        e.preventDefault();
        setError(null);
        try {
            const newUser = await completeProfile({
                email,
                nombre,
                boleta: regBoleta,
                carrera,
                vehiculo
            });
            localStorage.setItem('user', JSON.stringify(newUser));
            navigate('/map');
        } catch (err) {
            setError(err.message || "Error al completar perfil.");
        }
    };

    // --- VISTAS ---

    if (view === 'COMPLETE_PROFILE') {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-50">
                <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100">
                    <h2 className="text-2xl font-bold text-gray-900 text-center mb-2">Termina tu registro</h2>
                    <p className="text-gray-500 text-center text-sm mb-6">Hola {nombre}, configura tu cuenta institucional.</p>
                    {error && <div className="bg-red-50 text-red-600 p-3 rounded mb-4 text-sm font-medium">{error}</div>}

                    <form onSubmit={handleProfileCompletion} className="space-y-4">
                        <div>
                            <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wide">Correo</label>
                            <input type="text" disabled value={email} className="mt-1 block w-full px-4 py-2 bg-gray-100 border-none rounded-lg text-gray-500" />
                        </div>
                        <div>
                            <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wide">Boleta</label>
                            <input type="text" required value={regBoleta} onChange={e => setRegBoleta(e.target.value)}
                                className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all" />
                        </div>
                        {/* Carrera & Vehiculo Selects */}
                        <div>
                            <label className="block text-xs font-semibold text-gray-700 uppercase tracking-wide">Carrera</label>
                            <select value={carrera} onChange={e => setCarrera(e.target.value)} className="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                                <option>Ingeniería en Computación</option>
                                <option>Ingeniería en Comunicaciones y Electrónica</option>
                                <option>Ingeniería en Sistemas Automotrices</option>
                                <option>Ingeniería Mecanica</option>
                            </select>
                        </div>
                        <button type="submit" className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg shadow-lg transition-transform transform active:scale-95">
                            Completar Registro
                        </button>
                    </form>
                </div>
            </div>
        );
    }

    if (view === 'REGISTER') {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-50">
                <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100">
                    <div className="flex justify-between items-center mb-6">
                        <h2 className="text-2xl font-bold text-gray-900">Crear Cuenta</h2>
                        <button onClick={() => setView('LOGIN')} className="text-sm text-blue-600 hover:underline">Volver</button>
                    </div>
                    {error && <div className="bg-red-50 text-red-600 p-3 rounded mb-4 text-sm font-medium">{error}</div>}

                    <form onSubmit={handleRegister} className="space-y-4">
                        <div>
                            <label className="text-xs font-bold text-gray-500 uppercase">Nombre Completo</label>
                            <input type="text" required value={nombre} onChange={e => setNombre(e.target.value)} className="w-full mt-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Juan Pérez" />
                        </div>
                        <div>
                            <label className="text-xs font-bold text-gray-500 uppercase">Boleta</label>
                            <input type="text" required value={regBoleta} onChange={e => setRegBoleta(e.target.value)} className="w-full mt-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="2024..." />
                        </div>
                        {/* Simple Selects reusing state */}
                        <div>
                            <label className="text-xs font-bold text-gray-500 uppercase">Carrera</label>
                            <select value={carrera} onChange={e => setCarrera(e.target.value)} className="w-full mt-1 px-4 py-2 border rounded-lg outline-none">
                                <option>Ingeniería en Computación</option>
                                <option>Ingeniería en Comunicaciones y Electrónica</option>
                                <option>Ingeniería en Sistemas Automotrices</option>
                                <option>Ingeniería Mecánica</option>
                            </select>
                        </div>
                        <div>
                            <label className="text-xs font-bold text-gray-500 uppercase">Vehículo</label>
                            <select value={vehiculo} onChange={e => setVehiculo(e.target.value)} className="w-full mt-1 px-4 py-2 border rounded-lg outline-none">
                                <option value="ninguno">Ninguno</option>
                                <option value="automovil">Automóvil</option>
                                <option value="moto">Motocicleta</option>
                                <option value="bicicleta">Bicicleta/Patín eléctrico</option>
                            </select>
                        </div>
                        <button type="submit" className="w-full py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg shadow-md transition-all">
                            Registrarse
                        </button>
                    </form>
                </div>
            </div>
        );
    }

    // Default: LOGIN
    return (
        <div className="flex items-center justify-center min-h-screen bg-[#F3F4F6]">
            <div className="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-md border border-gray-200">
                <div className="text-center mb-8">
                    <span className="bg-[#800000] text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">ESIME CULHUACAN</span>
                    <h1 className="text-4xl font-extrabold text-[#1a202c] mt-4 tracking-tight">Bienvenido</h1>
                    <p className="text-gray-400 mt-2">Inicia sesión para navegar por el campus</p>
                </div>

                {error && (
                    <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm mb-6 text-center border border-red-100 font-medium animate-pulse">
                        {error}
                    </div>
                )}

                <div className="space-y-5">
                    <button
                        onClick={handleMicrosoftLogin}
                        className="w-full flex items-center justify-center px-4 py-3 bg-[#2F2F2F] text-white font-semibold rounded-xl hover:bg-black transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
                    >
                        <img
                            src="https://learn.microsoft.com/en-us/entra/identity-platform/media/howto-add-branding-in-apps/ms-symbollockup_mssymbol_19.png"
                            alt="Microsoft Logo"
                            className="w-5 h-5 mr-3 object-contain"
                        />
                        Continuar con Outlook
                    </button>

                    <div className="relative flex py-2 items-center">
                        <div className="flex-grow border-t border-gray-200"></div>
                        <span className="flex-shrink-0 mx-4 text-gray-300 text-xs font-bold uppercase">O ingresa manualmente</span>
                        <div className="flex-grow border-t border-gray-200"></div>
                    </div>

                    <form onSubmit={handleBoletaLogin} className="space-y-4">
                        <input
                            type="text"
                            value={boleta}
                            onChange={(e) => setBoleta(e.target.value)}
                            placeholder="Número de boleta"
                            className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:bg-white focus:outline-none transition-colors text-gray-700 font-medium"
                            required
                        />
                        <button
                            type="submit"
                            className="w-full py-3 bg-[#800000] hover:bg-[#600000] text-white font-bold rounded-xl shadow-lg transition-all hover:shadow-red-900/30"
                        >
                            Ingresar
                        </button>
                    </form>

                    <div className="text-center mt-6">
                        <p className="text-sm text-gray-500">
                            ¿No tienes cuenta?{' '}
                            <button onClick={() => setView('REGISTER')} className="text-blue-600 font-bold hover:underline">
                                Regístrate aquí
                            </button>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;
