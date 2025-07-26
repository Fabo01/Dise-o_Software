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
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              theme: {
                primary: '#4aed88',
              },
            },
            error: {
              duration: 5000,
              theme: {
                primary: '#ff6b6b',
              },
            },
          }}
        />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
);
