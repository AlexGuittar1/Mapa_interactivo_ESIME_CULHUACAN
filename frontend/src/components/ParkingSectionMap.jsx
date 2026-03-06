import React from 'react';
import { MapIcon } from 'lucide-react';

const ParkingSectionMap = ({ section }) => {
    if (!section) return null;

    return (
        <div className="w-full h-full min-h-[300px] bg-white rounded-3xl shadow-sm border border-gray-100 overflow-hidden flex flex-col relative">
            {/* Header del Mapa */}
            <div className="bg-gray-50 border-b border-gray-100 px-6 py-4 flex items-center justify-between z-10">
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-blue-100 rounded-lg">
                        <MapIcon className="w-5 h-5 text-blue-600" />
                    </div>
                    <div>
                        <h3 className="font-bold text-gray-900 leading-tight">Plano 2D</h3>
                        <p className="text-xs text-gray-500 font-medium">{section.name}</p>
                    </div>
                </div>
                <div className="bg-white px-3 py-1 rounded-full shadow-sm border border-gray-200 text-xs font-bold text-gray-600">
                    {section.total_spaces} Cajones
                </div>
            </div>

            {/* Contenedor Gráfico (Viewport) */}
            <div className="flex-1 w-full h-full relative bg-[#f8fafc] flex items-center justify-center p-6">

                {section.map_image_url ? (
                    <img
                        src={section.map_image_url}
                        alt={`Mapa de ${section.name}`}
                        className="w-full h-full object-contain rounded-xl shadow-sm"
                    />
                ) : (
                    /* EMPTY STATE ELEGANT */
                    <div className="flex flex-col items-center justify-center text-center max-w-xs animate-pulse-slow">
                        <div className="w-24 h-24 mb-4 rounded-full bg-blue-50 flex items-center justify-center">
                            <MapIcon className="w-10 h-10 text-blue-300" strokeWidth={1.5} />
                        </div>
                        <h4 className="text-lg font-bold text-gray-700 mb-2">Plano no disponible</h4>
                        <p className="text-sm text-gray-400 font-medium">
                            El mapa esquemático para <b>{section.name}</b> aún no ha sido cargado en el sistema.
                        </p>
                    </div>
                )}

            </div>
        </div>
    );
};

export default ParkingSectionMap;
