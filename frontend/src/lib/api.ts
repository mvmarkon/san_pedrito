import axios from 'axios';
import { toast } from 'react-toastify';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para añadir el token de autenticación
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Interceptor para manejar errores de respuesta
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response;
      let errorMessage = 'Ha ocurrido un error inesperado.';

      switch (status) {
        case 400:
          errorMessage = data.detail || data.message || 'Solicitud inválida.';
          if (data.email) errorMessage = `Email: ${data.email[0]}`;
          if (data.document_number) errorMessage = `Documento: ${data.document_number[0]}`;
          if (data.password) errorMessage = `Contraseña: ${data.password[0]}`;
          if (data.non_field_errors) errorMessage = data.non_field_errors[0];
          break;
        case 401:
          errorMessage = data.detail || 'No autorizado. Por favor, inicie sesión de nuevo.';
          // Optionally redirect to login page
          // window.location.href = '/login';
          break;
        case 403:
          errorMessage = data.detail || 'No tiene permiso para realizar esta acción.';
          break;
        case 404:
          errorMessage = data.detail || 'El recurso solicitado no fue encontrado.';
          break;
        case 500:
          errorMessage = 'Error interno del servidor. Por favor, intente de nuevo más tarde.';
          break;
        default:
          errorMessage = data.detail || data.message || `Error: ${status}`;
      }
      toast.error(errorMessage);
    } else if (error.request) {
      toast.error('No se pudo conectar con el servidor. Verifique su conexión a internet.');
    } else {
      toast.error('Error al configurar la solicitud.');
    }
    return Promise.reject(error);
  },
);

export default api;
