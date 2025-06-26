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
    const selectCliente = document.getElementById('inputClientePedido');
    const rutCliente = selectCliente.value;
    // clientes es global en gestionExtra.js
    const clienteObj = window.clientes?.find(c => c.rut === rutCliente);
    if (nombre && clienteObj) {
      console.log('Pedido creado:', {
        nombre,
        cliente: clienteObj.nombre + ' ' + clienteObj.apellido,
        mesa: clienteObj.mesa
      });
      this.gestorPedidos.agregarPedido({
        nombre,
        cliente: clienteObj.nombre + ' ' + clienteObj.apellido,
        mesa: clienteObj.mesa
      });
      this.elementos.inputPedido.value = '';
      selectCliente.value = '';
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

      const tdCliente = document.createElement('td');
      tdCliente.textContent = pedido.cliente || '-';
      fila.appendChild(tdCliente);

      const tdMesa = document.createElement('td');
      tdMesa.textContent = pedido.mesa || '-';
      fila.appendChild(tdMesa);

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

    // Renderizar tabla de cuentas agrupada por mesa
    const tablaCuentas = document.getElementById('tablaCuentas');
    if (tablaCuentas) {
      const tbodyCuentas = tablaCuentas.querySelector('tbody');
      tbodyCuentas.innerHTML = '';

      // Agrupa pedidos "Listo" por mesa
      const cuentasPorMesa = {};
      this.gestorPedidos.pedidos
        .filter(p => p.estado === 'Listo')
        .forEach(pedido => {
          const mesa = pedido.mesa || 'Sin mesa';
          if (!cuentasPorMesa[mesa]) cuentasPorMesa[mesa] = [];
          cuentasPorMesa[mesa].push(pedido);
        });

      Object.entries(cuentasPorMesa).forEach(([mesa, pedidosMesa]) => {
        // Nombres de los productos listos en esa mesa
        const pedidosNombres = pedidosMesa.map(p => p.nombre).join(', ');
        // Suma de precios de los productos listos en esa mesa
        const subtotal = pedidosMesa.reduce((sum, p) => {
          return sum + (window.obtenerPrecioPorNombre ? window.obtenerPrecioPorNombre(p.nombre) : 0);
        }, 0);

        // CREA la fila y asigna los datos en el orden correcto
        const fila = document.createElement('tr');

        // Mesa
        const tdMesa = document.createElement('td');
        tdMesa.textContent = mesa;
        fila.appendChild(tdMesa);

        // Pedidos
        const tdPedidos = document.createElement('td');
        tdPedidos.textContent = pedidosNombres;
        fila.appendChild(tdPedidos);

        // Subtotal
        const tdSubtotal = document.createElement('td');
        tdSubtotal.textContent = `$${subtotal.toLocaleString('es-CL')}`;
        fila.appendChild(tdSubtotal);

        // Acciones
        const tdAcciones = document.createElement('td');
        const btnBoleta = document.createElement('button');
        btnBoleta.textContent = 'Boleta PDF';
        btnBoleta.onclick = () => window.generarBoletaPDFMesa(mesa);
        tdAcciones.appendChild(btnBoleta);
        fila.appendChild(tdAcciones);

        tbodyCuentas.appendChild(fila);
      });
    }
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
