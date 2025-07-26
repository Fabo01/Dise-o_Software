# Backend/Infraestructura/Repositorios/PagosRepositorio.py
from typing import List, Optional
from decimal import Decimal
from datetime import date
from Backend.Dominio.Interfaces.IPagosRepositorio import IPagosRepositorio
from Backend.Dominio.Entidades.Transaccion_Entidad import TransaccionEntidad
from Backend.Infraestructura.Modelos.Transaccion_Modelo import TransaccionModelo
from Backend.Infraestructura.Modelos.MedioPago_Modelo import MedioPagoModelo
from django.db import transaction
from django.db.models import Sum
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

class PagosRepositorio(IPagosRepositorio):
    """
    Implementación concreta del repositorio de pagos.
    Maneja la persistencia de transacciones y medios de pago.
    """
    
    def crear_transaccion(self, transaccion: TransaccionEntidad) -> TransaccionEntidad:
        """Crea una nueva transacción"""
        with transaction.atomic():
            modelo = TransaccionModelo(
                pedido_id=transaccion.pedido_id,
                medio_pago_id=transaccion.medio_pago_id,
                monto=transaccion.monto,
                comision=transaccion.comision,
                estado=transaccion.estado,
                referencia_externa=transaccion.referencia_externa,
                notas=transaccion.notas
            )
            modelo.save()
            
            return self._modelo_a_entidad(modelo)
    
    def obtener_transaccion_por_id(self, transaccion_id: int) -> Optional[TransaccionEntidad]:
        """Obtiene una transacción por su ID"""
        try:
            modelo = TransaccionModelo.objects.get(id=transaccion_id)
            return self._modelo_a_entidad(modelo)
        except TransaccionModelo.DoesNotExist:
            return None
    
    def listar_transacciones_por_pedido(self, pedido_id: int) -> List[TransaccionEntidad]:
        """Lista todas las transacciones de un pedido específico"""
        modelos = TransaccionModelo.objects.filter(pedido_id=pedido_id)
        return [self._modelo_a_entidad(modelo) for modelo in modelos]
    
    def listar_transacciones_por_periodo(self, fecha_inicio, fecha_fin) -> List[TransaccionEntidad]:
        """Lista transacciones en un período específico"""
        modelos = TransaccionModelo.objects.filter(
            fecha_transaccion__date__gte=fecha_inicio,
            fecha_transaccion__date__lte=fecha_fin
        ).order_by('-fecha_transaccion')
        return [self._modelo_a_entidad(modelo) for modelo in modelos]
    
    def obtener_medios_pago_activos(self) -> List:
        """Obtiene lista de medios de pago activos"""
        medios = MedioPagoModelo.objects.filter(activo=True)
        return [
            {
                'id': medio.id,
                'nombre': medio.nombre,
                'tipo': medio.tipo,
                'comision_porcentaje': medio.comision_porcentaje,
                'requiere_validacion_externa': medio.requiere_validacion_externa
            }
            for medio in medios
        ]
    
    def validar_pago_externo(self, medio_pago_id: int, monto: Decimal, referencia: str) -> bool:
        """Valida un pago con servicio externo"""
        try:
            medio_pago = MedioPagoModelo.objects.get(id=medio_pago_id)
            
            if not medio_pago.requiere_validacion_externa:
                return True
            
            # Aquí iría la lógica de validación con servicios externos
            # Por ahora, simulamos una validación exitosa
            if medio_pago.tipo in ['tarjeta_credito', 'tarjeta_debito']:
                # Simular validación con gateway de pagos
                return self._validar_tarjeta(referencia, monto)
            elif medio_pago.tipo == 'transferencia':
                # Simular validación con API bancaria
                return self._validar_transferencia(referencia, monto)
            
            return True
            
        except MedioPagoModelo.DoesNotExist:
            return False
    
    def calcular_comisiones_periodo(self, fecha_inicio, fecha_fin) -> Decimal:
        """Calcula el total de comisiones en un período"""
        resultado = TransaccionModelo.objects.filter(
            fecha_transaccion__date__gte=fecha_inicio,
            fecha_transaccion__date__lte=fecha_fin,
            estado='exitosa'
        ).aggregate(total_comisiones=Sum('monto_comision'))
        
        return resultado.get('total_comisiones') or Decimal('0.00')
    
    def generar_comprobante_pago(self, transaccion_id: int) -> bytes:
        """Genera comprobante PDF de una transacción"""
        try:
            transaccion = TransaccionModelo.objects.get(id=transaccion_id)
            
            # Crear PDF en memoria
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            
            # Encabezado
            p.drawString(100, 750, "COMPROBANTE DE PAGO")
            p.drawString(100, 730, f"Transacción #{transaccion.id}")
            p.drawString(100, 710, f"Fecha: {transaccion.fecha_transaccion.strftime('%d/%m/%Y %H:%M')}")
            
            # Detalles de la transacción
            p.drawString(100, 680, f"Pedido: #{transaccion.pedido_id}")
            p.drawString(100, 660, f"Monto: ${transaccion.monto}")
            p.drawString(100, 640, f"Método de pago: {transaccion.medio_pago.nombre}")
            p.drawString(100, 620, f"Estado: {transaccion.estado}")
            
            if transaccion.referencia_externa:
                p.drawString(100, 600, f"Referencia: {transaccion.referencia_externa}")
            
            # Pie de página
            p.drawString(100, 550, "Gracias por su compra")
            
            p.showPage()
            p.save()
            
            buffer.seek(0)
            return buffer.getvalue()
            
        except TransaccionModelo.DoesNotExist:
            return b''
    
    def actualizar_estado_transaccion(self, transaccion_id: int, nuevo_estado: str) -> bool:
        """Actualiza el estado de una transacción"""
        try:
            with transaction.atomic():
                transaccion = TransaccionModelo.objects.get(id=transaccion_id)
                transaccion.estado = nuevo_estado
                if nuevo_estado == 'completado':
                    from django.utils import timezone
                    transaccion.fecha_procesamiento = timezone.now()
                transaccion.save()
                return True
        except TransaccionModelo.DoesNotExist:
            return False
    
    def _modelo_a_entidad(self, modelo: TransaccionModelo) -> TransaccionEntidad:
        """Convierte un modelo de Django a entidad de dominio"""
        return TransaccionEntidad(
            id=modelo.id,
            pedido_id=modelo.pedido_id,
            medio_pago_id=modelo.medio_pago_id,
            monto=modelo.monto,
            comision=modelo.comision,
            estado=modelo.estado,
            referencia_externa=modelo.referencia_externa,
            fecha_creacion=modelo.fecha_transaccion,
            fecha_procesamiento=modelo.fecha_procesamiento,
            notas=modelo.notas
        )
    
    def _validar_tarjeta(self, referencia: str, monto: Decimal) -> bool:
        """Simula validación de tarjeta con gateway de pagos"""
        # Simulación: referencia debe tener formato específico
        return len(referencia) >= 10 and monto > 0
    
    def _validar_transferencia(self, referencia: str, monto: Decimal) -> bool:
        """Simula validación de transferencia bancaria"""
        # Simulación: referencia debe ser numérica y monto válido
        return referencia.isdigit() and monto > 0
