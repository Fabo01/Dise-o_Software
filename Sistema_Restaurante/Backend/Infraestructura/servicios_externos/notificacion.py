def enviar_notificacion(usuario_id: int, mensaje: str) -> None:
    """
    Envía una notificación simple a un usuario.
    Args:
        usuario_id (int): ID del usuario destinatario.
        mensaje (str): Mensaje de la notificación.
    """
    print(f"Notificación enviada a usuario {usuario_id}: {mensaje}")

if __name__ == "__main__":
    # Prueba de funcionamiento
    enviar_notificacion(1, "¡Bienvenido al sistema!")