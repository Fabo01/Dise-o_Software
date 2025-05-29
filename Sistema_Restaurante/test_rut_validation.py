#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from Backend.Dominio.Objetos_Valor.rut import Rut

# Test current RUTs used in failing tests
test_ruts = ['21533873-8', '21533874-6', '21533879-7', '21533876-2', '21533875-4']

print("Testing current RUTs from failing tests:")
for rut in test_ruts:
    print(f'{rut}: {Rut.validar(rut)}')

print("\nTesting some common valid RUTs:")
# Some potentially valid RUTs to test
common_ruts = ['12345678-5', '11111111-1', '87654321-6', '19876543-K', '15678432-1']
for rut in common_ruts:
    print(f'{rut}: {Rut.validar(rut)}')

# Generate some valid RUTs using the algorithm
print("\nGenerating valid RUTs:")
def generar_rut_valido(numero_base):
    """Genera un RUT válido basado en un número base"""
    numero_str = str(numero_base).zfill(8)
    
    # Calcular dígito verificador
    suma = 0
    multiplicador = 2
    
    for i in range(len(numero_str) - 1, -1, -1):
        suma += int(numero_str[i]) * multiplicador
        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2
    
    resto = suma % 11
    dv = 11 - resto
    
    if dv == 11:
        dv_char = '0'
    elif dv == 10:
        dv_char = 'K'
    else:
        dv_char = str(dv)
    
    return f"{numero_base}-{dv_char}"

# Generate some valid RUTs
base_numbers = [12345678, 15678432, 19876543, 21533873, 87654321]
for num in base_numbers:
    rut = generar_rut_valido(num)
    print(f'{rut}: {Rut.validar(rut)}')
