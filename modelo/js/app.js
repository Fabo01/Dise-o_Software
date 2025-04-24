// Clase principal de la aplicación
class RestaurantApp {
    constructor() {
        this.db = new DatabaseAPI();
        this.ui = new UIComponents();
        this.currentPanel = null;
        
        // Paneles disponibles
        this.panels = {
            'clientes': new ClientePanel(this.db, this.ui),
            'ingredientes': new IngredientePanel(this.db, this.ui),
            'menus': new MenuPanel(this.db, this.ui),
            'compras': new PanelCompra(this.db, this.ui),
            'pedidos': new PanelPedido(this.db, this.ui),
            'graficos': new GraficosPanel(this.db, this.ui)
        };
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        // Navegación del sidebar
        document.querySelectorAll('[data-panel]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const panelName = e.target.getAttribute('data-panel') || 
                                 e.target.parentElement.getAttribute('data-panel');
                this.loadPanel(panelName);
            });
        });
        
        // Cerrar modal
        document.querySelector('.close-modal').addEventListener('click', () => {
            this.ui.hideModal();
        });
    }
    
    loadPanel(panelName) {
        if (this.currentPanel) {
            this.currentPanel.onLeave();
        }
        
        this.currentPanel = this.panels[panelName];
        this.currentPanel.render();
        
        // Actualizar clase activa en el menú
        document.querySelectorAll('.nav-menu a').forEach(link => {
            link.classList.remove('active');
        });
        
        document.querySelector(`[data-panel="${panelName}"]`).classList.add('active');
    }
}

// Clase base para todos los paneles
class Panel {
    constructor(db, ui) {
        this.db = db;
        this.ui = ui;
    }
    
    render() {
        // Método abstracto, debe ser implementado por las subclases
        throw new Error('Método render() debe ser implementado');
    }
    
    onLeave() {
        // Opcional: limpieza al salir del panel
    }
}

// Implementación de los paneles (ejemplo con ClientePanel)
class ClientePanel extends Panel {
    constructor(db, ui) {
        super(db, ui);
        this.selectedClientId = null;
    }
    
    render() {
        const clientes = this.db.getClientes();
        
        const html = `
            <div class="panel">
                <h2 class="panel-title">Gestión de Clientes</h2>
                
                <div class="panel-actions">
                    <button id="add-cliente" class="btn">Agregar Cliente</button>
                    <button id="edit-cliente" class="btn" ${!this.selectedClientId ? 'disabled' : ''}>Editar</button>
                    <button id="delete-cliente" class="btn btn-danger" ${!this.selectedClientId ? 'disabled' : ''}>Eliminar</button>
                </div>
                
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>RUT</th>
                                <th>Nombre</th>
                                <th>Email</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${clientes.map(cliente => `
                                <tr data-id="${cliente.rut}" class="${this.selectedClientId === cliente.rut ? 'selected' : ''}">
                                    <td>${cliente.rut}</td>
                                    <td>${cliente.nombre}</td>
                                    <td>${cliente.email}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
        
        document.getElementById('panel-container').innerHTML = html;
        
        // Event listeners
        document.getElementById('add-cliente').addEventListener('click', () => this.showAddForm());
        document.getElementById('edit-cliente').addEventListener('click', () => this.showEditForm());
        document.getElementById('delete-cliente').addEventListener('click', () => this.deleteCliente());
        
        // Selección de fila
        document.querySelectorAll('.table tbody tr').forEach(row => {
            row.addEventListener('click', () => {
                document.querySelectorAll('.table tbody tr').forEach(r => r.classList.remove('selected'));
                row.classList.add('selected');
                this.selectedClientId = row.getAttribute('data-id');
                document.getElementById('edit-cliente').disabled = false;
                document.getElementById('delete-cliente').disabled = false;
            });
        });
    }
    
    showAddForm() {
        const formHtml = `
            <div class="form-group">
                <label for="rut">RUT</label>
                <input type="text" id="rut" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="nombre">Nombre</label>
                <input type="text" id="nombre" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" class="form-control" required>
            </div>
            <button id="save-cliente" class="btn">Guardar</button>
        `;
        
        this.ui.showModal('Agregar Cliente', formHtml);
        
        document.getElementById('save-cliente').addEventListener('click', () => {
            const rut = document.getElementById('rut').value;
            const nombre = document.getElementById('nombre').value;
            const email = document.getElementById('email').value;
            
            if (!rut || !nombre || !email) {
                this.ui.showAlert('Todos los campos son obligatorios', 'error');
                return;
            }
            
            const result = this.db.addCliente({ rut, nombre, email });
            if (result) {
                this.ui.showAlert('Cliente agregado correctamente');
                this.ui.hideModal();
                this.render(); // Refrescar la lista
            } else {
                this.ui.showAlert('Error al agregar cliente', 'error');
            }
        });
    }
    
    showEditForm() {
        if (!this.selectedClientId) return;
        
        const cliente = this.db.getClienteByRut(this.selectedClientId);
        if (!cliente) return;
        
        const formHtml = `
            <div class="form-group">
                <label for="rut">RUT</label>
                <input type="text" id="rut" class="form-control" value="${cliente.rut}" readonly>
            </div>
            <div class="form-group">
                <label for="nombre">Nombre</label>
                <input type="text" id="nombre" class="form-control" value="${cliente.nombre}" required>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" class="form-control" value="${cliente.email}" required>
            </div>
            <button id="update-cliente" class="btn">Actualizar</button>
        `;
        
        this.ui.showModal('Editar Cliente', formHtml);
        
        document.getElementById('update-cliente').addEventListener('click', () => {
            const nombre = document.getElementById('nombre').value;
            const email = document.getElementById('email').value;
            
            if (!nombre || !email) {
                this.ui.showAlert('Todos los campos son obligatorios', 'error');
                return;
            }
            
            const result = this.db.updateCliente(this.selectedClientId, { nombre, email });
            if (result) {
                this.ui.showAlert('Cliente actualizado correctamente');
                this.ui.hideModal();
                this.render(); // Refrescar la lista
            } else {
                this.ui.showAlert('Error al actualizar cliente', 'error');
            }
        });
    }
    
