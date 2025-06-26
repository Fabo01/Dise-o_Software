import { GestorPedidos } from './gestorPedidos.js';
import { UI } from './ui.js';
import { obtenerIngredientes, crearIngrediente, obtenerClientes, crearCliente, obtenerUsuarios, crearUsuario } from './api.js';

const elementos = {
  form: document.getElementById('formPedido'),
  inputPedido: document.getElementById('inputPedido'),
  filtroEstado: document.getElementById('filtroEstado'),
  tablaPedidos: document.getElementById('tablaPedidos'),
  totalPedidos: document.getElementById('totalPedidos'),
  countPendientes: document.getElementById('countPendientes'),
  countPreparacion: document.getElementById('countPreparacion'),
  countListos: document.getElementById('countListos'),
  resumenPendientes: document.getElementById('resumenPendientes'),
  resumenPreparacion: document.getElementById('resumenPreparacion'),
  resumenListos: document.getElementById('resumenListos'),
};

const gestorPedidos = new GestorPedidos();
const ui = new UI(gestorPedidos, elementos);

document.addEventListener('DOMContentLoaded', () => {
  const select = document.getElementById('inputPedido');
  const cards = document.querySelectorAll('.menu-card[data-nombre]');
  if (select && cards.length) {
    // Limpia el select y agrega la opción por defecto
    select.innerHTML = '<option value="" disabled selected>Selecciona un menú</option>';
    cards.forEach(card => {
      const nombre = card.getAttribute('data-nombre');
      if (nombre) {
        const option = document.createElement('option');
        option.value = nombre;
        option.textContent = nombre;
        select.appendChild(option);
      }
    });
  }
});

function obtenerPrecioPorNombre(nombre) {
  // Busca el precio en las cards del menú
  const card = document.querySelector(`.menu-card[data-nombre="${nombre}"]`);
  if (card) {
    const precioSpan = card.querySelector('.precio');
    if (precioSpan) {
      // Quita el $ y puntos, y lo convierte a número
      return parseInt(precioSpan.textContent.replace(/\$|\./g, ''), 10);
    }
  }
  return 0;
}

// Agrupa pedidos listos por mesa
function obtenerCuentasPorMesa(pedidos) {
  const cuentas = {};
  pedidos.filter(p => p.estado === 'Listo').forEach(pedido => {
    if (!cuentas[pedido.mesa]) cuentas[pedido.mesa] = [];
    cuentas[pedido.mesa].push(pedido);
  });
  return cuentas;
}

