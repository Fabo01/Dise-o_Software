"""
Script para probar la API de clientes.
Este script permite comprobar el correcto funcionamiento de la API de clientes
realizando operaciones CRUD y verificando los resultados.
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = 'http://localhost:8000/api'  # Ajusta según tu configuración

def imprimir_respuesta(respuesta):
    """Imprime una respuesta de la API de forma legible"""
    print(f"Estado: {respuesta.status_code}")
    if respuesta.text:
        try:
            print(f"Respuesta: {json.dumps(respuesta.json(), indent=2, ensure_ascii=False)}")
        except:
            print(f"Respuesta: {respuesta.text}")
    print("-----------------------------------")

def crear_cliente():
    """Crea un nuevo cliente"""
    print("\n=== CREAR CLIENTE ===")
    datos_cliente = {
        "nombre": "Juan Pérez",
        "rut": "12345678-9",
        "correo": "juan@example.com",  # Asegúrate de que este campo esté presente
        "telefono": "912345678",
        "direccion": "Calle Ejemplo 123"
    }
    
    respuesta = requests.post(f"{BASE_URL}/clientes/", json=datos_cliente)
    imprimir_respuesta(respuesta)
    
    if respuesta.status_code == 201:
        return respuesta.json()["id"]
    return None

def obtener_cliente(cliente_id):
    """Obtiene los detalles de un cliente"""
    print(f"\n=== OBTENER CLIENTE {cliente_id} ===")
    respuesta = requests.get(f"{BASE_URL}/clientes/{cliente_id}/")
    imprimir_respuesta(respuesta)

def listar_clientes():
    """Lista todos los clientes"""
    print("\n=== LISTAR CLIENTES ===")
    respuesta = requests.get(f"{BASE_URL}/clientes/")
    imprimir_respuesta(respuesta)

def buscar_cliente_por_nombre():
    """Busca clientes por nombre"""
    print("\n=== BUSCAR CLIENTE POR NOMBRE ===")
    respuesta = requests.get(f"{BASE_URL}/clientes/?nombre=juan")
    imprimir_respuesta(respuesta)

def buscar_cliente_por_rut():
    """Busca un cliente por RUT"""
    print("\n=== BUSCAR CLIENTE POR RUT ===")
    respuesta = requests.get(f"{BASE_URL}/clientes/?rut=12345678-9")
    imprimir_respuesta(respuesta)

def actualizar_cliente(cliente_id):
    """Actualiza los datos de un cliente"""
    print(f"\n=== ACTUALIZAR CLIENTE {cliente_id} ===")
    datos_actualizados = {
        "nombre": "Juan Pérez Actualizado",
        "rut": "12345678-9",  # No se puede cambiar el RUT
        "correo": "juan.actualizado@example.com",
        "telefono": "987654321",
        "direccion": "Nueva Dirección 456"
    }
    
    respuesta = requests.put(f"{BASE_URL}/clientes/{cliente_id}/", json=datos_actualizados)
    imprimir_respuesta(respuesta)

def desactivar_cliente(cliente_id):
    """Desactiva un cliente"""
    print(f"\n=== DESACTIVAR CLIENTE {cliente_id} ===")
    respuesta = requests.post(f"{BASE_URL}/clientes/{cliente_id}/estado/", json={"accion": "desactivar"})
    imprimir_respuesta(respuesta)

def activar_cliente(cliente_id):
    """Activa un cliente"""
    print(f"\n=== ACTIVAR CLIENTE {cliente_id} ===")
    respuesta = requests.post(f"{BASE_URL}/clientes/{cliente_id}/estado/", json={"accion": "activar"})
    imprimir_respuesta(respuesta)

def registrar_visita(cliente_id):
    """Registra una visita para un cliente"""
    print(f"\n=== REGISTRAR VISITA CLIENTE {cliente_id} ===")
    respuesta = requests.post(f"{BASE_URL}/clientes/{cliente_id}/visita/")
    imprimir_respuesta(respuesta)

def eliminar_cliente(cliente_id):
    """Elimina un cliente"""
    print(f"\n=== ELIMINAR CLIENTE {cliente_id} ===")
    respuesta = requests.delete(f"{BASE_URL}/clientes/{cliente_id}/")
    imprimir_respuesta(respuesta)

def ejecutar_pruebas():
    """Ejecuta todas las pruebas en secuencia"""
    print("Iniciando pruebas de la API de clientes...")
    
    # Crear cliente
    cliente_id = crear_cliente()
    if not cliente_id:
        print("Error al crear el cliente. Deteniendo pruebas.")
        return
        
    # Obtener detalles del cliente
    obtener_cliente(cliente_id)
    
    # Listar todos los clientes
    listar_clientes()
    
    # Buscar por nombre y RUT
    buscar_cliente_por_nombre()
    buscar_cliente_por_rut()
    
    # Actualizar cliente
    actualizar_cliente(cliente_id)
    obtener_cliente(cliente_id)  # Verificar actualización
    
    # Probar estados
    desactivar_cliente(cliente_id)
    activar_cliente(cliente_id)
    
    # Registrar visita
    registrar_visita(cliente_id)
    obtener_cliente(cliente_id)  # Ver última visita actualizada
    
    # Eliminar cliente
    eliminar_cliente(cliente_id)
    obtener_cliente(cliente_id)  # Verificar eliminación
    
    print("Pruebas completadas.")

if __name__ == "__main__":
    ejecutar_pruebas()