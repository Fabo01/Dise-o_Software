from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
from Backend.Infraestructura.Modelos.Mesa_Modelo import MesaModelo
from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo


class PedidoModelo(models.Model):
    """Modelo Django para persistir pedidos en la base de datos"""
    
    ESTADOS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('en_preparacion', 'En Preparación'),
        ('listo', 'Listo'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    TIPOS_CHOICES = [
        ('mesa', 'Mesa'),
        ('delivery', 'Delivery'),
        ('para_llevar', 'Para Llevar'),
    ]
    
    # Información básica del pedido
    cliente = models.ForeignKey(
        ClienteModelo, 
        on_delete=models.CASCADE,
        related_name='pedidos',
        help_text='Cliente que realizó el pedido'
    )
    
    tipo_pedido = models.CharField(
        max_length=20,
        choices=TIPOS_CHOICES,
        default='mesa',
        help_text='Tipo de pedido'
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_CHOICES,
        default='pendiente',
        help_text='Estado actual del pedido'
    )
    
    # Información de entrega/ubicación
    mesa = models.ForeignKey(
        MesaModelo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidos',
        help_text='Mesa asignada (solo para pedidos de mesa)'
    )
    
    direccion_entrega = models.TextField(
        null=True,
        blank=True,
        help_text='Dirección de entrega (solo para delivery)'
    )
    
    telefono_contacto = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text='Teléfono de contacto'
    )
    
    # Observaciones y notas
    observaciones_generales = models.TextField(
        null=True,
        blank=True,
        help_text='Observaciones generales del pedido'
    )
    
    # Fechas importantes
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha y hora de creación del pedido'
    )
    
    fecha_confirmacion = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha y hora de confirmación del pedido'
    )
    
    fecha_entrega = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha y hora de entrega del pedido'
    )
    
    # Tiempo estimado de preparación en minutos
    tiempo_preparacion_estimado = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(480)],  # Máximo 8 horas
        help_text='Tiempo estimado de preparación en minutos'
    )
    
    # Total del pedido (calculado automáticamente)
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='Total del pedido'
    )
    
    class Meta:
        db_table = 'pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['tipo_pedido']),
            models.Index(fields=['fecha_creacion']),
            models.Index(fields=['cliente']),
            models.Index(fields=['mesa']),
        ]
        constraints = [
            # Un pedido de mesa debe tener una mesa asignada
            models.CheckConstraint(
                check=~(models.Q(tipo_pedido='mesa') & models.Q(mesa__isnull=True)),
                name='pedido_mesa_requiere_mesa'
            ),
            # Un pedido de delivery debe tener dirección
            models.CheckConstraint(
                check=~(models.Q(tipo_pedido='delivery') & models.Q(direccion_entrega__isnull=True)),
                name='pedido_delivery_requiere_direccion'
            ),
            # El total debe ser mayor o igual a 0
            models.CheckConstraint(
                check=models.Q(total__gte=0),
                name='pedido_total_positivo'
            ),
        ]

    def __str__(self):
        return f"Pedido #{self.pk} - {self.get_tipo_pedido_display()} - {self.get_estado_display()}"

    def clean(self):
        """Validaciones adicionales del modelo"""
        from django.core.exceptions import ValidationError
        
        # Validar que un pedido de mesa tenga mesa asignada
        if self.tipo_pedido == 'mesa' and not self.mesa:
            raise ValidationError('Un pedido de mesa debe tener una mesa asignada')
        
        # Validar que un pedido de delivery tenga dirección
        if self.tipo_pedido == 'delivery' and not self.direccion_entrega:
            raise ValidationError('Un pedido de delivery debe tener dirección de entrega')
        
        # Validar que las fechas sean consistentes
        if self.fecha_confirmacion and self.fecha_confirmacion < self.fecha_creacion:
            raise ValidationError('La fecha de confirmación no puede ser anterior a la fecha de creación')
        
        if self.fecha_entrega and self.fecha_confirmacion and self.fecha_entrega < self.fecha_confirmacion:
            raise ValidationError('La fecha de entrega no puede ser anterior a la fecha de confirmación')

    def save(self, *args, **kwargs):
        """Override del método save para validaciones y cálculos automáticos"""
        self.clean()
        super().save(*args, **kwargs)
        
        # Recalcular el total después de guardar
        self._recalcular_total()

    def _recalcular_total(self):
        """Recalcula el total del pedido basado en los items"""
        total_calculado = sum(
            item.subtotal for item in self.items.all()
        )
        
        if self.total != total_calculado:
            PedidoModelo.objects.filter(pk=self.pk).update(total=total_calculado)

    @property
    def cantidad_total_items(self):
        """Retorna la cantidad total de items en el pedido"""
        return sum(item.cantidad for item in self.items.all())

    @property
    def puede_modificar_items(self):
        """Determina si los items del pedido pueden ser modificados"""
        return self.estado in ['pendiente', 'confirmado']

    @property
    def esta_entregado(self):
        """Determina si el pedido está entregado"""
        return self.estado == 'entregado'

    @property
    def esta_cancelado(self):
        """Determina si el pedido está cancelado"""
        return self.estado == 'cancelado'

    def puede_cancelar(self):
        """Determina si el pedido puede ser cancelado"""
        return self.estado not in ['entregado', 'cancelado']

    def obtener_tiempo_transcurrido(self):
        """Retorna el tiempo transcurrido desde la confirmación en minutos"""
        if not self.fecha_confirmacion:
            return None
        
        from django.utils import timezone
        tiempo_transcurrido = timezone.now() - self.fecha_confirmacion
        return int(tiempo_transcurrido.total_seconds() / 60)

    def esta_atrasado(self):
        """Determina si el pedido está atrasado según el tiempo estimado"""
        if not self.tiempo_preparacion_estimado or not self.fecha_confirmacion:
            return False
        
        tiempo_transcurrido = self.obtener_tiempo_transcurrido()
        return tiempo_transcurrido > self.tiempo_preparacion_estimado


