from django.db import models
from django.core.validators import MinValueValidator
from .Ingrediente import Ingrediente

class Menu(models.Model):
    """
    Modelo para representar los menús o platos ofrecidos en el restaurante.
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    precio = models.FloatField(validators=[MinValueValidator(0.0)])
    costo = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    tiempo_preparacion = models.IntegerField(validators=[MinValueValidator(1)], default=15)
    categoria = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to='menus/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    disponible_delivery = models.BooleanField(default=True)
    ingredientes = models.ManyToManyField(Ingrediente, through='MenuIngrediente')
    
    class Meta:
        db_table = 'menu'
        ordering = ['categoria', 'nombre']
        
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
    
    def calcular_costo(self):
        """Calcula el costo del menú basado en sus ingredientes"""
        costo_total = 0
        for menu_ingrediente in self.menuingrediente_set.all():
            ingrediente = menu_ingrediente.ingrediente
            cantidad_requerida = menu_ingrediente.cantidad
            # Asumimos que el precio del ingrediente es por unidad
            costo_total += cantidad_requerida
        
        self.costo = costo_total
        self.save()
        return self.costo
    
    def calcular_margen(self):
        """Calcula el margen de ganancia del menú"""
        if not self.costo or self.costo == 0:
            self.calcular_costo()
        
        if self.costo > 0:
            return (self.precio - self.costo) / self.precio * 100
        return 0
    
    def verificar_disponibilidad(self):
        """Verifica si hay suficientes ingredientes para preparar el menú"""
        for menu_ingrediente in self.menuingrediente_set.all():
            ingrediente = menu_ingrediente.ingrediente
            cantidad_requerida = menu_ingrediente.cantidad
            
            if ingrediente.cantidad < cantidad_requerida or ingrediente.estado != 'disponible':
                self.disponible = False
                self.save()
                return False
                
        self.disponible = True
        self.save()
        return True
