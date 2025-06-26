# Tutorial: Activación del Frontend con React y TypeScript

Este tutorial te guía para instalar, ejecutar y conectar el frontend del sistema de restaurante usando React y TypeScript.

---

## 1. Requisitos Previos

- Node.js y npm instalados ([descargar aquí](https://nodejs.org/))
- Acceso a la terminal

---

## 2. Crear el Proyecto Frontend

Si aún no tienes el proyecto creado, ejecuta:

```bash
npx create-react-app frontend --template typescript
```

Esto generará una carpeta `frontend` con la estructura base.

---

## 3. Instalar Dependencias Adicionales (opcional)

Si necesitas consumir APIs o manejar rutas, instala:

```bash
cd frontend
npm install axios react-router-dom
```

---

## 4. Ejecutar el Frontend

Desde la carpeta `frontend`, ejecuta:

```bash
npm start
```

Esto abrirá la app en tu navegador en [http://localhost:3000](http://localhost:3000).

---

## 5. Estructura Básica de un Componente

Puedes editar `src/App.tsx` para personalizar la pantalla principal:

```typescript
// filepath: frontend/src/App.tsx
import React from 'react';

function App() {
  return (
    <div>
      <h1>Sistema Restaurante</h1>
      <p>¡Frontend React + TypeScript funcionando!</p>
    </div>
  );
}

export default App;
```

---

## 6. Conectar con el Backend

Para consumir la API de Django, puedes usar `axios`:

```typescript
// filepath: frontend/src/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Cambia el puerto si tu backend usa otro
});

export default api;
```

Ejemplo de uso en un componente:

```typescript
// filepath: frontend/src/App.tsx
import React, { useEffect, useState } from 'react';
import api from './api';

function App() {
  const [clientes, setClientes] = useState([]);

  useEffect(() => {
    api.get('/api/clientes/')
      .then(res => setClientes(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>Clientes</h1>
      <ul>
        {clientes.map((c: any) => (
          <li key={c.id}>{c.nombre} ({c.rut})</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
```

---

## 7. Personalización y Desarrollo

- Agrega tus propios componentes en la carpeta `src/`.
- Usa `npm run build` para generar una versión lista para producción.

---

¡Listo! Ahora tienes el frontend React funcionando y listo para conectarse con tu backend Django.
