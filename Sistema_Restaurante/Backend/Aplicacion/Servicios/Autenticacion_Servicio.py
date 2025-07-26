# Backend/Aplicacion/Servicios/Autenticacion_Servicio.py
# S1-16, S3-16: Sistema de autenticación JWT

import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from Backend.Infraestructura.Modelos.Usuario_Modelo import UsuarioModelo
from Backend.Dominio.Excepciones.DominioExcepcion import ValidacionExcepcion

class AutenticacionServicio:
    """
    Servicio para manejar autenticación JWT y roles de usuario.
    Implementa las tareas S1-16 y S3-16 del backlog.
    """
    
    SECRET_KEY = getattr(settings, 'SECRET_KEY', 'default-secret-key')
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    
    @classmethod
    def autenticar_usuario(cls, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Autentica un usuario con username y contraseña.
        Retorna información del usuario si es válido, None si no.
        """
        try:
            usuario = UsuarioModelo.objects.get(username=username)
            
            if check_password(password, usuario.password):
                return {
                    'rut': usuario.rut,
                    'username': usuario.username,
                    'nombre': usuario.nombre,
                    'rol': usuario.rol,
                    'email': usuario.email
                }
            return None
            
        except UsuarioModelo.DoesNotExist:
            return None
    
    @classmethod
    def generar_token_acceso(cls, usuario_data: Dict[str, Any]) -> str:
        """
        Genera un token JWT de acceso con duración limitada.
        """
        payload = {
            'rut': usuario_data['rut'],
            'username': usuario_data['username'],
            'rol': usuario_data['rol'],
            'exp': datetime.utcnow() + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES),
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        
        return jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
    
    @classmethod
    def generar_token_refresh(cls, usuario_data: Dict[str, Any]) -> str:
        """
        Genera un token JWT de refresco con duración extendida.
        """
        payload = {
            'rut': usuario_data['rut'],
            'exp': datetime.utcnow() + timedelta(days=cls.REFRESH_TOKEN_EXPIRE_DAYS),
            'iat': datetime.utcnow(),
            'type': 'refresh'
        }
        
        return jwt.encode(payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
    
    @classmethod
    def verificar_token(cls, token: str) -> Optional[Dict[str, Any]]:
        """
        Verifica y decodifica un token JWT.
        Retorna el payload si es válido, None si no.
        """
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @classmethod
    def refrescar_token(cls, refresh_token: str) -> Optional[str]:
        """
        Genera un nuevo token de acceso usando un token de refresco válido.
        """
        payload = cls.verificar_token(refresh_token)
        
        if not payload or payload.get('type') != 'refresh':
            return None
        
        try:
            usuario = UsuarioModelo.objects.get(rut=payload['rut'])
            usuario_data = {
                'rut': usuario.rut,
                'username': usuario.username,
                'nombre': usuario.nombre,
                'rol': usuario.rol,
                'email': usuario.email
            }
            
            return cls.generar_token_acceso(usuario_data)
            
        except UsuarioModelo.DoesNotExist:
            return None
    
    @classmethod
    def verificar_permisos(cls, usuario_rol: str, accion: str) -> bool:
        """
        Verifica si un rol de usuario tiene permisos para realizar una acción.
        Implementa el sistema de roles del restaurante.
        """
        permisos = {
            'administrador': [
                'crear_usuario', 'editar_usuario', 'eliminar_usuario',
                'ver_reportes', 'gestionar_sistema', 'backup_datos',
                'configurar_sistema', 'ver_analytics'
            ],
            'gerente': [
                'ver_reportes', 'gestionar_pedidos', 'gestionar_mesas',
                'ver_analytics', 'gestionar_delivery', 'gestionar_pagos'
            ],
            'mesero': [
                'crear_pedido', 'ver_pedidos', 'gestionar_mesas',
                'ver_menu', 'procesar_pagos'
            ],
            'cocinero': [
                'ver_pedidos_cocina', 'actualizar_estado_pedido',
                'gestionar_ingredientes', 'ver_menu'
            ]
        }
        
        return accion in permisos.get(usuario_rol.lower(), [])
    
    @classmethod
    def login(cls, username: str, password: str) -> Optional[Dict[str, str]]:
        """
        Proceso completo de login: autentica y genera tokens.
        """
        usuario_data = cls.autenticar_usuario(username, password)
        
        if not usuario_data:
            return None
        
        access_token = cls.generar_token_acceso(usuario_data)
        refresh_token = cls.generar_token_refresh(usuario_data)
        
        # Actualizar última sesión
        try:
            usuario = UsuarioModelo.objects.get(username=username)
            usuario.ultima_sesion = datetime.now()
            usuario.save()
        except UsuarioModelo.DoesNotExist:
            pass
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer',
            'usuario': usuario_data
        }

# Decorador para proteger endpoints
def requiere_autenticacion(roles_permitidos=None):
    """
    Decorador para proteger endpoints con autenticación JWT.
    
    Args:
        roles_permitidos (list): Lista de roles que pueden acceder al endpoint
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            auth_header = request.headers.get('Authorization')
            
            if not auth_header or not auth_header.startswith('Bearer '):
                return {'error': 'Token de autenticación requerido'}, 401
            
            token = auth_header.split(' ')[1]
            payload = AutenticacionServicio.verificar_token(token)
            
            if not payload:
                return {'error': 'Token inválido o expirado'}, 401
            
            if roles_permitidos and payload.get('rol') not in roles_permitidos:
                return {'error': 'Permisos insuficientes'}, 403
            
            request.usuario = payload
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator
