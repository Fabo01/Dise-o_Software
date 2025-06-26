// Frontend/js/api.js
const BASE_URL = 'http://localhost:8000/api/';

// Clientes
export async function obtenerClientes() {
  const res = await fetch(BASE_URL + 'clientes/');
  if (!res.ok) throw new Error('Error al obtener clientes');
  return await res.json();
}

export async function crearCliente(datos) {
  const res = await fetch(BASE_URL + 'clientes/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  });
  if (!res.ok) throw new Error('Error al crear cliente');
  return await res.json();
}

// Pedidos
export async function obtenerPedidos() {
  const res = await fetch(BASE_URL + 'pedidos/');
  if (!res.ok) throw new Error('Error al obtener pedidos');
  return await res.json();
}

export async function crearPedido(datos) {
  const res = await fetch(BASE_URL + 'pedidos/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  });
  if (!res.ok) throw new Error('Error al crear pedido');
  return await res.json();
}

// Ingredientes
export async function obtenerIngredientes() {
  const res = await fetch(BASE_URL + 'ingredientes/');
  if (!res.ok) throw new Error('Error al obtener ingredientes');
  return await res.json();
}

export async function crearIngrediente(datos) {
  const res = await fetch(BASE_URL + 'ingredientes/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  });
  if (!res.ok) throw new Error('Error al crear ingrediente');
  return await res.json();
}

// Usuarios
export async function obtenerUsuarios() {
  const res = await fetch(BASE_URL + 'usuarios/');
  if (!res.ok) throw new Error('Error al obtener usuarios');
  return await res.json();
}

export async function crearUsuario(datos) {
  const res = await fetch(BASE_URL + 'usuarios/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  });
  if (!res.ok) throw new Error('Error al crear usuario');
  return await res.json();
}