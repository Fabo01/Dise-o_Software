# Backend/Infraestructura/Servicios/ValidadorPerformance.py
# S3-30: Validación de optimizaciones de rendimiento
import time
import psutil
import os
from typing import Dict, List, Any, Optional
from django.test import TestCase
from django.db import connection, transaction
from django.core.cache import cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class ValidadorPerformance:
    """Validador de optimizaciones de rendimiento implementadas"""
    
    def __init__(self):
        self.metricas_base = {}
        self.umbrales = {
            'tiempo_consulta_max': 0.5,  # segundos
            'memoria_max_mb': 100,  # MB
            'consultas_sql_max': 5,  # por operación
            'tiempo_cache_hit_max': 0.01,  # segundos
            'cpu_usage_max': 80,  # porcentaje
        }
    
    def validar_optimizaciones_completas(self) -> Dict[str, Any]:
        """
        Ejecutar todas las validaciones de performance
        S3-30: Validar optimizaciones implementadas
        """
        resultados = {
            'timestamp': time.time(),
            'validaciones': {},
            'resumen': {
                'total_tests': 0,
                'tests_passed': 0,
                'tests_failed': 0,
                'score_performance': 0
            }
        }
        
        # Lista de validaciones a ejecutar
        validaciones = [
            ('consultas_optimizadas', self.validar_consultas_optimizadas),
            ('cache_funcionando', self.validar_cache_funcionando),
            ('indices_database', self.validar_indices_database),
            ('memoria_usage', self.validar_uso_memoria),
            ('tiempo_respuesta_api', self.validar_tiempo_respuesta_api),
            ('lazy_loading_frontend', self.validar_lazy_loading),
            ('paginacion_eficiente', self.validar_paginacion),
        ]
        
        for nombre, funcion_validacion in validaciones:
            try:
                resultado = funcion_validacion()
                resultados['validaciones'][nombre] = resultado
                
                resultados['resumen']['total_tests'] += 1
                if resultado.get('passed', False):
                    resultados['resumen']['tests_passed'] += 1
                else:
                    resultados['resumen']['tests_failed'] += 1
                    
            except Exception as e:
                logger.error(f"Error en validación {nombre}: {str(e)}")
                resultados['validaciones'][nombre] = {
                    'passed': False,
                    'error': str(e),
                    'tiempo_ejecucion': 0
                }
                resultados['resumen']['tests_failed'] += 1
        
        # Calcular score de performance
        if resultados['resumen']['total_tests'] > 0:
            score = (resultados['resumen']['tests_passed'] / 
                    resultados['resumen']['total_tests']) * 100
            resultados['resumen']['score_performance'] = round(score, 2)
        
        return resultados
    
    def validar_consultas_optimizadas(self) -> Dict[str, Any]:
        """Validar que las consultas están optimizadas"""
        from Backend.Infraestructura.Servicios.OptimizadorConsultas import OptimizadorConsultas
        
        start_time = time.time()
        optimizador = OptimizadorConsultas()
        
        # Test 1: Número de consultas SQL
        with self.capturar_consultas_sql() as consultas:
            clientes = optimizador.obtener_clientes_con_pedidos_recientes()
            list(clientes)  # Forzar evaluación
        
        num_consultas = len(consultas)
        tiempo_ejecucion = time.time() - start_time
        
        # Validaciones
        consultas_ok = num_consultas <= self.umbrales['consultas_sql_max']
        tiempo_ok = tiempo_ejecucion <= self.umbrales['tiempo_consulta_max']
        
        return {
            'passed': consultas_ok and tiempo_ok,
            'metricas': {
                'num_consultas_sql': num_consultas,
                'tiempo_ejecucion': round(tiempo_ejecucion, 4),
                'consultas_optimas': consultas_ok,
                'tiempo_optimo': tiempo_ok
            },
            'umbrales': {
                'max_consultas': self.umbrales['consultas_sql_max'],
                'max_tiempo': self.umbrales['tiempo_consulta_max']
            }
        }
    
    def validar_cache_funcionando(self) -> Dict[str, Any]:
        """Validar que el sistema de cache está funcionando"""
        from Backend.Infraestructura.Servicios.OptimizadorConsultas import CacheManager
        
        cache_manager = CacheManager()
        cache.clear()  # Limpiar cache
        
        # Test cache miss
        start_time = time.time()
        datos_miss = cache_manager.obtener_o_cachear(
            'test_performance_validation',
            lambda: self._generar_datos_prueba(),
            timeout=60
        )
        tiempo_miss = time.time() - start_time
        
        # Test cache hit
        start_time = time.time()
        datos_hit = cache_manager.obtener_o_cachear(
            'test_performance_validation',
            lambda: self._generar_datos_prueba(),
            timeout=60
        )
        tiempo_hit = time.time() - start_time
        
        # Validaciones
        cache_funcionando = tiempo_hit < tiempo_miss / 2  # Hit debe ser al menos 50% más rápido
        tiempo_hit_ok = tiempo_hit <= self.umbrales['tiempo_cache_hit_max']
        
        return {
            'passed': cache_funcionando and tiempo_hit_ok,
            'metricas': {
                'tiempo_cache_miss': round(tiempo_miss, 4),
                'tiempo_cache_hit': round(tiempo_hit, 4),
                'mejora_performance': round((tiempo_miss - tiempo_hit) / tiempo_miss * 100, 2),
                'cache_funcionando': cache_funcionando
            },
            'umbrales': {
                'max_tiempo_hit': self.umbrales['tiempo_cache_hit_max']
            }
        }
    
    def validar_indices_database(self) -> Dict[str, Any]:
        """Validar que los índices de base de datos existen"""
        indices_encontrados = []
        indices_esperados = [
            'cliente_rut',
            'pedido_fecha',
            'menu_disponible',
            'ingrediente_stock'
        ]
        
        with connection.cursor() as cursor:
            # Para SQLite
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='index' AND name NOT LIKE 'sqlite_%'
            """)
            indices_db = [row[0] for row in cursor.fetchall()]
        
        # Verificar índices esperados
        for indice_esperado in indices_esperados:
            encontrado = any(indice_esperado.lower() in indice.lower() for indice in indices_db)
            indices_encontrados.append({
                'indice': indice_esperado,
                'encontrado': encontrado
            })
        
        indices_ok = all(item['encontrado'] for item in indices_encontrados)
        
        return {
            'passed': indices_ok,
            'metricas': {
                'indices_esperados': len(indices_esperados),
                'indices_encontrados': sum(1 for item in indices_encontrados if item['encontrado']),
                'indices_detalle': indices_encontrados,
                'indices_db_total': len(indices_db)
            }
        }
    
    def validar_uso_memoria(self) -> Dict[str, Any]:
        """Validar que el uso de memoria es eficiente"""
        proceso = psutil.Process(os.getpid())
        memoria_inicial = proceso.memory_info().rss / 1024 / 1024  # MB
        
        # Ejecutar operaciones que consumen memoria
        self._ejecutar_operaciones_memoria()
        
        memoria_final = proceso.memory_info().rss / 1024 / 1024  # MB
        incremento_memoria = memoria_final - memoria_inicial
        
        # Validación
        memoria_ok = incremento_memoria <= self.umbrales['memoria_max_mb']
        
        return {
            'passed': memoria_ok,
            'metricas': {
                'memoria_inicial_mb': round(memoria_inicial, 2),
                'memoria_final_mb': round(memoria_final, 2),
                'incremento_mb': round(incremento_memoria, 2),
                'memoria_eficiente': memoria_ok
            },
            'umbrales': {
                'max_incremento_mb': self.umbrales['memoria_max_mb']
            }
        }
    
    def validar_tiempo_respuesta_api(self) -> Dict[str, Any]:
        """Validar tiempos de respuesta de API endpoints"""
        from django.test.client import Client
        
        client = Client()
        endpoints_test = [
            '/api/clientes/',
            '/api/menus/',
            '/api/ingredientes/',
            '/api/pedidos/'
        ]
        
        resultados_endpoints = []
        
        for endpoint in endpoints_test:
            try:
                start_time = time.time()
                response = client.get(endpoint)
                tiempo_respuesta = time.time() - start_time
                
                resultados_endpoints.append({
                    'endpoint': endpoint,
                    'tiempo_ms': round(tiempo_respuesta * 1000, 2),
                    'status_code': response.status_code,
                    'tiempo_ok': tiempo_respuesta <= self.umbrales['tiempo_consulta_max']
                })
                
            except Exception as e:
                resultados_endpoints.append({
                    'endpoint': endpoint,
                    'error': str(e),
                    'tiempo_ok': False
                })
        
        todos_ok = all(result.get('tiempo_ok', False) for result in resultados_endpoints)
        tiempo_promedio = sum(
            result.get('tiempo_ms', 0) for result in resultados_endpoints
        ) / len(resultados_endpoints) if resultados_endpoints else 0
        
        return {
            'passed': todos_ok,
            'metricas': {
                'endpoints_testados': len(endpoints_test),
                'endpoints_ok': sum(1 for r in resultados_endpoints if r.get('tiempo_ok')),
                'tiempo_promedio_ms': round(tiempo_promedio, 2),
                'detalle_endpoints': resultados_endpoints
            }
        }
    
    def validar_lazy_loading(self) -> Dict[str, Any]:
        """Validar implementación de lazy loading en frontend"""
        import os
        
        # Verificar archivos de lazy loading
        frontend_path = os.path.join(settings.BASE_DIR, '..', 'Frontend', 'src')
        lazy_files = [
            'utils/lazyComponents.js',
            'components/common/ErrorBoundary.jsx'
        ]
        
        archivos_encontrados = []
        for archivo in lazy_files:
            file_path = os.path.join(frontend_path, archivo)
            existe = os.path.exists(file_path)
            archivos_encontrados.append({
                'archivo': archivo,
                'existe': existe
            })
        
        lazy_implementado = all(item['existe'] for item in archivos_encontrados)
        
        return {
            'passed': lazy_implementado,
            'metricas': {
                'archivos_lazy_esperados': len(lazy_files),
                'archivos_lazy_encontrados': sum(1 for item in archivos_encontrados if item['existe']),
                'detalle_archivos': archivos_encontrados
            }
        }
    
    def validar_paginacion(self) -> Dict[str, Any]:
        """Validar implementación de paginación eficiente"""
        import os
        
        # Verificar archivos de paginación
        frontend_path = os.path.join(settings.BASE_DIR, '..', 'Frontend', 'src')
        paginacion_files = [
            'hooks/usePagination.js',
            'components/common/PaginationComponent.jsx'
        ]
        
        archivos_encontrados = []
        for archivo in paginacion_files:
            file_path = os.path.join(frontend_path, archivo)
            existe = os.path.exists(file_path)
            archivos_encontrados.append({
                'archivo': archivo,
                'existe': existe
            })
        
        paginacion_implementada = all(item['existe'] for item in archivos_encontrados)
        
        return {
            'passed': paginacion_implementada,
            'metricas': {
                'archivos_paginacion_esperados': len(paginacion_files),
                'archivos_paginacion_encontrados': sum(1 for item in archivos_encontrados if item['existe']),
                'detalle_archivos': archivos_encontrados
            }
        }
    
    def capturar_consultas_sql(self):
        """Context manager para capturar consultas SQL"""
        class CapturadorConsultas:
            def __init__(self):
                self.consultas = []
            
            def __enter__(self):
                self.consultas_iniciales = len(connection.queries)
                return self.consultas
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                self.consultas.extend(
                    connection.queries[self.consultas_iniciales:]
                )
        
        return CapturadorConsultas()
    
    def _generar_datos_prueba(self):
        """Generar datos de prueba para tests de cache"""
        import random
        return {
            'data': [random.randint(1, 1000) for _ in range(100)],
            'timestamp': time.time()
        }
    
    def _ejecutar_operaciones_memoria(self):
        """Ejecutar operaciones que consumen memoria para testing"""
        # Simular operaciones que usan memoria
        datos_grandes = []
        for i in range(1000):
            datos_grandes.append({
                'id': i,
                'data': f"test_data_{i}" * 100,
                'timestamp': time.time()
            })
        
        # Procesar datos
        result = sum(len(item['data']) for item in datos_grandes)
        return result
    
    def generar_reporte_performance(self, resultados: Dict[str, Any]) -> str:
        """Generar reporte legible de performance"""
        reporte = []
        reporte.append("=" * 60)
        reporte.append("REPORTE DE VALIDACIÓN DE PERFORMANCE")
        reporte.append("=" * 60)
        reporte.append("")
        
        # Resumen general
        resumen = resultados['resumen']
        reporte.append(f"📊 RESUMEN GENERAL")
        reporte.append(f"   Total de tests: {resumen['total_tests']}")
        reporte.append(f"   Tests pasados: {resumen['tests_passed']}")
        reporte.append(f"   Tests fallidos: {resumen['tests_failed']}")
        reporte.append(f"   Score de performance: {resumen['score_performance']}%")
        reporte.append("")
        
        # Detalle por validación
        for nombre, resultado in resultados['validaciones'].items():
            estado = "✅ PASS" if resultado.get('passed', False) else "❌ FAIL"
            reporte.append(f"{estado} {nombre.upper().replace('_', ' ')}")
            
            if 'metricas' in resultado:
                for metric, value in resultado['metricas'].items():
                    if isinstance(value, (int, float)):
                        reporte.append(f"   {metric}: {value}")
                    elif isinstance(value, bool):
                        reporte.append(f"   {metric}: {'✓' if value else '✗'}")
            
            if 'error' in resultado:
                reporte.append(f"   ERROR: {resultado['error']}")
            
            reporte.append("")
        
        # Recomendaciones
        reporte.append("🔧 RECOMENDACIONES:")
        if resumen['score_performance'] < 80:
            reporte.append("   - El sistema requiere optimizaciones adicionales")
            reporte.append("   - Revisar consultas SQL y uso de cache")
            reporte.append("   - Verificar implementación de índices")
        elif resumen['score_performance'] < 95:
            reporte.append("   - Performance aceptable, considerar optimizaciones menores")
        else:
            reporte.append("   - ¡Excelente performance! Sistema bien optimizado")
        
        reporte.append("")
        reporte.append("=" * 60)
        
        return "\n".join(reporte)


# Función de utilidad para ejecutar validación completa
def ejecutar_validacion_performance() -> Dict[str, Any]:
    """Función helper para ejecutar validación completa de performance"""
    validador = ValidadorPerformance()
    return validador.validar_optimizaciones_completas()


# Comando de management para ejecutar desde Django
from django.core.management.base import BaseCommand

class ComandoValidacionPerformance(BaseCommand):
    """Comando de Django para validar performance"""
    
    help = 'Ejecutar validación completa de optimizaciones de performance'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--generar-reporte',
            action='store_true',
            help='Generar reporte detallado de performance'
        )
    
    def handle(self, *args, **options):
        self.stdout.write('Ejecutando validación de performance...')
        
        validador = ValidadorPerformance()
        resultados = validador.validar_optimizaciones_completas()
        
        # Mostrar resumen
        resumen = resultados['resumen']
        if resumen['score_performance'] >= 80:
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Performance OK: {resumen["score_performance"]}% '
                    f'({resumen["tests_passed"]}/{resumen["total_tests"]} tests passed)'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  Performance Subóptima: {resumen["score_performance"]}% '
                    f'({resumen["tests_failed"]} tests failed)'
                )
            )
        
        # Generar reporte detallado si se solicita
        if options['generar_reporte']:
            reporte = validador.generar_reporte_performance(resultados)
            self.stdout.write('\n' + reporte)
