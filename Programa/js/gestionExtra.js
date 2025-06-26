let mesas = [];
let clientes = [];

const formMesa = document.getElementById('formMesa');
const inputMesa = document.getElementById('inputMesa');
const tablaMesas = document.getElementById('tablaMesas').querySelector('tbody');
const selectMesaCliente = document.getElementById('selectMesaCliente');

function renderMesas() {
    tablaMesas.innerHTML = '';
    selectMesaCliente.innerHTML = '<option value="">Asignar Mesa</option>';
    mesas.forEach((mesa, idx) => {
        // Render en tabla
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${mesa}</td>
            <td>
                <button onclick="eliminarMesa(${idx})">Eliminar</button>
            </td>
        `;
        tablaMesas.appendChild(tr);
        // Render en select
        selectMesaCliente.innerHTML += `<option value="${mesa}">${mesa}</option>`;
    });
}
window.eliminarMesa = function(idx) {
    // Si eliminas una mesa, desasigna de los clientes
    const mesaEliminada = mesas[idx];
    clientes = clientes.map(c => c.mesa === mesaEliminada ? { ...c, mesa: "" } : c);
    mesas.splice(idx, 1);
    renderMesas();
    renderClientes();
};

formMesa.addEventListener('submit', e => {
    e.preventDefault();
    const nombre = inputMesa.value.trim();
    if (nombre && !mesas.includes(nombre)) {
        mesas.push(nombre);
        inputMesa.value = '';
        renderMesas();
    }
});
renderMesas();

// --- Clientes ---
const formCliente = document.getElementById('formCliente');
const inputNombreCliente = document.getElementById('inputNombreCliente');
const inputApellidoCliente = document.getElementById('inputApellidoCliente');
const inputRutCliente = document.getElementById('inputRutCliente');
const tablaClientes = document.getElementById('tablaClientes').querySelector('tbody');

formCliente.addEventListener('submit', e => {
    e.preventDefault();
    const nombre = inputNombreCliente.value.trim();
    const apellido = inputApellidoCliente.value.trim();
    const rut = inputRutCliente.value.trim();
    const mesa = selectMesaCliente.value;
    if (nombre && apellido && rut && mesa && !clientes.some(c => c.rut === rut)) {
        clientes.push({ nombre, apellido, rut, mesa });
        inputNombreCliente.value = '';
        inputApellidoCliente.value = '';
        inputRutCliente.value = '';
        selectMesaCliente.value = '';
        renderClientes();
    }
});

function renderClientes() {
    tablaClientes.innerHTML = '';
    clientes.forEach((cliente, idx) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${cliente.nombre}</td>
            <td>${cliente.apellido}</td>
            <td>${cliente.rut}</td>
            <td>${cliente.mesa || '-'}</td>
            <td>
                <button onclick="eliminarCliente(${idx})">Eliminar</button>
            </td>
        `;
        tablaClientes.appendChild(tr);
    });
}
window.eliminarCliente = function(idx) {
    clientes.splice(idx, 1);
    renderClientes();
};

function actualizarSelectClientesPedido() {
    const select = document.getElementById('inputClientePedido');
    if (!select) return;
    select.innerHTML = '<option value="">Selecciona un cliente</option>';
    clientes.forEach((cliente, idx) => {
        select.innerHTML += `<option value="${cliente.rut}">${cliente.nombre} ${cliente.apellido} (Mesa: ${cliente.mesa || '-'})</option>`;
    });
}
window.actualizarSelectClientesPedido = actualizarSelectClientesPedido;
renderClientes = function() {
    tablaClientes.innerHTML = '';
    clientes.forEach((cliente, idx) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${cliente.nombre}</td>
            <td>${cliente.apellido}</td>
            <td>${cliente.rut}</td>
            <td>${cliente.mesa || '-'}</td>
            <td>
                <button onclick="eliminarCliente(${idx})">Eliminar</button>
            </td>
        `;
        tablaClientes.appendChild(tr);
    });
    actualizarSelectClientesPedido();
};
renderClientes();

window.clientes = clientes;