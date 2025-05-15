from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from Backend.Aplicacion.Servicios.Cliente_Servicio import ClienteServicio
from Backend.Infraestructura.Repositorios.Cliente_Repositorio import ClienteRepositorio
from Backend.Presentacion.Serializadores.Cliente_Serializador import ClienteSerializador
from Backend.Aplicacion.Servicios.ConsoleNotificationObserver import ConsoleNotificationObserver
from Backend.Aplicacion.Servicios.ObserverService import ObserverService

class ClienteAPI(APIView):
    """
    API para la gestión de clientes
    """
    observer_service = ObserverService()
    observer_registrado = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inyección de dependencias (Repository Pattern)
        self.servicio_cliente = ClienteServicio(ClienteRepositorio(), observer_service=ClienteAPI.observer_service)

    def get(self, request, id=None):
        """
        Obtiene un cliente por su ID o lista todos los clientes
        
        Args:
            request: Objeto request de Django
            id (int, opcional): ID del cliente a obtener
            
        Returns:
            Response: Respuesta HTTP con los datos del cliente o lista de clientes
        """
        if id:
            try:
                cliente = self.servicio_cliente.obtener_cliente(id)
                if not cliente:
                    return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)
                    
                serializer = ClienteSerializador(cliente)
                return Response(serializer.data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Parámetros de filtro
            solo_activos = request.query_params.get('activos', 'false').lower() == 'true'
            nombre = request.query_params.get('nombre')
            rut = request.query_params.get('rut')
            
            try:
                if rut:
                    cliente = self.servicio_cliente.buscar_cliente_por_rut(rut)
                    if not cliente:
                        return Response([], status=status.HTTP_200_OK)
                    clientes = [cliente]
                elif nombre:
                    clientes = self.servicio_cliente.buscar_clientes_por_nombre(nombre)
                else:
                    clientes = self.servicio_cliente.listar_clientes(solo_activos)
                    
                serializer = ClienteSerializador(clientes, many=True)
                return Response(serializer.data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """
        Crea un nuevo cliente
        
        Args:
            request: Objeto request de Django con los datos del cliente
            
        Returns:
            Response: Respuesta HTTP con los datos del cliente creado o errores de validación
        """
        serializer = ClienteSerializador(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            cliente = self.servicio_cliente.registrar_cliente(serializer.validated_data)
            return Response(ClienteSerializador(cliente).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, id):
        """
        Actualiza un cliente existente
        
        Args:
            request: Objeto request de Django con los datos del cliente
            id (int): ID del cliente a actualizar
            
        Returns:
            Response: Respuesta HTTP con los datos del cliente actualizado o errores de validación
        """
        serializer = ClienteSerializador(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            cliente = self.servicio_cliente.actualizar_cliente(id, serializer.validated_data)
            cliente.correo = serializer.validated_data.get('correo')
            cliente.estado = serializer.validated_data.get('estado', cliente.estado)
            return Response(ClienteSerializador(cliente).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, id):
        """
        Elimina un cliente
        
        Args:
            request: Objeto request de Django
            id (int): ID del cliente a eliminar
            
        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        try:
            resultado = self.servicio_cliente.eliminar_cliente(id)
            if resultado:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Cliente no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Endpoint para registrar un observer de consola y probar el patrón observer
    def post_registrar_observer(self, request):
        """
        Endpoint de prueba para registrar un observer de consola.
        """
        if not ClienteAPI.observer_registrado:
            observer = ConsoleNotificationObserver()
            ClienteAPI.observer_service.registrar(observer)
            ClienteAPI.observer_registrado = True
            return Response({"mensaje": "Observer de consola registrado. Ahora cualquier registro de cliente notificará en consola."})
        else:
            return Response({"mensaje": "Observer ya estaba registrado."})


class ClienteEstadoAPI(APIView):
    """
    API para gestionar el estado de los clientes (activar/desactivar)
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inyección de dependencias
        self.servicio_cliente = ClienteServicio(ClienteRepositorio())
    
    def post(self, request, id):
        """
        Activa o desactiva un cliente
        
        Args:
            request: Objeto request de Django con la acción a realizar
            id (int): ID del cliente
            
        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        accion = request.data.get('accion')
        if not accion or accion not in ('activar', 'desactivar'):
            return Response({"error": "Se debe especificar una acción válida: 'activar' o 'desactivar'"}, 
                           status=status.HTTP_400_BAD_REQUEST)
                           
        try:
            if accion == 'activar':
                cliente = self.servicio_cliente.activar_cliente(id)
            else:
                cliente = self.servicio_cliente.desactivar_cliente(id)
                
            return Response(ClienteSerializador(cliente).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClienteVisitaAPI(APIView):
    """
    API para registrar visitas de clientes
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inyección de dependencias
        self.servicio_cliente = ClienteServicio(ClienteRepositorio())
    
    def post(self, request, id):
        """
        Registra una visita para un cliente
        
        Args:
            request: Objeto request de Django
            id (int): ID del cliente
            
        Returns:
            Response: Respuesta HTTP con el resultado de la operación
        """
        try:
            cliente = self.servicio_cliente.registrar_visita_cliente(id)
            return Response(ClienteSerializador(cliente).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)