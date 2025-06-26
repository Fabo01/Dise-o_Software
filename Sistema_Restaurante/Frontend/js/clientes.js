const API_URL = 'http://localhost:8000/api/clientes/'; // Ajusta si tu endpoint es diferente

// Registrar cliente
document.getElementById('formCrearCliente').addEventListener('submit', async (e) => {
  e.preventDefault();
  const datos = {
    nombre: document.getElementById('nombre').value,
    rut: document.getElementById('rut').value,
    correo: document.getElementById('correo').value,
    telefono: document.getElementById('telefono').value,
    direccion: document.getElementById('direccion').value,
  };
  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datos)
    });
    if (!res.ok) throw new Error('Error al registrar cliente');
    alert('Cliente registrado correctamente');
    document.getElementById('formCrearCliente').reset();
    cargarClientes();
  } catch (err) {
    alert(err.message);
  }
});

// Buscar clientes
document.getElementById('btnBuscarCliente').addEventListener('click', async () => {
  const criterio = document.getElementById('busquedaCliente').value;
  cargarClientes(criterio);
});

// Cargar lista de clientes
async function cargarClientes(criterio = '') {
  let url = API_URL;
  if (criterio) {
    url += `?search=${encodeURIComponent(criterio)}`;
  }
  const res = await fetch(url);
  const clientes = await res.json();
  const tbody = document.querySelector('#tablaClientes tbody');
  tbody.innerHTML = '';
  clientes.forEach(cliente => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${cliente.id}</td>
      <td>${cliente.nombre}</td>
      <td>${cliente.rut}</td>
      <td>${cliente.correo}</td>
      <td>${cliente.telefono || ''}</td>
      <td>${cliente.direccion || ''}</td>
      <td>
        <button onclick="eliminarCliente(${cliente.id})">Eliminar</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// Eliminar cliente
window.eliminarCliente = async function(id) {
  if (!confirm('¿Seguro que deseas eliminar este cliente?')) return;
  const res = await fetch(`${API_URL}${id}/`, { method: 'DELETE' });
  if (res.status === 204) {
    alert('Cliente eliminado');
    cargarClientes();
  } else {
    const error = await res.json();
    alert(error.error || 'Error al eliminar cliente');
  }
};

// Cargar clientes al iniciar
cargarClientes();