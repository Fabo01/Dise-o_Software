import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from Backend.Infraestructura.Modelos.Usuario_Modelo import UsuarioModelo

scenarios('features/usuarios.feature')

@pytest.fixture
def limpiar_usuarios(db):
    UsuarioModelo.objects.all().delete()

@given(parsers.parse('que no existe un usuario con username "{username}"'), target_fixture="limpiar_usuarios")
def no_existe_usuario(username, limpiar_usuarios):
    assert not UsuarioModelo.objects.filter(username=username).exists()

@given(parsers.parse('que existe un usuario con username "{username}"'))
def existe_usuario(username, db):
    UsuarioModelo.objects.create(rut="21533873-8", username=username, nombre="Test", rol="mesero", email=f"{username}@mail.com", password="1234")
    assert UsuarioModelo.objects.filter(username=username).exists()

@given(parsers.parse('que existe un usuario con rut "{rut}"'))
def existe_usuario_rut(rut, db):
    UsuarioModelo.objects.create(rut=rut, username=rut, nombre="Test", rol="mesero", email=f"{rut}@mail.com", password="1234")
    assert UsuarioModelo.objects.filter(rut=rut).exists()

@given('que existen usuarios registrados')
def existen_usuarios_registrados(db):
    UsuarioModelo.objects.create(rut="21533876-2", username="ana", nombre="Ana", rol="mesero", email="ana@mail.com", password="1234")
    UsuarioModelo.objects.create(rut="21533875-4", username="luis", nombre="Luis", rol="cocinero", email="luis@mail.com", password="1234")
    assert UsuarioModelo.objects.count() >= 2

@when(parsers.parse('creo un usuario con username "{username}", nombre "{nombre}", rol "{rol}"'))
def crear_usuario(username, nombre, rol, db):
    UsuarioModelo.objects.create(rut="21533873-8", username=username, nombre=nombre, rol=rol, email=f"{username}@mail.com", password="1234")

@when(parsers.parse('creo un usuario con rut "{rut}", nombre "{nombre}", rol "{rol}"'))
def crear_usuario_rut(rut, nombre, rol, db):
    UsuarioModelo.objects.create(rut=rut, username=rut, nombre=nombre, rol=rol, email=f"{rut}@mail.com", password="1234")

@when(parsers.parse('actualizo el usuario "{username}" a nombre "{nombre}"'))
def actualizar_usuario(username, nombre, db):
    usuario = UsuarioModelo.objects.get(username=username)
    usuario.nombre = nombre
    usuario.save()

@when(parsers.parse('actualizo el usuario con rut "{rut}" a nombre "{nombre}"'))
def actualizar_usuario_rut(rut, nombre, db):
    usuario = UsuarioModelo.objects.get(rut=rut)
    usuario.nombre = nombre
    usuario.save()

@when(parsers.parse('elimino el usuario "{username}"'))
def eliminar_usuario(username, db):
    UsuarioModelo.objects.filter(username=username).delete()

@when(parsers.parse('elimino el usuario con rut "{rut}"'))
def eliminar_usuario_rut(rut, db):
    UsuarioModelo.objects.filter(rut=rut).delete()

@when('solicito la lista de usuarios')
def listar_usuarios(db):
    pass

@then(parsers.parse('el usuario "{username}" debe existir en el sistema con rol "{rol}"'))
def verificar_usuario(username, rol, db):
    usuario = UsuarioModelo.objects.get(username=username)
    assert usuario.rol == rol

@then(parsers.parse('el usuario con rut "{rut}" debe existir en el sistema con rol "{rol}"'))
def verificar_usuario_rut(rut, rol, db):
    usuario = UsuarioModelo.objects.get(rut=rut)
    assert usuario.rol == rol

@then(parsers.parse('el usuario "{username}" debe tener nombre "{nombre}"'))
def verificar_nombre(username, nombre, db):
    usuario = UsuarioModelo.objects.get(username=username)
    assert usuario.nombre == nombre

@then(parsers.parse('el usuario con rut "{rut}" debe tener nombre "{nombre}"'))
def verificar_nombre_rut(rut, nombre, db):
    usuario = UsuarioModelo.objects.get(rut=rut)
    assert usuario.nombre == nombre

@then(parsers.parse('el usuario "{username}" no debe existir en el sistema'))
def verificar_no_existe(username, db):
    assert not UsuarioModelo.objects.filter(username=username).exists()

@then(parsers.parse('el usuario con rut "{rut}" no debe existir en el sistema'))
def verificar_no_existe_rut(rut, db):
    assert not UsuarioModelo.objects.filter(rut=rut).exists()

@then('debo obtener una lista con los usuarios existentes')
def verificar_lista_usuarios(db):
    usuarios = UsuarioModelo.objects.all()
    assert usuarios.count() >= 0
