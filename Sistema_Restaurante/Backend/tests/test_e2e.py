# Backend/tests/test_e2e.py
# S3-35: Tests end-to-end del sistema completo
import pytest
import time
from django.test import TransactionTestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
import json

class TestE2EFlujoCompleto(TransactionTestCase):
    """Tests end-to-end para flujos completos del sistema"""
    
    def setUp(self):
        """Configuración inicial para tests E2E"""
        self.client = Client()
        self.api_client = APIClient()
        
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        
        # Datos de prueba base
        self.datos_cliente = {
            'rut': '12345678-9',
            'nombre': 'Cliente Test E2E',
            'email': 'cliente.e2e@test.com',
            'telefono': '987654321'
        }
        
        self.datos_ingrediente = {
            'nombre': 'Ingrediente E2E',
            'stock_actual': 100,
            'stock_minimo': 10,
            'precio_unitario': 1500
        }
        
        self.datos_menu = {
            'nombre': 'Menu E2E',
            'descripcion': 'Menu para testing end-to-end',
            'precio': 8500,
            'categoria': 'Plato Principal',
            'disponible': True
        }
    
    def test_flujo_completo_gestion_cliente(self):
        """
        Test E2E: Flujo completo de gestión de cliente
        1. Crear cliente
        2. Consultar cliente
        3. Actualizar cliente
        4. Listar clientes
        5. Eliminar cliente
        """
        # 1. Crear cliente
        response = self.api_client.post('/api/clientes/', self.datos_cliente, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cliente_id = response.data['id']
        
        # Verificar que se creó correctamente
        self.assertEqual(response.data['nombre'], self.datos_cliente['nombre'])
        self.assertEqual(response.data['rut'], self.datos_cliente['rut'])
        
        # 2. Consultar cliente específico
        response = self.api_client.get(f'/api/clientes/{cliente_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.datos_cliente['nombre'])
        
        # 3. Actualizar cliente
        datos_actualizados = {
            'nombre': 'Cliente E2E Actualizado',
            'email': 'cliente.actualizado@test.com',
            'telefono': '123456789'
        }
        response = self.api_client.patch(f'/api/clientes/{cliente_id}/', datos_actualizados, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], datos_actualizados['nombre'])
        
        # 4. Listar clientes (verificar que aparece)
        response = self.api_client.get('/api/clientes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        clientes = response.data['results'] if 'results' in response.data else response.data
        cliente_encontrado = any(c['id'] == cliente_id for c in clientes)
        self.assertTrue(cliente_encontrado, "Cliente no encontrado en la lista")
        
        # 5. Eliminar cliente
        response = self.api_client.delete(f'/api/clientes/{cliente_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar que se eliminó
        response = self.api_client.get(f'/api/clientes/{cliente_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_flujo_completo_gestion_inventario(self):
        """
        Test E2E: Flujo completo de gestión de inventario
        1. Crear ingrediente
        2. Verificar stock inicial
        3. Actualizar stock
        4. Verificar alertas de stock bajo
        5. Reponer stock
        """
        # 1. Crear ingrediente
        response = self.api_client.post('/api/ingredientes/', self.datos_ingrediente, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ingrediente_id = response.data['id']
        
        # 2. Verificar stock inicial
        response = self.api_client.get(f'/api/ingredientes/{ingrediente_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['stock_actual'], self.datos_ingrediente['stock_actual'])
        
        # 3. Simular consumo de stock (actualizar a stock bajo)
        datos_stock_bajo = {'stock_actual': 5}  # Menor al mínimo (10)
        response = self.api_client.patch(f'/api/ingredientes/{ingrediente_id}/', datos_stock_bajo, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 4. Verificar que aparece en alertas de stock bajo
        response = self.api_client.get('/api/ingredientes/stock-bajo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredientes_stock_bajo = response.data
        ingrediente_en_alerta = any(ing['id'] == ingrediente_id for ing in ingredientes_stock_bajo)
        self.assertTrue(ingrediente_en_alerta, "Ingrediente no aparece en alertas de stock bajo")
        
        # 5. Reponer stock
        datos_reposicion = {'stock_actual': 150}
        response = self.api_client.patch(f'/api/ingredientes/{ingrediente_id}/', datos_reposicion, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que ya no está en stock bajo
        response = self.api_client.get('/api/ingredientes/stock-bajo/')
        ingredientes_stock_bajo = response.data
        ingrediente_en_alerta = any(ing['id'] == ingrediente_id for ing in ingredientes_stock_bajo)
        self.assertFalse(ingrediente_en_alerta, "Ingrediente sigue en alertas después de reposición")
    
    def test_flujo_completo_pedido_delivery(self):
        """
        Test E2E: Flujo completo de pedido con delivery
        1. Crear cliente, ingredientes y menú
        2. Crear pedido
        3. Procesar pedido
        4. Asignar delivery
        5. Completar entrega
        6. Verificar estados
        """
        # 1. Preparar datos base
        # Crear cliente
        response = self.api_client.post('/api/clientes/', self.datos_cliente, format='json')
        cliente_id = response.data['id']
        
        # Crear ingrediente
        response = self.api_client.post('/api/ingredientes/', self.datos_ingrediente, format='json')
        ingrediente_id = response.data['id']
        
        # Crear menú
        response = self.api_client.post('/api/menus/', self.datos_menu, format='json')
        menu_id = response.data['id']
        
        # Asociar ingrediente al menú
        self.api_client.post(f'/api/menus/{menu_id}/ingredientes/', {'ingrediente_id': ingrediente_id})
        
        # 2. Crear pedido
        datos_pedido = {
            'cliente_id': cliente_id,
            'items': [
                {
                    'menu_id': menu_id,
                    'cantidad': 2
                }
            ],
            'tipo_entrega': 'delivery',
            'direccion_entrega': 'Calle Test 123, Ciudad Test'
        }
        
        response = self.api_client.post('/api/pedidos/', datos_pedido, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pedido_id = response.data['id']
        
        # Verificar estado inicial
        self.assertEqual(response.data['estado'], 'pendiente')
        
        # 3. Procesar pedido (cambiar a en_preparacion)
        response = self.api_client.patch(f'/api/pedidos/{pedido_id}/', {'estado': 'en_preparacion'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 4. Completar preparación y asignar delivery
        response = self.api_client.patch(f'/api/pedidos/{pedido_id}/', {'estado': 'listo_para_entrega'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Crear delivery
        datos_delivery = {
            'pedido_id': pedido_id,
            'direccion': 'Calle Test 123, Ciudad Test',
            'repartidor': 'Juan Pérez',
            'telefono_repartidor': '987654321'
        }
        
        response = self.api_client.post('/api/deliveries/', datos_delivery, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        delivery_id = response.data['id']
        
        # 5. Simular proceso de entrega
        # En camino
        response = self.api_client.patch(f'/api/deliveries/{delivery_id}/', {'estado': 'en_camino'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Entregado
        response = self.api_client.patch(f'/api/deliveries/{delivery_id}/', {'estado': 'entregado'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 6. Verificar estado final del pedido
        response = self.api_client.get(f'/api/pedidos/{pedido_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estado'], 'completado')
    
    def test_flujo_completo_analytics_dashboard(self):
        """
        Test E2E: Flujo completo de analytics y dashboard
        1. Crear datos de prueba (pedidos, ventas)
        2. Obtener métricas del dashboard
        3. Verificar reportes de ventas
        4. Validar datos de performance
        """
        # 1. Crear datos de prueba
        # Cliente
        response = self.api_client.post('/api/clientes/', self.datos_cliente, format='json')
        cliente_id = response.data['id']
        
        # Menú
        response = self.api_client.post('/api/menus/', self.datos_menu, format='json')
        menu_id = response.data['id']
        
        # Crear varios pedidos para generar datos
        pedidos_creados = []
        for i in range(5):
            datos_pedido = {
                'cliente_id': cliente_id,
                'items': [{'menu_id': menu_id, 'cantidad': i + 1}],
                'estado': 'completado'
            }
            response = self.api_client.post('/api/pedidos/', datos_pedido, format='json')
            pedidos_creados.append(response.data['id'])
        
        # 2. Obtener métricas del dashboard
        response = self.api_client.get('/api/analytics/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        dashboard_data = response.data
        self.assertIn('total_pedidos', dashboard_data)
        self.assertIn('ventas_total', dashboard_data)
        self.assertIn('clientes_activos', dashboard_data)
        
        # Verificar que los datos reflejan nuestros pedidos
        self.assertGreaterEqual(dashboard_data['total_pedidos'], 5)
        
        # 3. Obtener reporte de ventas
        response = self.api_client.get('/api/analytics/ventas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        ventas_data = response.data
        self.assertIn('ventas_por_periodo', ventas_data)
        self.assertIn('productos_mas_vendidos', ventas_data)
        
        # 4. Obtener datos de performance
        response = self.api_client.get('/api/analytics/performance/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        performance_data = response.data
        self.assertIn('tiempo_promedio_preparacion', performance_data)
        self.assertIn('satisfaccion_cliente', performance_data)
    
    def test_flujo_completo_sistema_pagos(self):
        """
        Test E2E: Flujo completo del sistema de pagos
        1. Crear pedido
        2. Generar pago
        3. Procesar pago
        4. Verificar estado
        5. Manejar fallos de pago
        """
        # 1. Crear pedido base
        response = self.api_client.post('/api/clientes/', self.datos_cliente, format='json')
        cliente_id = response.data['id']
        
        response = self.api_client.post('/api/menus/', self.datos_menu, format='json')
        menu_id = response.data['id']
        
        datos_pedido = {
            'cliente_id': cliente_id,
            'items': [{'menu_id': menu_id, 'cantidad': 1}],
            'estado': 'listo_para_pago'
        }
        
        response = self.api_client.post('/api/pedidos/', datos_pedido, format='json')
        pedido_id = response.data['id']
        total_pedido = response.data['total']
        
        # 2. Crear pago
        datos_pago = {
            'pedido_id': pedido_id,
            'monto': total_pedido,
            'metodo_pago': 'tarjeta_credito',
            'detalles_pago': {
                'numero_tarjeta': '**** **** **** 1234',
                'tipo_tarjeta': 'visa'
            }
        }
        
        response = self.api_client.post('/api/pagos/', datos_pago, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pago_id = response.data['id']
        
        # Verificar estado inicial
        self.assertEqual(response.data['estado'], 'pendiente')
        
        # 3. Procesar pago exitoso
        response = self.api_client.patch(f'/api/pagos/{pago_id}/', {'estado': 'procesando'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Simular confirmación de pago
        response = self.api_client.patch(f'/api/pagos/{pago_id}/', {'estado': 'completado'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 4. Verificar que el pedido se actualizó
        response = self.api_client.get(f'/api/pedidos/{pedido_id}/')
        self.assertEqual(response.data['estado'], 'pagado')
        
        # 5. Test de pago fallido
        # Crear otro pedido
        response = self.api_client.post('/api/pedidos/', datos_pedido, format='json')
        pedido_id_2 = response.data['id']
        
        datos_pago_2 = {
            'pedido_id': pedido_id_2,
            'monto': total_pedido,
            'metodo_pago': 'tarjeta_credito'
        }
        
        response = self.api_client.post('/api/pagos/', datos_pago_2, format='json')
        pago_id_2 = response.data['id']
        
        # Simular fallo de pago
        response = self.api_client.patch(f'/api/pagos/{pago_id_2}/', {'estado': 'fallido'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que el pedido mantiene estado correcto
        response = self.api_client.get(f'/api/pedidos/{pedido_id_2}/')
        self.assertNotEqual(response.data['estado'], 'pagado')
    
    def test_performance_sistema_completo(self):
        """
        Test E2E: Performance del sistema con carga
        Simular múltiples operaciones concurrentes
        """
        import threading
        import queue
        
        resultados = queue.Queue()
        
        def crear_cliente_pedido(thread_id):
            """Función para crear cliente y pedido en thread separado"""
            try:
                start_time = time.time()
                
                # Crear cliente
                datos_cliente_thread = {
                    'rut': f'1234567{thread_id:02d}',
                    'nombre': f'Cliente Thread {thread_id}',
                    'email': f'cliente{thread_id}@test.com',
                    'telefono': f'98765432{thread_id}'
                }
                
                client_thread = APIClient()
                response = client_thread.post('/api/clientes/', datos_cliente_thread, format='json')
                
                if response.status_code == 201:
                    tiempo_total = time.time() - start_time
                    resultados.put((thread_id, 'success', tiempo_total))
                else:
                    resultados.put((thread_id, 'error', response.status_code))
                    
            except Exception as e:
                resultados.put((thread_id, 'exception', str(e)))
        
        # Crear múltiples threads
        threads = []
        num_threads = 10
        
        for i in range(num_threads):
            thread = threading.Thread(target=crear_cliente_pedido, args=(i,))
            threads.append(thread)
        
        # Ejecutar todos los threads
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        tiempo_total = time.time() - start_time
        
        # Analizar resultados
        resultados_list = []
        while not resultados.empty():
            resultados_list.append(resultados.get())
        
        exitosos = [r for r in resultados_list if r[1] == 'success']
        errores = [r for r in resultados_list if r[1] != 'success']
        
        # Verificaciones de performance
        self.assertEqual(len(exitosos), num_threads, f"Solo {len(exitosos)} de {num_threads} requests exitosos")
        self.assertLess(tiempo_total, 10.0, "Sistema tardó más de 10 segundos en procesar requests concurrentes")
        
        if exitosos:
            tiempo_promedio = sum(r[2] for r in exitosos) / len(exitosos)
            self.assertLess(tiempo_promedio, 2.0, "Tiempo promedio por request excede 2 segundos")
    
    def test_integracion_completa_frontend_backend(self):
        """
        Test E2E: Integración completa frontend-backend
        Simular requests que haría el frontend
        """
        # Simular autenticación
        auth_data = {
            'username': self.user.username,
            'password': 'testpass123'
        }
        
        response = self.api_client.post('/api/auth/login/', auth_data, format='json')
        # Nota: Esto depende de la implementación específica de autenticación
        
        # Test de endpoints principales que usa el frontend
        endpoints_frontend = [
            '/api/clientes/',
            '/api/ingredientes/',
            '/api/menus/',
            '/api/pedidos/',
            '/api/analytics/dashboard/',
        ]
        
        for endpoint in endpoints_frontend:
            with self.subTest(endpoint=endpoint):
                response = self.api_client.get(endpoint)
                self.assertIn(response.status_code, [200, 401])  # 401 si requiere auth
        
        # Test de CORS headers (importantes para frontend)
        response = self.api_client.options('/api/clientes/')
        # Verificar headers CORS si están configurados
        
    def tearDown(self):
        """Limpieza después de cada test"""
        # Limpiar cache si se usa
        try:
            from django.core.cache import cache
            cache.clear()
        except:
            pass