    deleteCliente() {
        if (!this.selectedClientId) return;
        
        this.ui.showConfirm(
            '¿Estás seguro de eliminar este cliente?',
            () => {
                const result = this.db.deleteCliente(this.selectedClientId);
                if (result) {
                    this.ui.showAlert('Cliente eliminado correctamente');
                    this.selectedClientId = null;
                    this.render(); // Refrescar la lista
                } else {
                    this.ui.showAlert('Error al eliminar cliente', 'error');
                }
            }
        );
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    const app = new RestaurantApp();
});

class IngredientePanel extends Panel {
    constructor(db, ui) {
        super(db, ui);
        this.selectedId = null;
    }

    render() {
        const ingredientes = this.db.getIngredientes(); // Simulado o real

        const html = `
            <div class="panel">
                <h2 class="panel-title">Gestión de Ingredientes</h2>

                <div class="panel-actions">
                    <button id="add-ingrediente" class="btn">Agregar Ingrediente</button>
                    <button id="edit-ingrediente" class="btn" ${!this.selectedId ? 'disabled' : ''}>Editar</button>
                    <button id="delete-ingrediente" class="btn btn-danger" ${!this.selectedId ? 'disabled' : ''}>Eliminar</button>
                </div>

                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Stock</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${ingredientes.map(i => `
                            <tr data-id="${i.id}" class="${this.selectedId === i.id ? 'selected' : ''}">
                                <td>${i.id}</td>
                                <td>${i.nombre}</td>
                                <td>${i.stock}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;

        document.getElementById('panel-container').innerHTML = html;

        document.getElementById('add-ingrediente').addEventListener('click', () => this.showAddForm());
        document.getElementById('edit-ingrediente').addEventListener('click', () => this.showEditForm());
        document.getElementById('delete-ingrediente').addEventListener('click', () => this.deleteIngrediente());

        document.querySelectorAll('.table tbody tr').forEach(row => {
            row.addEventListener('click', () => {
                document.querySelectorAll('.table tbody tr').forEach(r => r.classList.remove('selected'));
                row.classList.add('selected');
                this.selectedId = row.getAttribute('data-id');
                document.getElementById('edit-ingrediente').disabled = false;
                document.getElementById('delete-ingrediente').disabled = false;
            });
        });
    }

    showAddForm() {
        const formHtml = `
            <div class="form-group">
                <label for="nombre">Nombre</label>
                <input type="text" id="nombre" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="stock">Stock</label>
                <input type="number" id="stock" class="form-control" required>
            </div>
            <button id="save-ingrediente" class="btn">Guardar</button>
        `;
        this.ui.showModal('Agregar Ingrediente', formHtml);

        document.getElementById('save-ingrediente').addEventListener('click', () => {
            const nombre = document.getElementById('nombre').value;
            const stock = parseInt(document.getElementById('stock').value);
            if (!nombre || isNaN(stock)) {
                this.ui.showAlert('Campos inválidos', 'error');
                return;
            }

            const result = this.db.addIngrediente({ nombre, stock });
            if (result) {
                this.ui.showAlert('Ingrediente agregado');
                this.ui.hideModal();
                this.render();
            } else {
                this.ui.showAlert('Error al guardar', 'error');
            }
        });
    }

    showEditForm() {
        if (!this.selectedId) return;
        const ingrediente = this.db.getIngredienteById(this.selectedId);
        const formHtml = `
            <div class="form-group">
                <label for="nombre">Nombre</label>
                <input type="text" id="nombre" class="form-control" value="${ingrediente.nombre}" required>
            </div>
            <div class="form-group">
                <label for="stock">Stock</label>
                <input type="number" id="stock" class="form-control" value="${ingrediente.stock}" required>
            </div>
            <button id="update-ingrediente" class="btn">Actualizar</button>
        `;
        this.ui.showModal('Editar Ingrediente', formHtml);

        document.getElementById('update-ingrediente').addEventListener('click', () => {
            const nombre = document.getElementById('nombre').value;
            const stock = parseInt(document.getElementById('stock').value);
            if (!nombre || isNaN(stock)) {
                this.ui.showAlert('Campos inválidos', 'error');
                return;
            }

            const result = this.db.updateIngrediente(this.selectedId, { nombre, stock });
            if (result) {
                this.ui.showAlert('Ingrediente actualizado');
                this.ui.hideModal();
                this.render();
            } else {
                this.ui.showAlert('Error al actualizar', 'error');
            }
        });
    }

    deleteIngrediente() {
        if (!this.selectedId) return;
        this.ui.showConfirm('¿Eliminar ingrediente?', () => {
            const result = this.db.deleteIngrediente(this.selectedId);
            if (result) {
                this.ui.showAlert('Ingrediente eliminado');
                this.selectedId = null;
                this.render();
            } else {
                this.ui.showAlert('Error al eliminar', 'error');
            }
        });
    }
}
