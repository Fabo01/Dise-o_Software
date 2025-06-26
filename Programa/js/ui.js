export class UI {
  constructor(gestorPedidos, elementos) {
    this.gestorPedidos = gestorPedidos;
    this.elementos = elementos;

    this.gestorPedidos.subscribe(this.render.bind(this));

    this.elementos.form.addEventListener('submit', this.handleAgregarPedido.bind(this));
    this.elementos.filtroEstado.addEventListener('change', this.handleFiltro.bind(this));

    this.render(this.gestorPedidos.pedidos);
  }

  handleAgregarPedido(event) {
    event.preventDefault();
    const nombre = this.elementos.inputPedido.value.trim();
    if (nombre) {
      this.gestorPedidos.agregarPedido(nombre);
      this.elementos.inputPedido.value = '';
    }
  }

  handleFiltro() {
    this.render(this.gestorPedidos.pedidos);
  }

  render(_pedidos) {
    const filtro = this.elementos.filtroEstado.value;
    const pedidosFiltrados = this.gestorPedidos.filtrarPorEstado(filtro);

    const tbody = this.elementos.tablaPedidos.querySelector('tbody');
    tbody.innerHTML = '';

    pedidosFiltrados.forEach((pedido) => {
      const fila = document.createElement('tr');

      const tdPedido = document.createElement('td');
      tdPedido.textContent = pedido.nombre;
      fila.appendChild(tdPedido);

      const tdEstado = document.createElement('td');
      tdEstado.textContent = pedido.estado;
      fila.appendChild(tdEstado);

      const tdAcciones = document.createElement('td');

      const indiceOriginal = this.gestorPedidos.pedidos.indexOf(pedido);

      if (pedido.estado !== 'Listo') {
        const btnAvanzar = document.createElement('button');
        btnAvanzar.textContent = 'Avanzar Estado';
        btnAvanzar.addEventListener('click', () => {
          this.gestorPedidos.avanzarEstado(indiceOriginal);
        });
        tdAcciones.appendChild(btnAvanzar);
      }

      const btnEliminar = document.createElement('button');
      btnEliminar.textContent = 'Eliminar';
      btnEliminar.addEventListener('click', () => {
        this.gestorPedidos.eliminarPedido(indiceOriginal);
      });
      tdAcciones.appendChild(btnEliminar);

      fila.appendChild(tdAcciones);

      tbody.appendChild(fila);
    });

    // Actualizar estadísticas
    this.elementos.totalPedidos.textContent = this.gestorPedidos.pedidos.length;
    this.elementos.countPendientes.textContent = this.gestorPedidos.pedidos.filter(p => p.estado === 'Pendiente').length;
    this.elementos.countPreparacion.textContent = this.gestorPedidos.pedidos.filter(p => p.estado === 'En Preparación').length;
    this.elementos.countListos.textContent = this.gestorPedidos.pedidos.filter(p => p.estado === 'Listo').length;

    // Actualizar resumen
    this.actualizarResumenDashboard();

    // Renderizar pedidos listos en la sección "listos"
    const tablaListos = document.getElementById('tablaListos');
    if (tablaListos) {
      const tbodyListos = tablaListos.querySelector('tbody');
      tbodyListos.innerHTML = '';

      const pedidosListos = this.gestorPedidos.pedidos.filter(p => p.estado === 'Listo');
      pedidosListos.forEach((pedido, index) => {
        const fila = document.createElement('tr');

        const tdPedido = document.createElement('td');
        tdPedido.textContent = pedido.nombre;
        fila.appendChild(tdPedido);

        const tdEstado = document.createElement('td');
        tdEstado.textContent = pedido.estado;
        fila.appendChild(tdEstado);

        const tdAcciones = document.createElement('td');
        const btnEliminar = document.createElement('button');
        btnEliminar.textContent = 'Eliminar';
        btnEliminar.addEventListener('click', () => {
          const idx = this.gestorPedidos.pedidos.indexOf(pedido);
          this.gestorPedidos.eliminarPedido(idx);
        });
        tdAcciones.appendChild(btnEliminar);

        fila.appendChild(tdAcciones);
        tbodyListos.appendChild(fila);
      });
    }

    // Renderizar pedidos en preparación en la sección "preparacion"
    const tablaPreparacion = document.getElementById('tablaPreparacion');
    if (tablaPreparacion) {
      const tbodyPreparacion = tablaPreparacion.querySelector('tbody');
      tbodyPreparacion.innerHTML = '';

      const pedidosPreparacion = this.gestorPedidos.pedidos.filter(p => p.estado === 'En Preparación');
      pedidosPreparacion.forEach((pedido) => {
        const fila = document.createElement('tr');

        const tdPedido = document.createElement('td');
        tdPedido.textContent = pedido.nombre;
        fila.appendChild(tdPedido);

        const tdEstado = document.createElement('td');
        tdEstado.textContent = pedido.estado;
        fila.appendChild(tdEstado);

        const tdAcciones = document.createElement('td');
        // Botón para avanzar a "Listo"
        const btnAvanzar = document.createElement('button');
        btnAvanzar.textContent = 'Marcar como Listo';
        btnAvanzar.addEventListener('click', () => {
          const idx = this.gestorPedidos.pedidos.indexOf(pedido);
          this.gestorPedidos.avanzarEstado(idx);
        });
        tdAcciones.appendChild(btnAvanzar);

        // Botón para eliminar
        const btnEliminar = document.createElement('button');
        btnEliminar.textContent = 'Eliminar';
        btnEliminar.addEventListener('click', () => {
          const idx = this.gestorPedidos.pedidos.indexOf(pedido);
          this.gestorPedidos.eliminarPedido(idx);
        });
        tdAcciones.appendChild(btnEliminar);

        fila.appendChild(tdAcciones);
        tbodyPreparacion.appendChild(fila);
      });
    }

    this.actualizarPedidosRecientes();
  }

  actualizarResumenDashboard() {
    const pedidos = this.gestorPedidos.pedidos;

    const pendientes = pedidos.filter(p => p.estado === 'Pendiente').length;
    const preparacion = pedidos.filter(p => p.estado === 'En Preparación').length;
    const listos = pedidos.filter(p => p.estado === 'Listo').length;

    this.elementos.resumenPendientes.textContent = pendientes;
    this.elementos.resumenPreparacion.textContent = preparacion;
    this.elementos.resumenListos.textContent = listos;

    this.actualizarPedidosRecientes();
  }

  actualizarPedidosRecientes() {
    const lista = document.getElementById('listaPedidosRecientes');
    if (!lista) return;
    // Toma los últimos 5 pedidos (del más reciente al más antiguo)
    const recientes = this.gestorPedidos.pedidos.slice(-5).reverse();
    lista.innerHTML = '';
    recientes.forEach(pedido => {
      const li = document.createElement('li');
      li.innerHTML = `<span>${pedido.nombre}</span> <span style="color:#ff7a00;font-weight:600;">${pedido.estado}</span>`;
      lista.appendChild(li);
    });
  }
}
