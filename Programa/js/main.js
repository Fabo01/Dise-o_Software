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
      <td><button onclick="generarBoletaPDFMesa('${mesa}')">Boleta PDF</button></td>
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
    const nombre = this.elementos.inputPedido.value.trim();
    const selectCliente = document.getElementById('inputClientePedido');
    const rutCliente = selectCliente.value;
    const clienteObj = window.clientes?.find(c => c.rut === rutCliente);
    if (nombre && clienteObj) {
      this.gestorPedidos.agregarPedido({
        nombre, // nombre del producto
        cliente: clienteObj.nombre + ' ' + clienteObj.apellido,
        mesa: clienteObj.mesa // <-- aquí debe ir el nombre de la mesa asignada al cliente
      });
      this.elementos.inputPedido.value = '';
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
  const cuenta = gestorCuentas.cuentas[idx]; // Ajusta según tu estructura
  if (!cuenta) return;

  // Datos de ejemplo, ajusta según tu modelo real
  const cliente = cuenta.cliente || '-';
  const mesa = cuenta.mesa || '-';
  const pedido = cuenta.pedido || '-';
  const precio = cuenta.precio || 10000; // CLP
  const iva = Math.round(precio * 0.19);
  const total = precio + iva;

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF();

  doc.setFontSize(16);
  doc.text("Boleta Restaurante", 20, 20);
  doc.setFontSize(12);
  doc.text(`Cliente: ${cliente}`, 20, 35);
  doc.text(`Mesa: ${mesa}`, 20, 45);
  doc.text(`Pedido: ${pedido}`, 20, 55);
  doc.text(`Subtotal: $${precio.toLocaleString('es-CL')}`, 20, 65);
  doc.text(`IVA (19%): $${iva.toLocaleString('es-CL')}`, 20, 75);
  doc.text(`Total: $${total.toLocaleString('es-CL')}`, 20, 85);

  doc.save(`boleta_${cliente}_${Date.now()}.pdf`);
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
  doc.text("exclaviza rappi", 105, 120, { align: "center" });

  doc.save(`boleta_mesa_${mesa}_${Date.now()}.pdf`);
};
