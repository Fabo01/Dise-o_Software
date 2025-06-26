export class Pedido {
  constructor({nombre, cliente, mesa}) {
    this.nombre = nombre;
    this.cliente = cliente;
    this.mesa = mesa;
    this.estado = 'Pendiente'; // Estado inicial
  }

  avanzarEstado() {
    if (this.estado === 'Pendiente') {
      this.estado = 'En Preparación';
      return true;
    }
    if (this.estado === 'En Preparación') {
      this.estado = 'Listo';
      return true;
    }
    return false; // Ya está en 'Listo'
  }
}
