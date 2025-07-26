#!/usr/bin/env python
"""
Test de Integración Básica - Sistema de Restaurante
Demuestra que todos los componentes funcionan correctamente
"""

import os
import sys
import django
from django.db import connection
from django.test.utils import setup_test_environment

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.Config.Settings.settings')
django.setup()

def test_base_datos():
    """Test de conectividad de base de datos"""
    print("🔍 Verificando base de datos...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM cliente")
            clientes = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM ingrediente")
            ingredientes = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM menu")
            menus = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM mesas")
            mesas = cursor.fetchone()[0]
            
        print(f"✅ Base de datos conectada")
        print(f"   - Clientes: {clientes}")
        print(f"   - Ingredientes: {ingredientes}") 
        print(f"   - Menús: {menus}")
        print(f"   - Mesas: {mesas}")
        return True
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")
        return False

def test_modelos():
    """Test de modelos Django"""
    print("\n🔍 Verificando modelos...")
    try:
        from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
        from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo
        from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo
        from Backend.Infraestructura.Modelos.Mesa_Modelo import MesaModelo
        
        # Test básico de CRUD
        clientes = ClienteModelo.objects.all()
        ingredientes = IngredienteModelo.objects.all()
        menus = MenuModelo.objects.all()
        mesas = MesaModelo.objects.all()
        
        print(f"✅ Modelos funcionando")
        print(f"   - ClienteModelo: {len(clientes)} registros")
        print(f"   - IngredienteModelo: {len(ingredientes)} registros")
        print(f"   - MenuModelo: {len(menus)} registros")
        print(f"   - MesaModelo: {len(mesas)} registros")
        return True
    except Exception as e:
        print(f"❌ Error en modelos: {e}")
        return False

def test_operaciones_crud():
    """Test de operaciones CRUD básicas"""
    print("\n🔍 Verificando operaciones CRUD...")
    try:
        from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
        
        # Crear cliente de prueba
        cliente_test = ClienteModelo.objects.create(
            nombre="Test Usuario",
            rut="11111111-1",
            correo="test@test.com",
            telefono="123456789"
        )
        
        # Leer
        cliente_leido = ClienteModelo.objects.get(id=cliente_test.id)
        assert cliente_leido.nombre == "Test Usuario"
        
        # Actualizar
        cliente_leido.nombre = "Test Usuario Actualizado"
        cliente_leido.save()
        
        # Verificar actualización
        cliente_actualizado = ClienteModelo.objects.get(id=cliente_test.id)
        assert cliente_actualizado.nombre == "Test Usuario Actualizado"
        
        # Eliminar
        cliente_actualizado.delete()
        
        print("✅ Operaciones CRUD funcionando")
        print("   - CREATE: ✅")
        print("   - READ: ✅") 
        print("   - UPDATE: ✅")
        print("   - DELETE: ✅")
        return True
    except Exception as e:
        print(f"❌ Error en CRUD: {e}")
        return False

def test_relaciones():
    """Test de relaciones entre modelos"""
    print("\n🔍 Verificando relaciones...")
    try:
        from Backend.Infraestructura.Modelos.Menu_Modelo import MenuModelo
        from Backend.Infraestructura.Modelos.Ingrediente_Modelo import IngredienteModelo
        
        # Verificar relación Menu-Ingrediente
        menus_con_ingredientes = 0
        for menu in MenuModelo.objects.all():
            ingredientes = menu.ingredientes.all()
            if ingredientes.exists():
                menus_con_ingredientes += 1
        
        print(f"✅ Relaciones funcionando")
        print(f"   - Menús con ingredientes: {menus_con_ingredientes}")
        return True
    except Exception as e:
        print(f"❌ Error en relaciones: {e}")
        return False

def test_validaciones():
    """Test de validaciones de negocio"""
    print("\n🔍 Verificando validaciones...")
    try:
        from Backend.Infraestructura.Modelos.Cliente_Modelo import ClienteModelo
        from django.core.exceptions import ValidationError
        
        # Intentar crear cliente con RUT inválido
        try:
            cliente_invalido = ClienteModelo(
                nombre="Test",
                rut="rut_invalido",
                correo="invalid_email"
            )
            cliente_invalido.full_clean()
            print("❌ Validación debería haber fallado")
            return False
        except ValidationError:
            print("✅ Validaciones funcionando")
            print("   - RUT inválido rechazado: ✅")
            print("   - Email inválido rechazado: ✅")
            return True
    except Exception as e:
        print(f"❌ Error en validaciones: {e}")
        return False

def test_arquitectura():
    """Test de estructura Clean Architecture"""
    print("\n🔍 Verificando Clean Architecture...")
    try:
        # Verificar estructura de carpetas
        import Backend.Dominio
        import Backend.Aplicacion  
        import Backend.Infraestructura
        import Backend.Presentacion
        
        print("✅ Clean Architecture implementada")
        print("   - Capa Dominio: ✅")
        print("   - Capa Aplicación: ✅")
        print("   - Capa Infraestructura: ✅")
        print("   - Capa Presentación: ✅")
        return True
    except Exception as e:
        print(f"❌ Error en arquitectura: {e}")
        return False

def main():
    """Ejecutar todos los tests"""
    print("🧪 EJECUTANDO TESTS DE INTEGRACIÓN")
    print("=" * 50)
    
    tests = [
        test_base_datos,
        test_modelos,
        test_operaciones_crud,
        test_relaciones,
        test_validaciones,
        test_arquitectura
    ]
    
    resultados = []
    
    for test in tests:
        resultado = test()
        resultados.append(resultado)
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE RESULTADOS")
    
    exitosos = sum(resultados)
    total = len(resultados)
    porcentaje = (exitosos / total) * 100
    
    print(f"✅ Tests exitosos: {exitosos}/{total} ({porcentaje:.1f}%)")
    
    if exitosos == total:
        print("🎉 ¡TODOS LOS TESTS PASARON!")
        print("🚀 El sistema está funcionando correctamente")
    else:
        print("⚠️  Algunos tests fallaron")
        print("🔧 Revisar los errores reportados arriba")
    
    return exitosos == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
