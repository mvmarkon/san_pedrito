import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import api from '@/lib/api';

interface Prenda {
  id: number;
  nombre: string;
  descripcion: string;
  precio: string;
  // Add other fields as necessary
}

export const Prendas = () => {
  const [prendas, setPrendas] = useState<Prenda[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPrendas = async () => {
      try {
        const response = await api.get('/prendas/prendas/');
        if (response.data && Array.isArray(response.data.results)) {
          setPrendas(response.data.results);
        } else {
          console.error('Unexpected response format:', response.data);
          setError('Error: Formato de datos inesperado.');
        }
      } catch (err) {
        console.error('Error fetching prendas:', err);
        setError('Error al cargar las prendas.');
      } finally {
        setLoading(false);
      }
    };

    fetchPrendas();
  }, []);

  if (loading) {
    return <div className="p-4">Cargando prendas...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">{error}</div>;
  }

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Prendas</h1>
        <Link
          to="/prendas/nueva"
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Nueva Prenda
        </Link>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white dark:bg-gray-800 shadow-md rounded-lg overflow-hidden">
          <thead className="bg-gray-200 dark:bg-gray-700">
            <tr>
              <th className="py-2 px-4 text-left text-sm font-semibold text-gray-700 dark:text-gray-200">
                Nombre
              </th>
              <th className="py-2 px-4 text-left text-sm font-semibold text-gray-700 dark:text-gray-200">
                Descripción
              </th>
              <th className="py-2 px-4 text-left text-sm font-semibold text-gray-700 dark:text-gray-200">
                Precio
              </th>
              <th className="py-2 px-4 text-left text-sm font-semibold text-gray-700 dark:text-gray-200">
                Acciones
              </th>
            </tr>
          </thead>
          <tbody>
            {prendas.length > 0 ? (
              prendas.map((prenda) => (
                <tr
                  key={prenda.id}
                  className="border-b border-gray-200 dark:border-gray-700"
                >
                  <td className="py-2 px-4 text-sm text-gray-900 dark:text-gray-100">
                    {prenda.nombre}
                  </td>
                  <td className="py-2 px-4 text-sm text-gray-900 dark:text-gray-100">
                    {prenda.descripcion}
                  </td>
                  <td className="py-2 px-4 text-sm text-gray-900 dark:text-gray-100">
                    {prenda.precio}
                  </td>
                  <td className="py-2 px-4 text-sm">
                    <Link
                      to={`/prendas/editar/${prenda.id}`}
                      className="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-200 mr-2"
                    >
                      Editar
                    </Link>
                    <button className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-200">
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan={4}
                  className="py-4 text-center text-gray-500 dark:text-gray-400"
                >
                  No hay prendas disponibles.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Prendas;
