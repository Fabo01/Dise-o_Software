import { Pedido } from './modeloPedido.js';

export class GestorPedidos {
  constructor() {
    this.pedidos = [];
    this.subscribers = [];
  }

  agregarPedido(nombre) {
    const pedido = new Pedido(nombre);
    this.pedidos.push(pedido);
    this.notify();
  }

  eliminarPedido(index) {
    this.pedidos.splice(index, 1);
    this.notify();
  }

  avanzarEstado(index) {
    const pedido = this.pedidos[index];
    if (pedido) {
      const cambio = pedido.avanzarEstado();
      this.notify();
      return cambio;
    }
    return false;
  }

  filtrarPorEstado(estado) {
    if (estado === 'Todos') return this.pedidos;
    return this.pedidos.filter(p => p.estado === estado);
  }

  subscribe(fn) {
    this.subscribers.push(fn);
  }

  notify() {
    this.subscribers.forEach(fn => fn(this.pedidos));
  }
}
