import React from 'react';
export const DetallePrenda = () => {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Detalle de Prenda</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Prenda details will go here */}
        <div>
          <h2 className="text-lg font-semibold">Información Básica</h2>
          {/* Basic info fields */}
        </div>
        <div>
          <h2 className="text-lg font-semibold">Imágenes</h2>
          {/* Image gallery */}
        </div>
      </div>
    </div>
  );
};

export default DetallePrenda;