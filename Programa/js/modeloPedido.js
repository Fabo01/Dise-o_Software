export class Pedido {
  constructor(nombre) {
    this.nombre = nombre;
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
