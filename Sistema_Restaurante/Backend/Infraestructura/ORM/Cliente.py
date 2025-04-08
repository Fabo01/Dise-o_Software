from django.db import models
import json

class Cliente(models.Model):
    """
    Modelo para representar a los clientes del restaurante.
    """
    ESTADOS_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('bloqueado', 'Bloqueado'),
    )
    
    rut = models.CharField(max_length=12, primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    preferencias = models.JSONField(default=dict, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_visita = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=10, choices=ESTADOS_CHOICES, default='activo')
    
    class Meta:
        db_table = 'cliente'
        ordering = ['nombre']
        
    def __str__(self):
        return f"{self.nombre} ({self.rut})"
    
    def get_preferencias(self):
        """Obtiene las preferencias del cliente como un diccionario"""
        if isinstance(self.preferencias, str):
            try:
                return json.loads(self.preferencias)
            except json.JSONDecodeError:
                return {}
        return self.preferencias
    
    def set_preferencia(self, clave, valor):
        """Establece una preferencia específica para el cliente"""
        preferencias = self.get_preferencias()
        preferencias[clave] = valor
        self.preferencias = preferencias
        self.save()
    
    def registrar_visita(self):
        """Actualiza la fecha de última visita del cliente"""
        # Django actualiza automáticamente el campo auto_now
        self.save(update_fields=['ultima_visita'])
    
    def tiene_pedidos_activos(self):
        """Verifica si el cliente tiene pedidos activos"""
        return self.pedido_set.exclude(estado__in=['cancelado', 'pagado', 'completado']).exists()
