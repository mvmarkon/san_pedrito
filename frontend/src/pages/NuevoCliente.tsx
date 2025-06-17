import React from 'react';
export const NuevoCliente = () => {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Nuevo Cliente</h1>
      <form className="space-y-4">
        {/* Form fields for new client will go here */}
        <div className="flex space-x-4">
          <button 
            type="submit" 
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Guardar
          </button>
          <button 
            type="button" 
            className="px-4 py-2 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
          >
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
};

export default NuevoCliente;