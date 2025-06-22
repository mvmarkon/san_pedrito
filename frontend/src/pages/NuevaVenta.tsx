import React from 'react';

export const NuevaVenta = () => {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Nueva Venta</h1>
      <form className="space-y-4">
        {/* Form fields for new venta will go here */}
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Guardar
        </button>
      </form>
    </div>
  );
};

export default NuevaVenta;
