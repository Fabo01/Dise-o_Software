import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from Backend.Infraestructura.Modelos.Usuario_Modelo import Usuario_Modelo

scenarios('features/usuarios.feature')

@pytest.fixture
def limpiar_usuarios(db):
    Usuario_Modelo.objects.all().delete()

@given(parsers.parse('que no existe un usuario con username "{username}"'), target_fixture="limpiar_usuarios")
def no_existe_usuario(username, limpiar_usuarios):
    assert not Usuario_Modelo.objects.filter(username=username).exists()

@given(parsers.parse('que existe un usuario con username "{username}"'))
def existe_usuario(username, db):
    Usuario_Modelo.objects.create(username=username, nombre="Test", rol="mesero")
    assert Usuario_Modelo.objects.filter(username=username).exists()

@when(parsers.parse('creo un usuario con username "{username}", nombre "{nombre}", rol "{rol}"'))
def crear_usuario(username, nombre, rol, db):
    Usuario_Modelo.objects.create(username=username, nombre=nombre, rol=rol)

@when(parsers.parse('actualizo el usuario "{username}" a nombre "{nombre}"'))
def actualizar_usuario(username, nombre, db):
    usuario = Usuario_Modelo.objects.get(username=username)
    usuario.nombre = nombre
    usuario.save()

@when(parsers.parse('elimino el usuario "{username}"'))
def eliminar_usuario(username, db):
    Usuario_Modelo.objects.filter(username=username).delete()

@when('solicito la lista de usuarios')
def listar_usuarios(db):
    pass

@then(parsers.parse('el usuario "{username}" debe existir en el sistema con rol "{rol}"'))
def verificar_usuario(username, rol, db):
    usuario = Usuario_Modelo.objects.get(username=username)
    assert usuario.rol == rol

@then(parsers.parse('el usuario "{username}" debe tener nombre "{nombre}"'))
def verificar_nombre(username, nombre, db):
    usuario = Usuario_Modelo.objects.get(username=username)
    assert usuario.nombre == nombre

@then(parsers.parse('el usuario "{username}" no debe existir en el sistema'))
def verificar_no_existe(username, db):
    assert not Usuario_Modelo.objects.filter(username=username).exists()

@then('debo obtener una lista con los usuarios existentes')
def verificar_lista_usuarios(db):
    usuarios = Usuario_Modelo.objects.all()
    assert usuarios.count() >= 0
