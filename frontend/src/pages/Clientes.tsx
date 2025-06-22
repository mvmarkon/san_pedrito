import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Cliente {
  id: number;
  nombre: string;
  apellido: string;
  email: string;
  document_number: string;
  phone_number?: string;
  address?: string;
}

export const Clientes = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchClientes = async () => {
      try {
        const response = await axios.get<Cliente[]>(`${import.meta.env.VITE_API_URL}/clientes/`);
        setClientes(response.data);
      } catch (err) {
        setError('Error al cargar los clientes.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchClientes();
  }, []);

  if (loading) {
    return <div className="p-4">Cargando clientes...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">{error}</div>;
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Clientes</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white shadow-md rounded-lg overflow-hidden">
          <thead className="bg-gray-200 text-gray-700">
            <tr>
              <th className="py-2 px-4 text-left">Nombre</th>
              <th className="py-2 px-4 text-left">Apellido</th>
              <th className="py-2 px-4 text-left">Email</th>
              <th className="py-2 px-4 text-left">Documento</th>
              <th className="py-2 px-4 text-left">Teléfono</th>
              <th className="py-2 px-4 text-left">Dirección</th>
            </tr>
          </thead>
          <tbody className="text-gray-600">
            {clientes.map((cliente) => (
              <tr key={cliente.id} className="border-b border-gray-200 hover:bg-gray-100">
                <td className="py-2 px-4">{cliente.nombre}</td>
                <td className="py-2 px-4">{cliente.apellido}</td>
                <td className="py-2 px-4">{cliente.email}</td>
                <td className="py-2 px-4">{cliente.document_number}</td>
                <td className="py-2 px-4">{cliente.phone_number || 'N/A'}</td>
                <td className="py-2 px-4">{cliente.address || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Clientes;