function renderCuentasPorMesa(pedidos) {
  const tabla = document.getElementById('tablaCuentas');
  const tbody = tabla.querySelector('tbody');
  tbody.innerHTML = '';

  const cuentas = obtenerCuentasPorMesa(pedidos);

  Object.entries(cuentas).forEach(([mesa, pedidosMesa], idx) => {
    const subtotal = pedidosMesa.reduce((sum, p) => sum + obtenerPrecioPorNombre(p.nombre), 0);
    const iva = Math.round(subtotal * 0.19);
    const total = subtotal + iva;
    const pedidosNombres = pedidosMesa.map(p => p.nombre).join(', ');

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${mesa}</td>
      <td>${pedidosNombres}</td>
      <td>$${subtotal.toLocaleString('es-CL')}</td>
      <td>$${iva.toLocaleString('es-CL')}</td>
      <td>$${total.toLocaleString('es-CL')}</td>
      <td><button onclick="generarBoletaPDFMesa('Mesa 1')">Boleta PDF</button></td>
    `;
    tbody.appendChild(tr);
  });
}

// Suscribirse a los cambios de pedidos para actualizar la UI y las cuentas
gestorPedidos.subscribe((pedidos) => {
  ui.render(pedidos);
  renderCuentasPorMesa(pedidos);
});

// Llama una vez al cargar la página para mostrar el estado inicial
document.addEventListener('DOMContentLoaded', () => {
  renderCuentasPorMesa(gestorPedidos.pedidos);
});

// En main.js, modifica la función handleAgregarPedido:
function handleAgregarPedido(event) {
  event.preventDefault();
  const nombre = elementos.inputPedido.value.trim();
  const selectCliente = document.getElementById('inputClientePedido');
  const rutCliente = selectCliente.value;
  const clienteObj = window.clientes?.find(c => c.rut === rutCliente);
  if (nombre && clienteObj) {
    gestorPedidos.agregarPedido({
      nombre, // nombre del producto
      cliente: clienteObj.nombre + ' ' + clienteObj.apellido,
      mesa: clienteObj.mesa // <-- aquí debe ir el nombre de la mesa asignada al cliente
    });
    elementos.inputPedido.value = '';
    selectCliente.value = '';
  }
}

window.generarBoleta = function(idx) {
  const pedido = gestorPedidos.pedidos[idx];
  if (!pedido) return;
  // Precio genérico, puedes mejorarlo según tu lógica
  const precio = 10000; // CLP
  const iva = Math.round(precio * 0.19);
  const total = precio + iva;

  const boleta = `
    <h3>Boleta</h3>
    <p><strong>Cliente:</strong> ${pedido.cliente}</p>
    <p><strong>Mesa:</strong> ${pedido.mesa}</p>
    <p><strong>Pedido:</strong> ${pedido.nombre}</p>
    <p><strong>Subtotal:</strong> $${precio.toLocaleString('es-CL')}</p>
    <p><strong>IVA (19%):</strong> $${iva.toLocaleString('es-CL')}</p>
    <p><strong>Total:</strong> $${total.toLocaleString('es-CL')}</p>
  `;
  const win = window.open('', '', 'width=400,height=400');
  win.document.write(`<html><body>${boleta}</body></html>`);
  win.document.close();
};

window.generarBoletaPDF = function(idx) {
  const pedido = gestorPedidos.pedidos[idx];
  if (!pedido) return;

  const precio = obtenerPrecioPorNombre(pedido.nombre);
  const iva = Math.round(precio * 0.19);
  const total = precio + iva;

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  doc.setFontSize(16);
  doc.text("Boleta Restaurante", 20, 20);
  doc.setFontSize(12);
  doc.text(`Cliente: ${pedido.cliente || '-'}`, 20, 35);
  doc.text(`Mesa: ${pedido.mesa || '-'}`, 20, 45);
  doc.text(`Pedido: ${pedido.nombre || '-'}`, 20, 55);
  doc.text(`Subtotal: $${precio.toLocaleString('es-CL')}`, 20, 65);
  doc.text(`IVA (19%): $${iva.toLocaleString('es-CL')}`, 20, 75);
  doc.text(`Total: $${total.toLocaleString('es-CL')}`, 20, 85);

  doc.save(`boleta_${pedido.cliente || 'cliente'}_${Date.now()}.pdf`);
};

window.generarBoletaPDFMesa = function(mesa) {
  const pedidosMesa = gestorPedidos.pedidos.filter(p => p.estado === 'Listo' && p.mesa === mesa);
  if (!pedidosMesa.length) return;

  const cliente = pedidosMesa[0].cliente || '-';
  const pedidosNombres = pedidosMesa.map(p => p.nombre).join(', ');
  const subtotal = pedidosMesa.reduce((sum, p) => sum + obtenerPrecioPorNombre(p.nombre), 0);
  const iva = Math.round(subtotal * 0.19);
  const total = subtotal + iva;

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  // Encabezado
  doc.setFontSize(18);
  doc.setTextColor(255, 122, 0);
  doc.text("Boleta Restaurante", 105, 20, { align: "center" });

  doc.setDrawColor(255, 122, 0);
  doc.line(20, 25, 190, 25);

  // Datos principales
  doc.setFontSize(12);
  doc.setTextColor(40, 40, 40);
  doc.text(`Mesa:`, 20, 35);
  doc.text(`${mesa}`, 60, 35);
  doc.text(`Cliente(s):`, 20, 43);
  doc.text(`${cliente}`, 60, 43);

  doc.text(`Pedidos:`, 20, 51);
  doc.text(`${pedidosNombres}`, 60, 51);

  doc.line(20, 56, 190, 56);

  // Totales
  doc.setFontSize(13);
  doc.setTextColor(0, 0, 0);
  doc.text(`Subtotal:`, 20, 65);
  doc.text(`$${subtotal.toLocaleString('es-CL')}`, 60, 65);

  doc.text(`IVA (19%):`, 20, 73);
  doc.text(`$${iva.toLocaleString('es-CL')}`, 60, 73);

  doc.setFontSize(14);
  doc.setTextColor(255, 122, 0);
  doc.text(`TOTAL:`, 20, 83);
  doc.text(`$${total.toLocaleString('es-CL')}`, 60, 83);

  // Pie de página
  doc.setFontSize(11);
  doc.setTextColor(150, 150, 150);
  doc.text("Gracias por su preferencia", 105, 110, { align: "center" });

  doc.setFontSize(13);
  doc.setTextColor(255, 122, 0);
  doc.text("¡Vuelve pronto!", 105, 120, { align: "center" });

  doc.save(`boleta_mesa_${mesa}_${Date.now()}.pdf`);
};

async function mostrarIngredientes() {
  try {
    const ingredientes = await obtenerIngredientes();
    const tbody = document.getElementById('tablaIngredientes').querySelector('tbody');
    tbody.innerHTML = '';
    ingredientes.forEach(ing => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${ing.nombre || ''}</td>
        <td>${ing.cantidad ?? ''}</td>
        <td>${ing.unidad_medida || ''}</td>
        <td>${ing.categoria || ''}</td>
        <td>${ing.fecha_vencimiento ? new Date(ing.fecha_vencimiento).toLocaleDateString() : ''}</td>
        <td>${ing.nivel_critico ?? ''}</td>
        <td>${ing.tipo || ''}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    alert(e.message);
  }
}

// Llama a la función cuando se muestre la sección de inventario
document.addEventListener('DOMContentLoaded', mostrarIngredientes);

document.getElementById('formIngrediente').addEventListener('submit', async (e) => {
  e.preventDefault();
  const datos = {
    nombre: document.getElementById('nombreIngrediente').value,
    cantidad: document.getElementById('cantidadIngrediente').value,
    unidad_medida: document.getElementById('unidadMedidaIngrediente').value,
    categoria: document.getElementById('categoriaIngrediente').value,
    fecha_vencimiento: document.getElementById('fechaVencimientoIngrediente').value,
    nivel_critico: document.getElementById('nivelCriticoIngrediente').value,
    tipo: document.getElementById('tipoIngrediente').value
  };
  try {
    await crearIngrediente(datos);
    alert('Ingrediente creado correctamente');
    // Recarga la tabla de ingredientes si es necesario
  } catch (err) {
    alert(err.message);
  }
});

document.getElementById('btnMostrarIngredientes').addEventListener('click', mostrarIngredientes);

// --- Gestión de Clientes ---
async function mostrarClientes() {
  try {
    const clientes = await obtenerClientes();
    const tbody = document.getElementById('tablaClientes').querySelector('tbody');
    tbody.innerHTML = '';
    clientes.forEach(cliente => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${cliente.nombre || ''}</td>
        <td>${cliente.apellido || ''}</td>
        <td>${cliente.rut || ''}</td>
        <td>${cliente.mesa || ''}</td>
        <td>
          <button onclick="editarCliente('${cliente.id}')">Editar</button>
          <button onclick="eliminarCliente('${cliente.id}')">Eliminar</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
    window.clientes = clientes;
  } catch (e) {
    alert(e.message);
  }
}

document.getElementById('formCliente').addEventListener('submit', async (e) => {
  e.preventDefault();
  const datos = {
    nombre: document.getElementById('inputNombreCliente').value,
    apellido: document.getElementById('inputApellidoCliente').value,
    rut: document.getElementById('inputRutCliente').value,
    mesa: document.getElementById('selectMesaCliente').value
  };
  try {
    await crearCliente(datos);
    alert('Cliente agregado correctamente');
    mostrarClientes();
    e.target.reset();
  } catch (err) {
    alert(err.message);
  }
});

window.eliminarCliente = async function(id) {
  if (!confirm('¿Seguro que deseas eliminar este cliente?')) return;
  try {
    const res = await fetch(`http://localhost:8000/api/clientes/${id}/`, { method: 'DELETE' });
    if (res.status === 204) {
      alert('Cliente eliminado');
      mostrarClientes();
    } else {
      const error = await res.json();
      alert(error.error || 'Error al eliminar cliente');
    }
  } catch (err) {
    alert(err.message);
  }
};

window.editarCliente = function(id) {
  alert('Funcionalidad de edición de cliente no implementada aún.');
};

// Mostrar clientes al cargar la sección
document.addEventListener('DOMContentLoaded', mostrarClientes);

// (Opcional) Si tienes un botón para refrescar clientes:
const btnMostrarClientes = document.getElementById('btnMostrarClientes');
if (btnMostrarClientes) {
  btnMostrarClientes.addEventListener('click', mostrarClientes);
}

// --- Gestión de Usuarios ---

// Mostrar usuarios en la tabla
async function mostrarUsuarios() {
  try {
    const usuarios = await obtenerUsuarios();
    const tbody = document.getElementById('tablaUsuarios').querySelector('tbody');
    tbody.innerHTML = '';
    usuarios.forEach(usuario => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${usuario.rut || ''}</td>
        <td>${usuario.username || ''}</td>
        <td>${usuario.nombre || ''}</td>
        <td>${usuario.apellido || ''}</td>
        <td>${usuario.email || ''}</td>
        <td>${usuario.telefono || ''}</td>
        <td>${usuario.direccion || ''}</td>
        <td>${usuario.rol || ''}</td>
        <td>
          <button onclick="eliminarUsuario('${usuario.rut}')">Eliminar</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    alert(e.message);
  }
}

// Registrar usuario desde el formulario
document.getElementById('formUsuario').addEventListener('submit', async (e) => {
  e.preventDefault();
  const datos = {
    rut: document.getElementById('inputRutUsuario').value,
    username: document.getElementById('inputUsernameUsuario').value,
    nombre: document.getElementById('inputNombreUsuario').value,
    apellido: document.getElementById('inputApellidoUsuario').value,
    rol: document.getElementById('selectRolUsuario').value,
    email: document.getElementById('inputCorreoUsuario').value,
    telefono: document.getElementById('inputTelefonoUsuario').value || null,
    direccion: document.getElementById('inputDireccionUsuario').value || null,
    password: document.getElementById('inputPasswordUsuario').value
  };

  const res = await fetch('http://localhost:8000/api/usuarios/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(datos)
  });

  if (!res.ok) {
    const error = await res.json();
    console.log(error); // Aquí ves el response en la consola
  }
});

// Eliminar usuario
window.eliminarUsuario = async function(rut) {
  if (!confirm('¿Seguro que deseas eliminar este usuario?')) return;
  try {
    const res = await fetch(`http://localhost:8000/api/usuarios/${rut}/`, { method: 'DELETE' });
    if (res.status === 204) {
      alert('Usuario eliminado');
      mostrarUsuarios();
    } else {
      const error = await res.json();
      alert(error.error || 'Error al eliminar usuario');
    }
  } catch (err) {
    alert(err.message);
  }
};

// Mostrar usuarios al cargar la sección
document.addEventListener('DOMContentLoaded', mostrarUsuarios);

// --- FIN Gestión de Usuarios ---