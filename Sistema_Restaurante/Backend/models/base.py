from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from datetime import datetime
import json

# Configuración de la base de datos
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///restaurant.db")

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Crear una fábrica de sesiones
session_factory = sessionmaker(bind=engine)

# Crear una sesión de ámbito que manejará las transacciones
db_session = scoped_session(session_factory)

# Crear la clase base para los modelos
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """Inicializa la base de datos creando todas las tablas definidas"""
    # Importar aquí todos los modelos para asegurarse que estén registrados
    import models.all_models
    
    # Crear las tablas
    Base.metadata.create_all(bind=engine)

def to_dict(model_instance, exclude=None):
    """
    Convierte una instancia de modelo a un diccionario
    
    Args:
        model_instance: Instancia del modelo a convertir
        exclude: Lista de campos a excluir
        
    Returns:
        Diccionario con los datos del modelo
    """
    if exclude is None:
        exclude = []
        
    result = {}
    for column in model_instance.__table__.columns:
        if column.name not in exclude:
            value = getattr(model_instance, column.name)
            
            # Convertir datetime a string
            if isinstance(value, datetime):
                value = value.isoformat()
                
            # Convertir JSON si es necesario
            if isinstance(value, str) and (value.startswith('{') or value.startswith('[')):
                try:
                    value = json.loads(value)
                except:
                    pass
                
            result[column.name] = value
            
    return result
