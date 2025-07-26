# Backend/tests/test_bdd_runner.py
"""
BDD Test Runner - Ejecuta las pruebas BDD usando pytest-bdd
"""
import pytest
from pytest_bdd import scenarios

# Importar todos los escenarios de las features
scenarios('features/delivery.feature')
scenarios('features/pagos.feature') 
scenarios('features/analytics.feature')

# Los step definitions se importan automáticamente desde el directorio step_definitions
