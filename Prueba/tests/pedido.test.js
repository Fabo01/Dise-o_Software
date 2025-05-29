import { Pedido } from '../js/modeloPedido.js';

function testAvanzarEstado() {
  const pedido = new Pedido('Pizza');
  console.assert(pedido.estado === 'Pendiente', 'Estado inicial debe ser Pendiente');

  let avancado = pedido.avanzarEstado();
  console.assert(avancado === true, 'Debe avanzar de Pendiente a En Preparación');
  console.assert(pedido.estado === 'En Preparación', 'Estado debe ser En Preparación');

  avancado = pedido.avanzarEstado();
  console.assert(avancado === true, 'Debe avanzar de En Preparación a Listo');
  console.assert(pedido.estado === 'Listo', 'Estado debe ser Listo');

  avancado = pedido.avanzarEstado();
  console.assert(avancado === false, 'No debe avanzar más allá de Listo');
  console.assert(pedido.estado === 'Listo', 'Estado sigue siendo Listo');

  console.log('Tests de Pedido pasados.');
}

testAvanzarEstado();