class ItemPedidoModelo(models.Model):
    """Modelo Django para los items individuales de un pedido"""
    
    pedido = models.ForeignKey(
        PedidoModelo,
        on_delete=models.CASCADE,
        related_name='items',
        help_text='Pedido al que pertenece este item'
    )
    
    menu = models.ForeignKey(
        MenuModelo,
        on_delete=models.CASCADE,
        related_name='items_pedido',
        help_text='Item del menú solicitado'
    )
    
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text='Cantidad solicitada del item'
    )
    
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text='Precio unitario al momento del pedido'
    )
    
    observaciones = models.TextField(
        null=True,
        blank=True,
        help_text='Observaciones específicas para este item'
    )
    
    # Campos calculados
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text='Subtotal del item (cantidad × precio_unitario)'
    )
    
    class Meta:
        db_table = 'items_pedido'
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Items de Pedido'
        ordering = ['id']
        indexes = [
            models.Index(fields=['pedido']),
            models.Index(fields=['menu']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(cantidad__gt=0),
                name='item_cantidad_positiva'
            ),
            models.CheckConstraint(
                check=models.Q(precio_unitario__gt=0),
                name='item_precio_positivo'
            ),
            models.CheckConstraint(
                check=models.Q(subtotal__gte=0),
                name='item_subtotal_positivo'
            ),
        ]

    def __str__(self):
        return f"{self.cantidad}x {self.menu.nombre} - ${self.subtotal}"

    def clean(self):
        """Validaciones del item de pedido"""
        from django.core.exceptions import ValidationError
        
        if self.cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor a 0')
        
        if self.precio_unitario <= 0:
            raise ValidationError('El precio unitario debe ser mayor a 0')

    def save(self, *args, **kwargs):
        """Override del método save para calcular el subtotal"""
        # Calcular subtotal automáticamente
        self.subtotal = self.cantidad * self.precio_unitario
        
        self.clean()
        super().save(*args, **kwargs)
        
        # Actualizar el total del pedido
        if self.pedido_id:
            self.pedido._recalcular_total()

    def delete(self, *args, **kwargs):
        """Override del método delete para actualizar el total del pedido"""
        pedido = self.pedido
        super().delete(*args, **kwargs)
        pedido._recalcular_total()
