document.querySelectorAll('.nav-link').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.section;

    document.querySelectorAll('.seccion').forEach(sec => {
      sec.classList.add('oculto');
    });

    document.getElementById(target).classList.remove('oculto');
  });
});
import { GestorPedidos } from './gestorPedidos.js';

const gestor = new GestorPedidos();

// Simulación: si ya usas un gestor existente, reemplaza esto con el correcto
function actualizarDashboard() {
  const pedidos = gestor.obtenerPedidos();

  const pendientes = pedidos.filter(p => p.estado === 'Pendiente').length;
  const preparacion = pedidos.filter(p => p.estado === 'En Preparación').length;
  const listos = pedidos.filter(p => p.estado === 'Listo').length;

  document.getElementById('resumenPendientes').textContent = pendientes;
  document.getElementById('resumenPreparacion').textContent = preparacion;
  document.getElementById('resumenListos').textContent = listos;
}

// Llama a esta función cada vez que se actualicen los pedidos o al cargar
document.addEventListener('DOMContentLoaded', actualizarDashboard);
