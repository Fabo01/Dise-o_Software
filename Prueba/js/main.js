import { GestorPedidos } from './gestorPedidos.js';
import { UI } from './ui.js';

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

function renderCuentas(pedidos) {
  const tabla = document.getElementById('tablaCuentas');
  const tbody = tabla.querySelector('tbody');
  const totalSpan = document.getElementById('totalCuentas');
  tbody.innerHTML = '';
  let total = 0;

  // Solo muestra pedidos con estado "Listo"
  pedidos.filter(p => p.estado === 'Listo').forEach(pedido => {
    const precio = obtenerPrecioPorNombre(pedido.nombre);
    total += precio;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${pedido.nombre}</td>
      <td>$${precio.toLocaleString('es-CL')}</td>
      <td>${pedido.estado}</td>
    `;
    tbody.appendChild(tr);
  });

  totalSpan.textContent = `$${total.toLocaleString('es-CL')}`;
}

// Suscribirse a los cambios de pedidos para actualizar la UI y las cuentas
gestorPedidos.subscribe((pedidos) => {
  ui.render(pedidos);
  renderCuentas(pedidos);
});

// Llama una vez al cargar la página para mostrar el estado inicial
document.addEventListener('DOMContentLoaded', () => {
  renderCuentas(gestorPedidos.pedidos);
});

class ClientePanel(ctk.CTkFrame) {
  constructor(parent, db, cliente_crud) {
    super(parent);
    this.db = db;
    this.cliente_crud = cliente_crud;
  }

  add_cliente() {
    // Usa self.cliente_crud en vez de ClienteCRUD
    const cliente_existente = this.cliente_crud.get_cliente_by_rut(this.db, rut);
  }
}
