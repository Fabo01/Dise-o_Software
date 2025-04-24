class DatabaseAPI {
    constructor() {
        // Datos de ejemplo (en una app real, aquí irían las llamadas a una API real)
        this.clientes = [
            { rut: '12345678-9', nombre: 'Juan Pérez', email: 'juan@example.com' },
            { rut: '98765432-1', nombre: 'María González', email: 'maria@example.com' }
        ];
        
        this.ingredientes = [
            { id: 1, nombre: 'Tomate', tipo: 'Vegetal', cantidad: 50, unidad: 'kg' },
            { id: 2, nombre: 'Carne', tipo: 'Proteína', cantidad: 30, unidad: 'kg' }
        ];
        
        this.menus = [
            { 
                id: 1, 
                nombre: 'Menú Clásico', 
                descripcion: 'Hamburguesa con papas fritas', 
                precio: 5990,
                ingredientes: [
                    { ingredienteId: 1, cantidad: 0.2 },
                    { ingredienteId: 2, cantidad: 0.3 }
                ]
            }
        ];
        
        this.pedidos = [];
    }
    
    // Métodos para clientes
    getClientes() {
        return [...this.clientes];
    }
    
    getClienteByRut(rut) {
        return this.clientes.find(c => c.rut === rut);
    }
    
    addCliente(cliente) {
        if (this.getClienteByRut(cliente.rut)) {
            return false;
        }
        this.clientes.push(cliente);
        return true;
    }
    
    updateCliente(rut, updates) {
        const index = this.clientes.findIndex(c => c.rut === rut);
        if (index === -1) return false;
        
        this.clientes[index] = { ...this.clientes[index], ...updates };
        return true;
    }
    
    deleteCliente(rut) {
        const index = this.clientes.findIndex(c => c.rut === rut);
        if (index === -1) return false;
        
        this.clientes.splice(index, 1);
        return true;
    }
    
    // Métodos para ingredientes, menús, pedidos...
    // (Implementación similar a los métodos de clientes)
}