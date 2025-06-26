from Backend.Dominio.Entidades.Ingrediente_Entidad import IngredienteEntidad
from Backend.Dominio.Interfaces.IEntidad_Factory import IEntidadFactory
from datetime import datetime
from pathlib import Path

class IngredienteFactory(IEntidadFactory):
    """
    Factory para crear instancias de IngredienteEntidad con validación
    y procesamiento previo de los datos.
    """
    IMAGEN_DIR = Path("Backend/Static/Imagenes/Ingredientes")
    
    def crear(self, nombre, cantidad, unidad_medida, fecha_vencimiento=None, nivel_critico=None, tipo=None):
        """
        Crea una nueva instancia de IngredienteEntidad.
        
        Args:
            nombre (str): Nombre del ingrediente (será formateado)
            cantidad (float): Cantidad disponible del ingrediente
            unidad_medida (str): Unidad de medida del ingrediente
            fecha_vencimiento (datetime, opcional): Fecha de vencimiento
            nivel_critico (float, opcional): Nivel crítico de stock
            tipo (str, opcional): Categoría del ingrediente
            
        Returns:
            IngredienteEntidad: Nueva instancia del ingrediente
        """
        # Formateo de datos
        nombre = nombre.strip().title() if nombre else ''
        unidad_medida = unidad_medida.lower().strip() if unidad_medida else ''
        
        # Manejo de fecha de vencimiento
        if fecha_vencimiento is None:
            # Si no se proporciona fecha, podríamos establecer una por defecto
            # Por ejemplo, 6 meses en el futuro
            fecha_vencimiento = datetime.now().replace(month=datetime.now().month + 6)
        
        # Conversión a float para asegurar tipo correcto
        if cantidad is not None:
            cantidad = float(cantidad)
        if nivel_critico is not None:
            nivel_critico = float(nivel_critico)
        
        # Creación de la entidad
        return IngredienteEntidad(
            nombre=nombre,
            cantidad=cantidad,
            unidad_medida=unidad_medida,
            fecha_vencimiento=fecha_vencimiento,
            nivel_critico=nivel_critico,
            tipo=tipo
        )