import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './index.css';

// Configurar el contenedor de la aplicación
const container = document.getElementById('root');
const root = createRoot(container);

// Renderizar la aplicación
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
