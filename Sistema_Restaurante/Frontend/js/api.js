// Frontend/js/api.js
export async function obtenerClientes() {
  const response = await fetch('http://localhost:8000/api/clientes/', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      // Si usas JWT:
      // 'Authorization': 'Bearer TU_TOKEN_JWT'
    }
  });
  if (!response.ok) throw new Error('Error al obtener clientes');
  return await response.json();
}

export async function crearCliente(datos) {
  const response = await fetch('http://localhost:8000/api/clientes/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // 'Authorization': 'Bearer TU_TOKEN_JWT'
    },
    body: JSON.stringify(datos)
  });
  if (!response.ok) throw new Error('Error al crear cliente');
  return await response.json();
}