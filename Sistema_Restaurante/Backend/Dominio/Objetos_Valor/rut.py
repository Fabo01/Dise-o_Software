import re

class Rut:
    @staticmethod
    def validar(rut: str) -> bool:
        """Valida un RUT chileno (formato: XXXXXXXX-Y o XX.XXX.XXX-Y)"""
        rut = rut.replace(".", "").replace("-", "").upper()
        if not rut[:-1].isdigit() or len(rut) < 2:
            return False
        cuerpo = rut[:-1]
        dv = rut[-1]
        suma = 0
        multiplo = 2
        for c in reversed(cuerpo):
            suma += int(c) * multiplo
            multiplo = 9 if multiplo == 2 else multiplo - 1
            multiplo = 2 if multiplo < 2 else multiplo
        resto = suma % 11
        dv_esperado = str(11 - resto) if 11 - resto != 11 else '0'
        if dv == 'K':
            dv = 'k'
        if dv == 'K' or dv == 'k':
            dv_esperado = 'K' if 11 - resto == 10 else dv_esperado
        return dv == str(dv_esperado)
