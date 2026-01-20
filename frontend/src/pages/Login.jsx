import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "../authConfig";
import { login, checkEmail, completeProfile } from '../services/api';

const Login = () => {
    const navigate = useNavigate();
    const { instance } = useMsal();

    // Estados
    const [step, setStep] = useState('CHOICE');
    const [error, setError] = useState(null);

    // Boleta Login State
    const [boleta, setBoleta] = useState('');

    // Profile Completion State
    const [email, setEmail] = useState('');
    const [msName, setMsName] = useState('');
    const [newBoleta, setNewBoleta] = useState('');
    const [carrera, setCarrera] = useState('Ingeniería en Sistemas Computacionales');
    const [vehiculo, setVehiculo] = useState('ninguno');

    const handleMicrosoftLogin = () => {
        setError(null);
        instance.loginPopup(loginRequest)
            .then(async (response) => {
                const msEmail = response.account.username; // si el correo no esta disponible 

                setEmail(msEmail);
                setMsName(name);
                // Verificar si el usuario existe en nuestra base de datos
                try {
                    const check = await checkEmail(msEmail);
                    if (check.exists) {
                        // Login Success
                        localStorage.setItem('user', JSON.stringify(check.user));
                        navigate('/map');
                    } else {
                        // Debemos completar el perfil
                        setStep('COMPLETE_PROFILE');
                    }
                } catch (err) {
                    setError("Error conectando con el servidor");
                }
            })
            .catch(e => {
                console.error(e);
                setError("Error al iniciar sesión con Microsoft");
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
            setError(err.message || "Usuario no encontrado");
        }
    };

    const handleCompleteProfile = async (e) => {
        e.preventDefault();
        setError(null);
        try {
            const newUser = await completeProfile({
                email: email,
                nombre: msName,
                boleta: newBoleta,
                carrera,
                vehiculo
            });
            localStorage.setItem('user', JSON.stringify(newUser));
            navigate('/map');
        } catch (err) {
            setError(err.message || "Error al registrar perfil");
        }
    };

    // renderizado

    if (step === 'COMPLETE_PROFILE') {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-100">
                <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
                    <h1 className="text-xl font-bold text-center mb-2 text-blue-900">Completar Perfil</h1>
                    <p className="text-sm text-center text-gray-600 mb-6">Hola {msName}, termina de configurar tu cuenta.</p>

                    {error && <div className="mb-4 text-red-600 text-center text-sm">{error}</div>}

                    <form onSubmit={handleCompleteProfile} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Correo Institucional</label>
                            <input type="text" disabled value={email} className="mt-1 block w-full px-3 py-2 bg-gray-100 border border-gray-300 rounded-md text-gray-500" />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Número de Boleta</label>
                            <input
                                type="text"
                                required
                                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500"
                                value={newBoleta}
                                onChange={(e) => setNewBoleta(e.target.value)}
                                placeholder="2020640001"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Carrera</label>
                            <select value={carrera} onChange={(e) => setCarrera(e.target.value)} className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500">
                                <option>Ingeniería en Sistemas Computacionales</option>
                                <option>Ingeniería en Comunicaciones y Electrónica</option>
                                <option>Ingeniería Mecánica</option>
                                <option>Ingeniería Eléctrica</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Medio de Transporte</label>
                            <select value={vehiculo} onChange={(e) => setVehiculo(e.target.value)} className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500">
                                <option value="ninguno">Ninguno</option>
                                <option value="auto">Automóvil</option>
                                <option value="moto">Motocicleta</option>
                                <option value="bici">Bicicleta</option>
                            </select>
                        </div>
                        <button
                            type="submit"
                            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                        >
                            Registrar y Entrar
                        </button>
                    </form>
                </div>
            </div>
        );
    }

    // Vista default
    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-md">
                <h1 className="text-2xl font-bold text-center mb-6 text-blue-900">ESIME Map</h1>

                {error && <div className="mb-4 text-red-600 text-center text-sm">{error}</div>}

                <div className="space-y-4">
                    {/* Boton Microsoft*/}
                    <button
                        onClick={handleMicrosoftLogin}
                        className="w-full flex items-center justify-center gap-2 py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                        <img src="https://learn.microsoft.com/en-us/entra/identity-platform/media/howto-add-branding-in-apps/ms-symbollockup_mssymbol_19.png" alt="Microsoft" className="h-5 w-5" />
                        Iniciar sesión con Correo Institucional
                    </button>

                    <div className="relative">
                        <div className="absolute inset-0 flex items-center">
                            <div className="w-full border-t border-gray-300"></div>
                        </div>
                        <div className="relative flex justify-center text-sm">
                            <span className="px-2 bg-white text-gray-500">O ingresa con tu número de boleta</span>
                        </div>
                    </div>

                    {/* Boleta Login */}
                    <form onSubmit={handleBoletaLogin} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700">Número de Boleta</label>
                            <input
                                type="text"
                                required
                                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                                value={boleta}
                                onChange={(e) => setBoleta(e.target.value)}
                                placeholder="2020..."
                            />
                        </div>
                        <button
                            type="submit"
                            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-900 hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                        >
                            Ingresar con número de boleta
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Login;
