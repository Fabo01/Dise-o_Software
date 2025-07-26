# Backend/Presentacion/Controladores/Auth_Controlador.py
# Controlador de autenticación JWT

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers

from Backend.Aplicacion.Servicios.Autenticacion_Servicio import AutenticacionServicio
from Backend.Infraestructura.Modelos.Usuario_Modelo import UsuarioModelo


class CustomTokenObtainPairSerializer(serializers.Serializer):
    """Serializer personalizado para login con RUT"""
    rut = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        rut = attrs.get('rut')
        password = attrs.get('password')

        try:
            # Buscar usuario por RUT
            usuario = UsuarioModelo.objects.get(rut=rut)
            
            # Verificación de contraseña simple para demo
            if password in ["admin123", "password123", "1234"]:
                return {
                    'rut': rut,
                    'usuario': usuario
                }
            else:
                raise serializers.ValidationError('Credenciales inválidas')
                
        except UsuarioModelo.DoesNotExist:
            raise serializers.ValidationError('Usuario no encontrado')


class LoginView(APIView):
    """
    Endpoint para autenticación de usuarios.
    """
    
    def post(self, request):
        """
        Autentica un usuario y retorna tokens JWT.
        
        Body:
        {
            "rut": "string",
            "password": "string"
        }
        """
        # Mantener compatibilidad con username y rut
        rut = request.data.get('rut') or request.data.get('username')
        password = request.data.get('password')
        
        if not rut or not password:
            return Response({
                'error': 'RUT y password son requeridos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Usar el serializer personalizado
        serializer = CustomTokenObtainPairSerializer(data={'rut': rut, 'password': password})
        
        try:
            serializer.is_valid(raise_exception=True)
            usuario = serializer.validated_data['usuario']
            
            # Crear o obtener usuario Django para JWT
            django_user, created = User.objects.get_or_create(
                username=usuario.rut,
                defaults={
                    'first_name': usuario.nombre,
                    'last_name': usuario.apellido,
                    'email': usuario.email
                }
            )
            
            # Generar tokens JWT
            refresh = RefreshToken.for_user(django_user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'rut': usuario.rut,
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'rol': usuario.rol,
                    'email': usuario.email
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class LogoutView(APIView):
    """Vista para logout"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({'message': 'Logout exitoso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Token inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )


class PerfilUsuarioView(APIView):
    """Vista para obtener perfil del usuario autenticado"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Obtener usuario por username (que es el RUT)
            usuario = UsuarioModelo.objects.get(rut=request.user.username)
            
            return Response({
                'rut': usuario.rut,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'rol': usuario.rol,
                'email': usuario.email,
                'telefono': usuario.telefono,
                'direccion': usuario.direccion,
                'fecha_registro': usuario.fecha_registro
            }, status=status.HTTP_200_OK)
            
        except UsuarioModelo.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )


class RefreshTokenView(APIView):
    """
    Endpoint para refrescar tokens de acceso.
    """
    
    def post(self, request):
        """
        Refresca un token de acceso usando un refresh token.
        
        Body:
        {
            "refresh_token": "string"
        }
        """
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({
                'error': 'Refresh token es requerido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        new_access_token = AutenticacionServicio.refrescar_token(refresh_token)
        
        if not new_access_token:
            return Response({
                'error': 'Refresh token inválido o expirado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'access_token': new_access_token,
            'token_type': 'bearer'
        }, status=status.HTTP_200_OK)

class VerifyTokenView(APIView):
    """
    Endpoint para verificar la validez de un token.
    """
    
    def post(self, request):
        """
        Verifica si un token es válido.
        
        Body:
        {
            "token": "string"
        }
        """
        token = request.data.get('token')
        
        if not token:
            return Response({
                'error': 'Token es requerido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        payload = AutenticacionServicio.verificar_token(token)
        
        if not payload:
            return Response({
                'valid': False,
                'error': 'Token inválido o expirado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'valid': True,
            'payload': payload
        }, status=status.HTTP_200_OK)

class RegistroView(APIView):
    """
    Endpoint para registro de nuevos usuarios (solo administradores).
    """
    
    def post(self, request):
        """
        Registra un nuevo usuario en el sistema.
        
        Body:
        {
            "rut": "string",
            "username": "string", 
            "nombre": "string",
            "apellido": "string",
            "rol": "string",
            "email": "string",
            "password": "string"
        }
        """
        # Verificar token de administrador
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            payload = AutenticacionServicio.verificar_token(token)
            
            if not payload or payload.get('rol') != 'administrador':
                return Response({
                    'error': 'Solo administradores pueden registrar usuarios'
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'error': 'Token de autenticación requerido'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Validar datos requeridos
        campos_requeridos = ['rut', 'username', 'nombre', 'rol', 'email', 'password']
        for campo in campos_requeridos:
            if not request.data.get(campo):
                return Response({
                    'error': f'{campo} es requerido'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Crear nuevo usuario
            usuario = UsuarioModelo.objects.create(
                rut=request.data['rut'],
                username=request.data['username'],
                nombre=request.data['nombre'],
                apellido=request.data.get('apellido', ''),
                rol=request.data['rol'],
                email=request.data['email'],
                telefono=request.data.get('telefono'),
                direccion=request.data.get('direccion'),
                password=make_password(request.data['password'])
            )
            
            return Response({
                'message': 'Usuario registrado exitosamente',
                'usuario': {
                    'rut': usuario.rut,
                    'username': usuario.username,
                    'nombre': usuario.nombre,
                    'rol': usuario.rol,
                    'email': usuario.email
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': f'Error al registrar usuario: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

class PerfilView(APIView):
    """
    Endpoint para obtener información del perfil del usuario autenticado.
    """
    
    def get(self, request):
        """
        Obtiene la información del perfil del usuario autenticado.
        """
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({
                'error': 'Token de autenticación requerido'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        token = auth_header.split(' ')[1]
        payload = AutenticacionServicio.verificar_token(token)
        
        if not payload:
            return Response({
                'error': 'Token inválido o expirado'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            usuario = UsuarioModelo.objects.get(rut=payload['rut'])
            return Response({
                'rut': usuario.rut,
                'username': usuario.username,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'rol': usuario.rol,
                'email': usuario.email,
                'telefono': usuario.telefono,
                'direccion': usuario.direccion,
                'fecha_registro': usuario.fecha_registro,
                'ultima_sesion': usuario.ultima_sesion
            }, status=status.HTTP_200_OK)
            
        except UsuarioModelo.DoesNotExist:
            return Response({
                'error': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
