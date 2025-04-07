"""
Script para inicializar la base de datos con datos de ejemplo
"""
from models import db_session, init_db
from models.usuario import Usuario
from models.cliente import Cliente
from models.ingrediente import Ingrediente
from models.menu import Menu
from models.mesa import Mesa
from models.pedido import DeliveryApp, MedioPago

def create_initial_data():
    # Inicializar las tablas
    init_db()
    
    # Crear usuarios
    print("Creando usuarios...")
    admin = Usuario(
        username="admin",
        password="admin123",
        nombre="Administrador",
        apellido="Sistema",
        rol="admin",
        email="admin@restaurante.com"
    )
    
    jefe_local = Usuario(
        username="jefe_local",
        password="local123",
        nombre="Carlos",
        apellido="Rodríguez",
        rol="jefe_local",
        email="carlos@restaurante.com",
        telefono="912345678"
    )
    
    mesero1 = Usuario(
        username="mesero1",
        password="mesa123",
        nombre="Ana",
        apellido="Martínez",
        rol="mesero",
        email="ana@restaurante.com"
    )
    
    cocina1 = Usuario(
        username="cocina1",
        password="cocina123",
        nombre="Pedro",
        apellido="Gómez",
        rol="cocina",
        email="pedro@restaurante.com"
    )
    
    db_session.add_all([admin, jefe_local, mesero1, cocina1])
    
    # Crear clientes
    print("Creando clientes...")
    cliente1 = Cliente(
        rut="12345678-9",
        nombre="María Pérez",
        telefono="987654321",
        direccion="Av. Principal 123",
        correo="maria@gmail.com"
    )
    
    cliente2 = Cliente(
        rut="98765432-1",
        nombre="Juan Soto",
        telefono="912345678",
        direccion="Calle Secundaria 456",
        correo="juan@gmail.com"
    )
    
    db_session.add_all([cliente1, cliente2])
    
    # Crear ingredientes
    print("Creando ingredientes...")
    tomate = Ingrediente(
        nombre="Tomate",
        categoria="Verduras",
        cantidad=10.0,
        unidad="kg",
        nivel_critico=2.0,
        costo_unitario=1500  # por kg
    )
    
    queso = Ingrediente(
        nombre="Queso Mozzarella",
        categoria="Lácteos",
        cantidad=5.0,
        unidad="kg",
        nivel_critico=1.0,
        costo_unitario=8000  # por kg
    )
    
    harina = Ingrediente(
        nombre="Harina",
        categoria="Secos",
        cantidad=20.0,
        unidad="kg",
        nivel_critico=5.0,
        costo_unitario=900  # por kg
    )
    
    aceite = Ingrediente(
        nombre="Aceite de Oliva",
        categoria="Aceites",
        cantidad=3.0,
        unidad="l",
        nivel_critico=0.5,
        costo_unitario=6000  # por litro
    )
    
    db_session.add_all([tomate, queso, harina, aceite])
    
    # Crear menús
    print("Creando menús...")
    pizza = Menu(
        nombre="Pizza Margarita",
        descripcion="Pizza tradicional con tomate, mozzarella y albahaca",
        precio=8900,
        categoria="Pizzas",
        tiempo_preparacion=15
    )
    
    pasta = Menu(
        nombre="Spaghetti al Pomodoro",
        descripcion="Pasta con salsa de tomate casera y albahaca",
        precio=7500,
        categoria="Pastas",
        tiempo_preparacion=12
    )
    
    ensalada = Menu(
        nombre="Ensalada Mediterránea",
        descripcion="Ensalada fresca con tomate, queso feta y aceitunas",
        precio=5900,
        categoria="Ensaladas",
        tiempo_preparacion=8
    )
    
    db_session.add_all([pizza, pasta, ensalada])
    db_session.flush()  # Para obtener IDs
    
    # Agregar ingredientes a los menús
    print("Asignando ingredientes a menús...")
    pizza.agregar_ingrediente(tomate, 0.3)
    pizza.agregar_ingrediente(queso, 0.2)
    pizza.agregar_ingrediente(harina, 0.25)
    
    pasta.agregar_ingrediente(tomate, 0.2)
    pasta.agregar_ingrediente(aceite, 0.05)
    
    ensalada.agregar_ingrediente(tomate, 0.2)
    ensalada.agregar_ingrediente(aceite, 0.03)
    
    # Crear mesas
    print("Creando mesas...")
    for i in range(1, 11):
        capacidad = 2 if i <= 4 else (4 if i <= 8 else 6)
        ubicacion = "Terraza" if i <= 5 else "Interior"
        
        mesa = Mesa(
            numero=i,
            capacidad=capacidad,
            ubicacion=ubicacion
        )
        db_session.add(mesa)
    
    # Crear apps de delivery
    print("Configurando apps de delivery...")
    rappi = DeliveryApp(
        nombre="Rappi",
        comision=0.25,
        activa=True
    )
    
    uber_eats = DeliveryApp(
        nombre="Uber Eats",
        comision=0.27,
        activa=True
    )
    
    pedidos_ya = DeliveryApp(
        nombre="PedidosYa",
        comision=0.23,
        activa=True
    )
    
    db_session.add_all([rappi, uber_eats, pedidos_ya])
    
    # Crear medios de pago
    print("Configurando medios de pago...")
    efectivo = MedioPago(
        nombre="Efectivo",
        tipo="efectivo",
        comision=0.0
    )
    
    tarjeta = MedioPago(
        nombre="Tarjeta de Crédito/Débito",
        tipo="tarjeta",
        comision=0.03
    )
    
    transferencia = MedioPago(
        nombre="Transferencia Bancaria",
        tipo="transferencia",
        comision=0.01
    )
    
    db_session.add_all([efectivo, tarjeta, transferencia])
    
    # Guardar todos los cambios
    db_session.commit()
    print("Base de datos inicializada correctamente!")

if __name__ == "__main__":
    create_initial_data()
