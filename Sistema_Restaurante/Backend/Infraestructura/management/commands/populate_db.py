from django.core.management.base import BaseCommand
from decimal import Decimal
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
from Backend.Infraestructura.Modelos.Mesa_Modelo import MesaModelo
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo
from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo
from Backend.Infraestructura.Modelos.Pedido_Modelo import PedidoModelo, ItemPedidoModelo
from Backend.Infraestructura.Modelos.MedioPago_Modelo import MedioPagoModelo
from Backend.Infraestructura.Modelos.DeliveryApp_Modelo import DeliveryAppModelo

class Command(BaseCommand):
    help = 'Poblar la base de datos con datos de prueba'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Iniciando población de la base de datos...")
        
        # Crear clientes con RUTs válidos
        clientes = [
            {
                'nombre': 'Juan Pérez',
                'rut': '11111111-1',
                'correo': 'juan.perez@email.com',
                'telefono': '+56 9 8765 4321',
                'direccion': 'Av. Providencia 123, Santiago'
            },
            {
                'nombre': 'María González',
                'rut': '22222222-2',
                'correo': 'maria.gonzalez@email.com',
                'telefono': '+56 9 1234 5678',
                'direccion': 'Calle Los Leones 456, Las Condes'
            },
            {
                'nombre': 'Carlos Rodríguez',
                'rut': '12345678-5',
                'correo': 'carlos.rodriguez@email.com',
                'telefono': '+56 9 5555 5555',
                'direccion': 'Av. Apoquindo 789, Las Condes'
            }
        ]
        
        for cliente_data in clientes:
            cliente, created = ClienteModelo.objects.get_or_create(
                rut=cliente_data['rut'],
                defaults=cliente_data
            )
            if created:
                self.stdout.write(f"✅ Cliente creado: {cliente.nombre}")

        # Crear mesas con tipos y capacidades válidas
        mesas = [
            {'numero': '1', 'capacidad': 1, 'tipo_mesa': 'individual', 'estado': 'libre'},
            {'numero': '2', 'capacidad': 3, 'tipo_mesa': 'pequeña', 'estado': 'libre'},
            {'numero': '3', 'capacidad': 5, 'tipo_mesa': 'mediana', 'estado': 'libre'},
            {'numero': '4', 'capacidad': 7, 'tipo_mesa': 'grande', 'estado': 'libre'},
            {'numero': '5', 'capacidad': 10, 'tipo_mesa': 'familiar', 'estado': 'libre'},
            {'numero': '6', 'capacidad': 4, 'tipo_mesa': 'vip', 'estado': 'libre'},
        ]
        
        for mesa_data in mesas:
            mesa, created = MesaModelo.objects.get_or_create(
                numero=mesa_data['numero'],
                defaults=mesa_data
            )
            if created:
                self.stdout.write(f"✅ Mesa creada: Mesa {mesa.numero}")

        # Crear ingredientes
        ingredientes = [
            {'nombre': 'Tomate', 'cantidad': 50, 'categoria': 'Verduras', 'unidad_medida': 'kg', 'nivel_critico': 5},
            {'nombre': 'Cebolla', 'cantidad': 30, 'categoria': 'Verduras', 'unidad_medida': 'kg', 'nivel_critico': 3},
            {'nombre': 'Carne de Res', 'cantidad': 25, 'categoria': 'Carnes', 'unidad_medida': 'kg', 'nivel_critico': 5},
            {'nombre': 'Pollo', 'cantidad': 20, 'categoria': 'Carnes', 'unidad_medida': 'kg', 'nivel_critico': 4},
            {'nombre': 'Queso', 'cantidad': 15, 'categoria': 'Lácteos', 'unidad_medida': 'kg', 'nivel_critico': 2},
            {'nombre': 'Pan', 'cantidad': 100, 'categoria': 'Panadería', 'unidad_medida': 'unidades', 'nivel_critico': 20},
            {'nombre': 'Lechuga', 'cantidad': 10, 'categoria': 'Verduras', 'unidad_medida': 'kg', 'nivel_critico': 2},
            {'nombre': 'Aceite', 'cantidad': 5, 'categoria': 'Condimentos', 'unidad_medida': 'litros', 'nivel_critico': 1},
        ]
        
        for ingrediente_data in ingredientes:
            ingrediente, created = IngredienteModelo.objects.get_or_create(
                nombre=ingrediente_data['nombre'],
                defaults=ingrediente_data
            )
            if created:
                self.stdout.write(f"✅ Ingrediente creado: {ingrediente.nombre}")

        # Crear menús
        menus = [
            {
                'nombre': 'Hamburguesa Clásica',
                'descripcion': 'Hamburguesa con carne, lechuga, tomate y queso',
                'precio': Decimal('8500'),
                'categoria': 'Hamburguesas',
                'tiempo_preparacion': 15,
                'disponible': True
            },
            {
                'nombre': 'Pollo a la Plancha',
                'descripcion': 'Pechuga de pollo con ensalada',
                'precio': Decimal('7200'),
                'categoria': 'Pollo',
                'tiempo_preparacion': 20,
                'disponible': True
            },
            {
                'nombre': 'Ensalada César',
                'descripcion': 'Lechuga, crutones, queso parmesano y aderezo césar',
                'precio': Decimal('5500'),
                'categoria': 'Ensaladas',
                'tiempo_preparacion': 10,
                'disponible': True
            },
            {
                'nombre': 'Lomito Completo',
                'descripcion': 'Pan con carne, tomate, palta y mayonesa',
                'precio': Decimal('6800'),
                'categoria': 'Lomitos',
                'tiempo_preparacion': 12,
                'disponible': True
            },
            {
                'nombre': 'Papas Fritas',
                'descripcion': 'Papas fritas caseras',
                'precio': Decimal('3200'),
                'categoria': 'Acompañamientos',
                'tiempo_preparacion': 8,
                'disponible': True
            }
        ]
        
        for menu_data in menus:
            menu, created = MenuModelo.objects.get_or_create(
                nombre=menu_data['nombre'],
                defaults=menu_data
            )
            if created:
                self.stdout.write(f"✅ Menú creado: {menu.nombre}")

        # Crear medios de pago
        medios_pago = [
            {
                'nombre': 'Efectivo',
                'tipo': 'efectivo',
                'activo': True,
                'comision_porcentaje': Decimal('0.00'),
                'requiere_validacion': False
            },
            {
                'nombre': 'Tarjeta de Débito',
                'tipo': 'tarjeta_debito',
                'activo': True,
                'comision_porcentaje': Decimal('1.50'),
                'requiere_validacion': True
            },
            {
                'nombre': 'Tarjeta de Crédito',
                'tipo': 'tarjeta_credito',
                'activo': True,
                'comision_porcentaje': Decimal('2.90'),
                'requiere_validacion': True
            },
            {
                'nombre': 'Transferencia',
                'tipo': 'transferencia',
                'activo': True,
                'comision_porcentaje': Decimal('0.50'),
                'requiere_validacion': False
            }
        ]
        
        for medio_data in medios_pago:
            medio, created = MedioPagoModelo.objects.get_or_create(
                nombre=medio_data['nombre'],
                defaults=medio_data
            )
            if created:
                self.stdout.write(f"✅ Medio de pago creado: {medio.nombre}")

        # Crear apps de delivery
        apps = [
            {
                'nombre': 'Uber Eats',
                'comision': Decimal('15.00'),
                'activa': True,
                'api_endpoint': 'https://api.ubereats.com/',
            },
            {
                'nombre': 'Rappi',
                'comision': Decimal('18.00'),
                'activa': True,
                'api_endpoint': 'https://api.rappi.com/',
            },
            {
                'nombre': 'PedidosYa',
                'comision': Decimal('16.50'),
                'activa': True,
                'api_endpoint': 'https://api.pedidosya.com/',
            }
        ]
        
        for app_data in apps:
            app, created = DeliveryAppModelo.objects.get_or_create(
                nombre=app_data['nombre'],
                defaults=app_data
            )
            if created:
                self.stdout.write(f"✅ App de delivery creada: {app.nombre}")

        # Crear pedido de ejemplo
        try:
            cliente = ClienteModelo.objects.first()
            mesa = MesaModelo.objects.first()
            menu1 = MenuModelo.objects.filter(nombre='Hamburguesa Clásica').first()
            menu2 = MenuModelo.objects.filter(nombre='Papas Fritas').first()
            
            if cliente and mesa and menu1:
                pedido = PedidoModelo.objects.create(
                    cliente=cliente,
                    mesa=mesa,
                    estado='confirmado',
                    tipo_pedido='mesa',
                    observaciones_generales='Pedido de prueba',
                    total=Decimal('11700')
                )
                
                ItemPedidoModelo.objects.create(
                    pedido=pedido,
                    menu=menu1,
                    cantidad=1,
                    precio_unitario=menu1.precio,
                    observaciones='Sin cebolla'
                )
                
                if menu2:
                    ItemPedidoModelo.objects.create(
                        pedido=pedido,
                        menu=menu2,
                        cantidad=1,
                        precio_unitario=menu2.precio
                    )
                
                self.stdout.write(f"✅ Pedido de ejemplo creado: #{pedido.id}")
        except Exception as e:
            self.stdout.write(f"❌ Error creando pedido de ejemplo: {e}")

        self.stdout.write("\n🎉 ¡Base de datos poblada exitosamente!")
        self.stdout.write(f"\n📊 Resumen:")
        self.stdout.write(f"   - Clientes: {ClienteModelo.objects.count()}")
        self.stdout.write(f"   - Mesas: {MesaModelo.objects.count()}")
        self.stdout.write(f"   - Ingredientes: {IngredienteModelo.objects.count()}")
        self.stdout.write(f"   - Menús: {MenuModelo.objects.count()}")
        self.stdout.write(f"   - Medios de pago: {MedioPagoModelo.objects.count()}")
        self.stdout.write(f"   - Apps de delivery: {DeliveryAppModelo.objects.count()}")
        self.stdout.write(f"   - Pedidos: {PedidoModelo.objects.count()}")
