# Backend/Presentacion/Controladores/Analytics_Controlador.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.utils import timezone

from Backend.Aplicacion.Servicios.Analytics_Servicio import AnalyticsServicio

class AnalyticsViewSet(viewsets.ViewSet):
    """
    ViewSet para manejo de analytics y reportes
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analytics_servicio = AnalyticsServicio()
    
    @action(detail=False, methods=['get'], url_path='dashboard')
    def dashboard_data(self, request):
        """
        Endpoint para obtener datos del dashboard
        GET /api/analytics/dashboard?period=today&start_date=&end_date=
        """
        try:
            # Obtener parámetros de fecha
            period = request.query_params.get('period', 'today')
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            
            # Calcular fechas según el periodo
            if period == 'today':
                fecha_inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
                fecha_fin = timezone.now()
            elif period == 'week':
                fecha_inicio = timezone.now() - timedelta(days=7)
                fecha_fin = timezone.now()
            elif period == 'month':
                fecha_inicio = timezone.now() - timedelta(days=30)
                fecha_fin = timezone.now()
            elif period == 'custom' and start_date and end_date:
                fecha_inicio = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                fecha_fin = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            else:
                fecha_inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
                fecha_fin = timezone.now()
            
            # Obtener datos del dashboard
            data = self.analytics_servicio.obtener_datos_dashboard_completo(fecha_inicio, fecha_fin)
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al obtener datos del dashboard: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='sales-kpis')
    def sales_kpis(self, request):
        """
        Endpoint específico para KPIs de ventas
        """
        try:
            fecha_inicio, fecha_fin = self._parse_date_params(request)
            data = self.analytics_servicio.obtener_kpis_ventas(fecha_inicio, fecha_fin)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Error al obtener KPIs de ventas: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='inventory-kpis')
    def inventory_kpis(self, request):
        """
        Endpoint específico para KPIs de inventario
        """
        try:
            fecha_inicio, fecha_fin = self._parse_date_params(request)
            data = self.analytics_servicio.obtener_kpis_inventario(fecha_inicio, fecha_fin)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Error al obtener KPIs de inventario: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='operational-kpis')
    def operational_kpis(self, request):
        """
        Endpoint específico para KPIs operacionales
        """
        try:
            fecha_inicio, fecha_fin = self._parse_date_params(request)
            data = self.analytics_servicio.obtener_kpis_operacionales(fecha_inicio, fecha_fin)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'Error al obtener KPIs operacionales: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], url_path='export-report')
    def export_report(self, request):
        """
        Endpoint para exportar reportes en diferentes formatos
        POST /api/analytics/export-report
        Body: {
            "format": "pdf|excel|csv",
            "sections": ["sales", "inventory", "operational"],
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "include_charts": true
        }
        """
        try:
            # Obtener configuración de exportación
            export_config = request.data
            format_type = export_config.get('format', 'pdf')
            sections = export_config.get('sections', ['sales'])
            include_charts = export_config.get('include_charts', False)
            
            # Parsear fechas
            start_date = export_config.get('start_date')
            end_date = export_config.get('end_date')
            
            if start_date and end_date:
                fecha_inicio = datetime.fromisoformat(start_date)
                fecha_fin = datetime.fromisoformat(end_date)
            else:
                fecha_inicio = timezone.now() - timedelta(days=30)
                fecha_fin = timezone.now()
            
            # Obtener datos según secciones solicitadas
            data = {}
            if 'sales' in sections:
                data['sales'] = self.analytics_servicio.obtener_kpis_ventas(fecha_inicio, fecha_fin)
            if 'inventory' in sections:
                data['inventory'] = self.analytics_servicio.obtener_kpis_inventario(fecha_inicio, fecha_fin)
            if 'operational' in sections:
                data['operational'] = self.analytics_servicio.obtener_kpis_operacionales(fecha_inicio, fecha_fin)
            
            # Por ahora devolvemos los datos JSON
            # En una implementación completa, aquí generaríamos el archivo PDF/Excel
            return Response({
                'message': f'Reporte en formato {format_type} generado exitosamente',
                'data': data,
                'config': export_config,
                'download_url': f'/api/analytics/download-report/{format_type}/latest'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': f'Error al exportar reporte: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _parse_date_params(self, request):
        """
        Método auxiliar para parsear parámetros de fecha
        """
        period = request.query_params.get('period', 'today')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if period == 'today':
            fecha_inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            fecha_fin = timezone.now()
        elif period == 'week':
            fecha_inicio = timezone.now() - timedelta(days=7)
            fecha_fin = timezone.now()
        elif period == 'month':
            fecha_inicio = timezone.now() - timedelta(days=30)
            fecha_fin = timezone.now()
        elif period == 'custom' and start_date and end_date:
            fecha_inicio = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            fecha_fin = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        else:
            fecha_inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            fecha_fin = timezone.now()
        
        return fecha_inicio, fecha_fin
