# San Pedrito - Aplicación de Gestión de Stock de Ropa Infantil

San Pedrito es una Progressive Web App (PWA) multiplataforma diseñada para gestionar stock de ropa infantil, clientes y ventas.

## Estructura del Proyecto

```
/
├── frontend/         # Aplicación Vite + React
├── backend/          # API Django + Django REST Framework
└── docker-compose.yml  # Configuración de Docker
```

## Requisitos Técnicos

### Frontend
- Framework: Vite + React
- Librerías: react-query, zustand, react-hook-form, react-table, react-to-print, react-chartjs-2
- UI/UX: shadcn/ui, diseño responsive (mobile-first)
- PWA: vite-plugin-pwa

### Backend
- Framework: Django + Django REST Framework
- Base de datos: PostgreSQL
- Autenticación: Token-based (Django REST SimpleJWT)

### Dockerización
- Servicios: frontend, backend, db

## Funcionalidades Clave

### Gestión de Stock
- Modelo de datos para prendas
- Generación de QR
- Subida de fotos
- Alertas de stock

### Clientes y Ventas
- ABM de clientes
- Registro de ventas
- Tickets imprimibles
- Reservas

### Dashboard
- Métricas visuales
- Exportación de datos

## Instalación y Configuración

### Requisitos Previos
- Docker y Docker Compose
- Node.js (para desarrollo local del frontend)
- Python (para desarrollo local del backend)

### Configuración Local

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd san_pedrito
```

2. Iniciar los servicios con Docker Compose:
en el frontend hacer
```bash
npm install
npm run build
```
Luego volver al directorio raiz y hacer
```bash
docker-compose up
```

3. Acceder a la aplicación:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/api/
   - Documentación API: http://localhost:8000/api/docs/

## Desarrollo

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Licencia

Este proyecto está licenciado bajo [Licencia].