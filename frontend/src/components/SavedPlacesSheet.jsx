import React, { useState, useEffect } from 'react';
import { X, Bookmark, Edit, Plus, User, Clock, MapPin, Trash2, Heart } from 'lucide-react';
// api import removed as it does not exist as default export

const SavedPlacesSheet = ({ onClose }) => {
    const [savedPlaces, setSavedPlaces] = useState([]);
    const [isAdding, setIsAdding] = useState(false); // To toggle "Add Places" view
    const [allBuildings, setAllBuildings] = useState([]); // List of system buildings to Favorite
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState(null);

    useEffect(() => {
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            const parsedUser = JSON.parse(storedUser);
            setUser(parsedUser);
            fetchSavedPlaces(parsedUser.boleta);
            fetchAllBuildings();
        }
    }, []);

    const fetchSavedPlaces = async (boleta) => {
        try {
            const res = await fetch(`http://127.0.0.1:5001/api/saved-places?user_boleta=${boleta}`);
            if (res.ok) {
                const data = await res.json();
                setSavedPlaces(data);
            }
        } catch (error) {
            console.error("Error fetching saved places:", error);
        } finally {
            setLoading(false);
        }
    };

    const fetchAllBuildings = async () => {
        try {
            const res = await fetch(`http://127.0.0.1:5001/api/buildings`);
            if (res.ok) {
                const data = await res.json();
                setAllBuildings(data);
            }
        } catch (error) {
            console.error("Error fetching buildings:", error);
        }
    };

    const handleDelete = async (id) => {
        try {
            const res = await fetch(`http://127.0.0.1:5001/api/saved-places/${id}`, { method: 'DELETE' });
            if (res.ok) {
                setSavedPlaces(prev => prev.filter(p => p.id !== id));
            }
        } catch (error) {
            console.error("Error deleting place:", error);
        }
    };

    const handleAddFavorite = async (building) => {
        if (!user) return;
        // Check if already saved
        if (savedPlaces.some(p => p.name === building.nombre)) {
            alert("Ya está guardado");
            return;
        }

        try {
            const res = await fetch(`http://127.0.0.1:5001/api/saved-places`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_boleta: user.boleta,
                    name: building.nombre,
                    lat: building.lat,
                    lon: building.lon,
                    type: 'favorite'
                })
            });
            if (res.ok) {
                const newPlace = await res.json();
                setSavedPlaces(prev => [...prev, newPlace]);
                setIsAdding(false); // Go back to list
            }
        } catch (error) {
            console.error("Error adding favorite:", error);
        }
    };

    const renderIcon = (type) => {
        if (type === 'favorite') return <div className="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center text-red-600"><Heart size={20} fill="currentColor" /></div>;
        return <div className="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center text-gray-500"><MapPin size={20} /></div>;
    };

    return (
        <div className="fixed inset-x-0 bottom-0 z-50 flex flex-col h-[85vh] transition-transform duration-300 ease-in-out transform translate-y-0 text-gray-800 font-sans shadow-2xl rounded-t-[32px] overflow-hidden">

            {/* Header Section - Red Gradient */}
            <div className="bg-[#b91c1c] p-6 text-white shrink-0 relative">
                {/* Close Button */}
                <button
                    onClick={onClose}
                    className="absolute top-6 right-6 p-1.5 bg-white/20 rounded-full hover:bg-white/30 transition-colors"
                >
                    <X size={20} className="text-white" />
                </button>

                <div className="mt-2">
                    <Bookmark size={32} className="text-white mb-2" />
                    <h2 className="text-2xl font-bold mb-1">
                        {isAdding ? "Agregar Favorito" : "Lugares Guardados"}
                    </h2>

                    {!isAdding && (
                        <div className="flex items-center text-sm text-white/80 mb-6">
                            <span>{user ? user.nombre : "Usuario"} • {savedPlaces.length} Guardados</span>
                        </div>
                    )}

                    {!isAdding ? (
                        <div className="flex gap-3 mt-4">
                            <button
                                onClick={() => setIsAdding(true)}
                                className="flex items-center gap-2 px-6 py-2 bg-white text-black rounded-full text-xs font-bold hover:bg-gray-100 transition-colors uppercase tracking-wide"
                            >
                                <Plus size={16} />
                                Agregar lugares
                            </button>
                        </div>
                    ) : (
                        <button
                            onClick={() => setIsAdding(false)}
                            className="mt-4 flex items-center gap-2 px-4 py-1.5 bg-white/20 text-white rounded-full text-xs font-bold hover:bg-white/30 transition-colors uppercase"
                        >
                            <X size={14} /> Cancelar
                        </button>
                    )}
                </div>
            </div>

            {/* Body Section */}
            <div className="flex-1 bg-white overflow-y-auto px-0 pt-4 pb-24">

                {isAdding ? (
                    // VIEW: List of all system buildings to add
                    <div className="px-4">
                        <h3 className="text-sm font-bold text-gray-500 uppercase tracking-widest mb-4 px-2">Lugares Disponibles</h3>
                        <div className="space-y-2">
                            {allBuildings.map(b => (
                                <div key={b.id} className="flex justify-between items-center p-3 hover:bg-gray-50 rounded-xl border border-transparent hover:border-gray-100 transition-all">
                                    <div className="flex items-center gap-3">
                                        <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-600">
                                            <MapPin size={16} />
                                        </div>
                                        <span className="text-sm font-bold text-gray-800">{b.nombre}</span>
                                    </div>
                                    <button
                                        onClick={() => handleAddFavorite(b)}
                                        className="text-white bg-red-600 p-2 rounded-full hover:bg-red-700 shadow-md"
                                    >
                                        <Plus size={16} />
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>
                ) : (
                    // VIEW: Saved Places List
                    <>
                        {savedPlaces.length === 0 && !loading && (
                            <div className="text-center py-10 px-6 opacity-60">
                                <Bookmark size={48} className="mx-auto mb-4 text-gray-300" />
                                <p className="text-sm font-bold text-gray-400">Aún no tienes lugares guardados.</p>
                            </div>
                        )}

                        <div className="divide-y divide-gray-100">
                            {savedPlaces.map((place) => (
                                <div key={place.id} className="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors">
                                    <div className="flex items-center gap-4 flex-1">
                                        {renderIcon(place.type)}
                                        <div className="flex flex-col">
                                            <span className="text-sm font-bold text-gray-900 leading-tight">
                                                {place.name}
                                            </span>
                                            <span className="text-[10px] text-gray-400 font-medium uppercase tracking-wider mt-0.5">
                                                {place.type === 'custom' ? 'Personalizado' : 'Favorito'}
                                            </span>
                                        </div>
                                    </div>

                                    <button
                                        onClick={() => handleDelete(place.id)}
                                        className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
                                    >
                                        <Trash2 size={18} />
                                    </button>
                                </div>
                            ))}
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default SavedPlacesSheet;
