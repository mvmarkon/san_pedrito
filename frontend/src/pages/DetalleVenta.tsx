import React from 'react';
import DashboardLayout from '../layouts/DashboardLayout';

export const DetalleVenta = () => {
  return (
    <DashboardLayout>
      <div className="p-4">
        <h1 className="text-2xl font-bold mb-4">Detalle de Venta</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Venta details will go here */}
          <div>
            <h2 className="text-lg font-semibold">Información de la Venta</h2>
            {/* Basic info fields */}
          </div>
          <div>
            <h2 className="text-lg font-semibold">Items de la Venta</h2>
            {/* Items list */}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default DetalleVenta;