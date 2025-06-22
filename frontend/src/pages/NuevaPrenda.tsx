import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import api from '@/lib/api';

interface Categoria {
  id: number;
  nombre: string;
}

interface Prenda {
  id: number;
  nombre: string;
  descripcion: string;
  categoria: number;
  precio_costo: number;
  precio_venta: number;
  genero: string;
  imagen_principal: string | null;
  activo: boolean;
  imagenes: { id: number; imagen: string; titulo: string; orden: number }[];
}

export const NuevaPrenda = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [nombre, setNombre] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [categoria, setCategoria] = useState<number | ''>('');
  const [precioCosto, setPrecioCosto] = useState<number | ''>('');
  const [precioVenta, setPrecioVenta] = useState<number | ''>('');
  const [genero, setGenero] = useState('');
  const [imagenPrincipal, setImagenPrincipal] = useState<File | null>(null);
  const [imagenes, setImagenes] = useState<File[]>([]);
  const [activo, setActivo] = useState(true);
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [loading, setLoading] = useState(false);
  const [existingImages, setExistingImages] = useState<
    {
      id: number;
      imagen: string;
      titulo: string;
      orden: number;
    }[]
  >([]);

  useEffect(() => {
    const fetchCategorias = async () => {
      try {
        const response = await api.get('/prendas/categorias/');
        setCategorias(response.data.results);
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    };

    const fetchPrenda = async () => {
      if (id) {
        try {
          const response = await api.get(`/prendas/prendas/${id}/`);
          const prenda: Prenda = response.data;
          setNombre(prenda.nombre);
          setDescripcion(prenda.descripcion);
          setCategoria(prenda.categoria);
          setPrecioCosto(prenda.precio_costo);
          setPrecioVenta(prenda.precio_venta);
          setGenero(prenda.genero);
          setActivo(prenda.activo);
          setExistingImages(prenda.imagenes);
        } catch (error) {
          console.error('Error fetching prenda:', error);
        }
      }
    };

    fetchCategorias();
    fetchPrenda();
  }, [id]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append('nombre', nombre);
    formData.append('descripcion', descripcion);
    formData.append('categoria', String(categoria));
    formData.append('precio_costo', String(precioCosto));
    formData.append('precio_venta', String(precioVenta));
    formData.append('genero', genero);
    if (imagenPrincipal) {
      formData.append('imagen_principal', imagenPrincipal);
    }
    imagenes.forEach((image, index) => {
      formData.append(`imagenes[${index}]`, image);
    });
    formData.append('activo', String(activo));

    try {
      if (id) {
        await api.put(`/prendas/prendas/${id}/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
      } else {
        await api.post('/prendas/prendas/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
      }

      navigate('/prendas');
    } catch (error) {
      console.error('Error saving prenda:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">
        {id ? 'Editar Prenda' : 'Nueva Prenda'}
      </h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label
            htmlFor="nombre"
            className="block text-sm font-medium text-foreground"
          >
            Nombre
          </label>
          <input
            type="text"
            id="nombre"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-background text-foreground"
            required
          />
        </div>
        <div>
          <label
            htmlFor="descripcion"
            className="block text-sm font-medium text-foreground"
          >
            Descripción
          </label>
          <textarea
            id="descripcion"
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            rows={3}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-background text-foreground"
          ></textarea>
        </div>
        <div>
          <label
            htmlFor="categoria"
            className="block text-sm font-medium text-foreground"
          >
            Categoría
          </label>
          <select
            id="categoria"
            value={categoria}
            onChange={(e) => setCategoria(Number(e.target.value))}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-background text-foreground"
            required
          >
            <option value="">Seleccione una categoría</option>
            {categorias &&
              categorias.map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.nombre}
                </option>
              ))}
          </select>
        </div>
        <div>
          <label
            htmlFor="precioCosto"
            className="block text-sm font-medium text-foreground"
          >
            Precio Costo
          </label>
          <input
            type="number"
            id="precioCosto"
            value={precioCosto}
            onChange={(e) => setPrecioCosto(Number(e.target.value))}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-background text-foreground"
            step="0.01"
            required
          />
        </div>
        <div>
          <label
            htmlFor="precioVenta"
            className="block text-sm font-medium text-foreground"
          >
            Precio Venta
          </label>
          <input
            type="number"
            id="precioVenta"
            value={precioVenta}
            onChange={(e) => setPrecioVenta(Number(e.target.value))}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-background text-foreground"
            step="0.01"
            required
          />
        </div>
        <div>
          <label
            htmlFor="genero"
            className="block text-sm font-medium text-foreground"
          >
            Género
          </label>
          <select
            id="genero"
            value={genero}
            onChange={(e) => setGenero(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 bg-background text-foreground"
            required
          >
            <option value="">Seleccione un género</option>
            <option value="M">Masculino</option>
            <option value="F">Femenino</option>
            <option value="U">Unisex</option>
          </select>
        </div>
        <div>
          <label
            htmlFor="imagenPrincipal"
            className="block text-sm font-medium text-foreground"
          >
            Imagen Principal
          </label>
          <input
            type="file"
            id="imagenPrincipal"
            onChange={(e) =>
              setImagenPrincipal(e.target.files ? e.target.files[0] : null)
            }
            className="mt-1 block w-full text-sm text-foreground file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          {id && existingImages.length > 0 && (
            <div className="mt-2">
              <h3 className="text-sm font-medium text-foreground">
                Imágenes Existentes:
              </h3>
              <div className="mt-2 grid grid-cols-4 gap-2">
                {existingImages.map((img) => (
                  <div
                    key={img.id}
                    className="relative w-24 h-24 overflow-hidden rounded-md"
                  >
                    <img
                      src={img.imagen}
                      alt={img.titulo || 'Existing image'}
                      className="w-full h-full object-cover"
                    />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
        <div>
          <label
            htmlFor="imagenes"
            className="block text-sm font-medium text-foreground"
          >
            Imágenes Adicionales
          </label>
          <input
            type="file"
            id="imagenes"
            multiple
            onChange={(e) => setImagenes(Array.from(e.target.files || []))}
            className="mt-1 block w-full text-sm text-foreground file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          {imagenes.length > 0 && (
            <div className="mt-2 grid grid-cols-4 gap-2">
              {imagenes.map((image, index) => (
                <div
                  key={index}
                  className="relative w-24 h-24 overflow-hidden rounded-md"
                >
                  <img
                    src={URL.createObjectURL(image)}
                    alt={`Preview ${index}`}
                    className="w-full h-full object-cover"
                  />
                </div>
              ))}
            </div>
          )}
        </div>
        <div className="flex items-center">
          <input
            type="checkbox"
            id="activo"
            checked={activo}
            onChange={(e) => setActivo(e.target.checked)}
            className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <label
            htmlFor="activo"
            className="ml-2 block text-sm text-foreground"
          >
            Activo
          </label>
        </div>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? 'Guardando...' : 'Guardar'}
        </button>
      </form>
    </div>
  );
};

export default NuevaPrenda;
