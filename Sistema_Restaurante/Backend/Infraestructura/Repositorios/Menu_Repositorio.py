from django.db.models import Q, Count, Avg, Sum
from django.db import transaction
from typing import List, Optional
from decimal import Decimal
from datetime import datetime

from Backend.Dominio.Entidades.Menu_Entidad import MenuEntidad
from Backend.Dominio.Interfaces.IMenuRepositorio import IMenuRepositorio
from Backend.Dominio.Objetos_Valor.PrecioVO import PrecioVO
from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo
from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo


class MenuRepositorio(IMenuRepositorio):
    """
    Implementación concreta del repositorio de menús usando Django ORM.
    Maneja la persistencia y recuperación de entidades de menú.
    """
    
    def guardar(self, menu: MenuEntidad) -> MenuEntidad:
        """
        Guarda o actualiza un menú en la base de datos.
        
        Args:
            menu (MenuEntidad): La entidad de menú a guardar
            
        Returns:
            MenuEntidad: La entidad guardada con su ID actualizado
        """
        with transaction.atomic():
            if menu.id:
                # Actualizar menú existente
                menu_modelo = MenuModelo.objects.get(id=menu.id)
                self._actualizar_modelo_desde_entidad(menu_modelo, menu)
                menu_modelo.save()
            else:
                # Crear nuevo menú
                menu_modelo = self._crear_modelo_desde_entidad(menu)
                menu_modelo.save()
                menu.id = menu_modelo.id
            
            # Gestionar ingredientes
            self._actualizar_ingredientes(menu_modelo, menu.ingredientes)
            
            return self._convertir_a_entidad(menu_modelo)
    
    def buscar_por_id(self, id: int) -> Optional[MenuEntidad]:
        """
        Busca un menú por su ID.
        
        Args:
            id (int): ID del menú a buscar
            
        Returns:
            Optional[MenuEntidad]: La entidad encontrada o None
        """
        try:
            menu_modelo = MenuModelo.objects.select_related().prefetch_related('ingredientes').get(id=id)
            return self._convertir_a_entidad(menu_modelo)
        except MenuModelo.DoesNotExist:
            return None
    
    def buscar_por_nombre(self, nombre: str) -> List[MenuEntidad]:
        """
        Busca menús que contengan el nombre especificado.
        
        Args:
            nombre (str): Nombre o parte del nombre a buscar
            
        Returns:
            List[MenuEntidad]: Lista de menús encontrados
        """
        menus_modelo = MenuModelo.objects.filter(
            nombre__icontains=nombre
        ).prefetch_related('ingredientes')
        
        return [self._convertir_a_entidad(menu) for menu in menus_modelo]
    
    def buscar_por_categoria(self, categoria: str) -> List[MenuEntidad]:
        """
        Busca menús por categoría.
        
        Args:
            categoria (str): Categoría a buscar
            
        Returns:
            List[MenuEntidad]: Lista de menús de la categoría
        """
        menus_modelo = MenuModelo.objects.filter(
            categoria__iexact=categoria
        ).prefetch_related('ingredientes')
        
        return [self._convertir_a_entidad(menu) for menu in menus_modelo]
    
    def buscar_por_tipo(self, tipo: str) -> List[MenuEntidad]:
        """
        Busca menús por tipo.
        
        Args:
            tipo (str): Tipo a buscar
            
        Returns:
            List[MenuEntidad]: Lista de menús del tipo especificado
        """
        menus_modelo = MenuModelo.objects.filter(
            tipo__iexact=tipo
        ).prefetch_related('ingredientes')
        
        return [self._convertir_a_entidad(menu) for menu in menus_modelo]
    
    def buscar_por_rango_precio(self, precio_min: Decimal, precio_max: Decimal) -> List[MenuEntidad]:
        """
        Busca menús dentro de un rango de precios.
        
        Args:
            precio_min (Decimal): Precio mínimo
            precio_max (Decimal): Precio máximo
            
        Returns:
            List[MenuEntidad]: Lista de menús en el rango de precios
        """
        menus_modelo = MenuModelo.objects.filter(
            precio__gte=precio_min,
            precio__lte=precio_max
        ).prefetch_related('ingredientes')
        
        return [self._convertir_a_entidad(menu) for menu in menus_modelo]
    
    def listar_disponibles(self) -> List[MenuEntidad]:
        """
        Lista todos los menús disponibles.
        
        Returns:
            List[MenuEntidad]: Lista de menús disponibles
        """
        menus_modelo = MenuModelo.objects.filter(
            disponible=True
        ).prefetch_related('ingredientes').order_by('categoria', 'nombre')
        
        return [self._convertir_a_entidad(menu) for menu in menus_modelo]
    
    def listar_todos(self) -> List[MenuEntidad]:
        """
        Lista todos los menús.
        
        Returns:
            List[MenuEntidad]: Lista de todos los menús
        """
        menus_modelo = MenuModelo.objects.all().prefetch_related('ingredientes').order_by('categoria', 'nombre')
        return [self._convertir_a_entidad(menu) for menu in menus_modelo]
    
    def listar_por_popularidad(self, limite: int = 10) -> List[MenuEntidad]:
        """
        Lista los menús más populares (más ordenados).
        
        Args:
            limite (int): Número máximo de menús a retornar
            
        Returns:
            List[MenuEntidad]: Lista de menús ordenados por popularidad
        """
        menus_modelo = MenuModelo.objects.filter(
            disponible=True
        ).prefetch_related('ingredientes').order_by('-veces_ordenado')[:limite]
        
        return [self._convertir_a_entidad(menu) for menu in menus_modelo]
    
    def buscar_con_ingrediente(self, ingrediente_id: int) -> List[MenuEntidad]:
        """
        Busca menús que contengan un ingrediente específico.
        
        Args:
            ingrediente_id (int): ID del ingrediente
            
        Returns:
            List[MenuEntidad]: Lista de menús que contienen el ingrediente
        """
        menus_modelo = MenuModelo.objects.filter(
            ingredientes__id=ingrediente_id
        ).prefetch_related('ingredientes')
        
        return [self._convertir_a_entidad(menu) for menu in menus_modelo]
    
    def contar_total(self) -> int:
        """
        Cuenta el total de menús.
        
        Returns:
            int: Número total de menús
        """
        return MenuModelo.objects.count()
    
    def contar_disponibles(self) -> int:
        """
        Cuenta los menús disponibles.
        
        Returns:
            int: Número de menús disponibles
        """
        return MenuModelo.objects.filter(disponible=True).count()
    
    def obtener_precio_promedio(self) -> Decimal:
        """
        Obtiene el precio promedio de los menús disponibles.
        
        Returns:
            Decimal: Precio promedio
        """
        resultado = MenuModelo.objects.filter(disponible=True).aggregate(
            promedio=Avg('precio')
        )
        return resultado['promedio'] or Decimal('0.00')
    
    def obtener_estadisticas_categoria(self) -> dict:
        """
        Obtiene estadísticas por categoría.
        
        Returns:
            dict: Estadísticas agrupadas por categoría
        """
        return MenuModelo.objects.values('categoria').annotate(
            total=Count('id'),
            disponibles=Count('id', filter=Q(disponible=True)),
            precio_promedio=Avg('precio'),
            total_ordenado=Sum('veces_ordenado')
        ).order_by('categoria')
    
    def eliminar(self, id: int) -> bool:
        """
        Elimina un menú por su ID.
        
        Args:
            id (int): ID del menú a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existía
        """
        try:
            menu = MenuModelo.objects.get(id=id)
            menu.delete()
            return True
        except MenuModelo.DoesNotExist:
            return False
    
    def existe(self, id: int) -> bool:
        """
        Verifica si existe un menú con el ID dado.
        
        Args:
            id (int): ID del menú
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        return MenuModelo.objects.filter(id=id).exists()
    
    def _crear_modelo_desde_entidad(self, menu: MenuEntidad) -> MenuModelo:
        """
        Crea un modelo ORM desde una entidad de dominio.
        
        Args:
            menu (MenuEntidad): Entidad de menú
            
        Returns:
            MenuModelo: Modelo ORM creado
        """
        return MenuModelo(
            nombre=menu.nombre,
            descripcion=menu.descripcion,
            precio=menu.precio.valor,
            categoria=menu.categoria,
            tipo=menu.tipo,
            imagen=menu.imagen,
            disponible=menu.disponible,
            tiempo_preparacion=menu.tiempo_preparacion or 15
        )
    
    def _actualizar_modelo_desde_entidad(self, menu_modelo: MenuModelo, menu: MenuEntidad):
        """
        Actualiza un modelo ORM desde una entidad de dominio.
        
        Args:
            menu_modelo (MenuModelo): Modelo ORM a actualizar
            menu (MenuEntidad): Entidad de dominio con los nuevos datos
        """
        menu_modelo.nombre = menu.nombre
        menu_modelo.descripcion = menu.descripcion
        menu_modelo.precio = menu.precio.valor
        menu_modelo.categoria = menu.categoria
        menu_modelo.tipo = menu.tipo
        menu_modelo.imagen = menu.imagen
        menu_modelo.disponible = menu.disponible
        menu_modelo.tiempo_preparacion = menu.tiempo_preparacion or 15
    
    def _actualizar_ingredientes(self, menu_modelo: MenuModelo, ingredientes_ids: List[int]):
        """
        Actualiza los ingredientes asociados a un menú.
        
        Args:
            menu_modelo (MenuModelo): Modelo del menú
            ingredientes_ids (List[int]): Lista de IDs de ingredientes
        """
        if ingredientes_ids:
            ingredientes = IngredienteModelo.objects.filter(id__in=ingredientes_ids)
            menu_modelo.ingredientes.set(ingredientes)
        else:
            menu_modelo.ingredientes.clear()
    
    def _convertir_a_entidad(self, menu_modelo: MenuModelo) -> MenuEntidad:
        """
        Convierte un modelo ORM a una entidad de dominio.
        
        Args:
            menu_modelo (MenuModelo): Modelo ORM
            
        Returns:
            MenuEntidad: Entidad de dominio
        """
        menu = MenuEntidad(
            nombre=menu_modelo.nombre,
            descripcion=menu_modelo.descripcion,
            precio=menu_modelo.precio,
            categoria=menu_modelo.categoria,
            tipo=menu_modelo.tipo,
            imagen=menu_modelo.imagen
        )
        
        # Establecer propiedades adicionales
        menu.id = menu_modelo.id
        menu.disponible = menu_modelo.disponible
        menu.fecha_creacion = menu_modelo.fecha_creacion
        menu.fecha_actualizacion = menu_modelo.fecha_actualizacion
        menu.veces_ordenado = menu_modelo.veces_ordenado
        menu.tiempo_preparacion = menu_modelo.tiempo_preparacion
        
        # Cargar ingredientes
        if hasattr(menu_modelo, 'ingredientes'):
            menu.ingredientes = [ing.id for ing in menu_modelo.ingredientes.all()]
        
        return menu
    
    def existe_por_nombre(self, nombre: str) -> bool:
        """
        Verifica si existe un menú con el nombre dado.
        
        Args:
            nombre: Nombre del menú
            
        Returns:
            True si existe, False en caso contrario
        """
        return MenuModelo.objects.filter(nombre__iexact=nombre).exists()
