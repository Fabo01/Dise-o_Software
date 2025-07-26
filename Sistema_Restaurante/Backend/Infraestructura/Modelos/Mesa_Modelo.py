from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo


class MesaModelo(models.Model):
    """
    Modelo Django para la gestión de mesas en el restaurante
    Representa una mesa física con su capacidad, ubicación y estado actual
    """
    
    # Opciones para el estado de la mesa
    ESTADO_CHOICES = [
        ('libre', 'Libre'),
        ('ocupada', 'Ocupada'),
        ('reservada', 'Reservada'),
        ('limpieza', 'En Limpieza'),
        ('fuera_servicio', 'Fuera de Servicio'),
    ]
    
    # Opciones para el tipo de mesa
    TIPO_CHOICES = [
        ('individual', 'Individual (1-2 personas)'),
        ('pequeña', 'Pequeña (3-4 personas)'),
        ('mediana', 'Mediana (5-6 personas)'),
        ('grande', 'Grande (7-8 personas)'),
        ('familiar', 'Familiar (9+ personas)'),
        ('vip', 'VIP'),
    ]
    
    # Campos básicos
    numero = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Número de Mesa",
        help_text="Identificador único de la mesa"
    )
    
    capacidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        verbose_name="Capacidad",
        help_text="Cantidad máxima de personas que pueden sentarse"
    )
    
    tipo_mesa = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='pequeña',
        verbose_name="Tipo de Mesa",
        help_text="Clasificación de la mesa según su capacidad"
    )
    
    ubicacion = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Ubicación",
        help_text="Zona del restaurante donde está ubicada la mesa"
    )
    
    caracteristicas = models.TextField(
        blank=True,
        verbose_name="Características",
        help_text="Características especiales de la mesa (vista, accesibilidad, etc.)"
    )
    
    # Estado y ocupación
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='libre',
        verbose_name="Estado",
        help_text="Estado actual de la mesa"
    )
    
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa",
        help_text="Indica si la mesa está disponible para servicio"
    )
    
    # Relaciones opcionales para ocupación actual
    cliente_actual = models.ForeignKey(
        ClienteModelo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mesa_ocupada',
        verbose_name="Cliente Actual",
        help_text="Cliente que actualmente ocupa la mesa"
    )
    
    cantidad_personas_actual = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        verbose_name="Personas Actuales",
        help_text="Cantidad de personas actualmente en la mesa"
    )
    
    pedido_id_actual = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Pedido Actual",
        help_text="ID del pedido asociado a la mesa actual"
    )
    
    # Timestamps de ocupación
    hora_ocupacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hora de Ocupación",
        help_text="Momento en que la mesa fue ocupada"
    )
    
    hora_liberacion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Hora de Liberación",
        help_text="Momento en que la mesa fue liberada"
    )
    
    # Estadísticas y métricas
    tiempo_servicio_promedio = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Tiempo Promedio de Servicio",
        help_text="Tiempo promedio de servicio en minutos"
    )
    
    total_servicios = models.PositiveIntegerField(
        default=0,
        verbose_name="Total de Servicios",
        help_text="Número total de veces que la mesa ha sido ocupada"
    )
    
    # Metadatos
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )

    
    class Meta:
        db_table = 'mesas'
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        ordering = ['numero']
        indexes = [
            models.Index(fields=['numero']),
            models.Index(fields=['estado']),
            models.Index(fields=['capacidad']),
            models.Index(fields=['tipo_mesa']),
            models.Index(fields=['activa']),
        ]
    
    def clean(self):
        """Validaciones personalizadas del modelo"""
        super().clean()
        
        # Validar consistencia entre tipo y capacidad
        self._validar_tipo_capacidad()
        
        # Validar estado de ocupación
        self._validar_estado_ocupacion()
        
        # Validar cantidad de personas
        self._validar_cantidad_personas()
    
    def _validar_tipo_capacidad(self):
        """Valida que el tipo de mesa sea consistente con la capacidad"""
        rangos_capacidad = {
            'individual': (1, 2),
            'pequeña': (3, 4),
            'mediana': (5, 6),
            'grande': (7, 8),
            'familiar': (9, 20),
            'vip': (1, 20)  # VIP puede tener cualquier capacidad
        }
        
        if self.tipo_mesa in rangos_capacidad:
            min_cap, max_cap = rangos_capacidad[self.tipo_mesa]
            if not (min_cap <= self.capacidad <= max_cap):
                raise ValidationError(
                    f"Una mesa {self.tipo_mesa} debe tener entre {min_cap} y {max_cap} personas"
                )
    
    def _validar_estado_ocupacion(self):
        """Valida la consistencia entre estado y datos de ocupación"""
        if self.estado == 'ocupada':
            if not self.cliente_actual:
                raise ValidationError("Una mesa ocupada debe tener un cliente asignado")
            if not self.cantidad_personas_actual:
                raise ValidationError("Una mesa ocupada debe tener cantidad de personas")
        
        elif self.estado == 'reservada':
            if not self.cliente_actual:
                raise ValidationError("Una mesa reservada debe tener un cliente asignado")
        
        elif self.estado in ['libre', 'limpieza', 'fuera_servicio']:
            if self.estado == 'libre' and (self.cliente_actual or self.cantidad_personas_actual):
                raise ValidationError("Una mesa libre no puede tener cliente o personas asignadas")
    
    def _validar_cantidad_personas(self):
        """Valida que la cantidad de personas no exceda la capacidad"""
        if self.cantidad_personas_actual and self.cantidad_personas_actual > self.capacidad:
            raise ValidationError(
                f"La cantidad de personas ({self.cantidad_personas_actual}) "
                f"no puede exceder la capacidad de la mesa ({self.capacidad})"
            )
    
    def save(self, *args, **kwargs):
        """Override del método save para ejecutar validaciones"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def esta_libre(self):
        """Determina si la mesa está libre para ser ocupada"""
        return self.estado == 'libre' and self.activa
    
    @property
    def esta_ocupada(self):
        """Determina si la mesa está ocupada"""
        return self.estado == 'ocupada'
    
    @property
    def puede_reservarse(self):
        """Determina si la mesa puede ser reservada"""
        return self.estado == 'libre' and self.activa
    
    def es_adecuada_para(self, cantidad_personas):
        """
        Verifica si la mesa es adecuada para una cantidad de personas
        
        Args:
            cantidad_personas (int): Cantidad de personas a ubicar
            
        Returns:
            bool: True si la mesa es adecuada, False en caso contrario
        """
        # Una mesa es adecuada si tiene capacidad suficiente sin desperdiciar demasiado espacio
        return (self.capacidad >= cantidad_personas and self.capacidad <= cantidad_personas + 2)
    
    def obtener_tiempo_ocupacion_actual(self):
        """
        Calcula el tiempo actual de ocupación en minutos
        
        Returns:
            int: Tiempo en minutos, None si no está ocupada
        """
        if not self.esta_ocupada or not self.hora_ocupacion:
            return None
        
        from django.utils import timezone
        tiempo_ocupacion = timezone.now() - self.hora_ocupacion
        return int(tiempo_ocupacion.total_seconds() / 60)
    
    def calcular_tiempo_servicio(self):
        """
        Calcula el tiempo de servicio basado en hora de ocupación y liberación
        
        Returns:
            int: Tiempo de servicio en minutos, None si no hay datos suficientes
        """
        if not self.hora_ocupacion or not self.hora_liberacion:
            return None
        
        tiempo_servicio = self.hora_liberacion - self.hora_ocupacion
        return int(tiempo_servicio.total_seconds() / 60)
    
    def actualizar_tiempo_promedio(self, nuevo_tiempo):
        """
        Actualiza el tiempo promedio de servicio con un nuevo tiempo
        
        Args:
            nuevo_tiempo (int): Nuevo tiempo de servicio en minutos
        """
        if self.tiempo_servicio_promedio is None:
            self.tiempo_servicio_promedio = nuevo_tiempo
        else:
            # Promedio ponderado (70% histórico, 30% actual)
            self.tiempo_servicio_promedio = int(
                (self.tiempo_servicio_promedio * 0.7) + (nuevo_tiempo * 0.3)
            )
    
    def incrementar_servicios(self):
        """Incrementa el contador de servicios totales"""
        self.total_servicios += 1
    
    def obtener_resumen_estado(self):
        """Retorna un resumen del estado actual de la mesa"""
        estado_base = f"Mesa {self.numero} ({self.capacidad} personas) - {self.get_estado_display()}"
        
        if self.esta_ocupada and self.hora_ocupacion:
            tiempo_ocupacion = self.obtener_tiempo_ocupacion_actual()
            estado_base += f" - {tiempo_ocupacion} min"
        
        if not self.activa:
            estado_base += " - INACTIVA"
        
        return estado_base
    
    def __str__(self):
        return f"Mesa {self.numero} - {self.get_estado_display()} - {self.capacidad} personas"
