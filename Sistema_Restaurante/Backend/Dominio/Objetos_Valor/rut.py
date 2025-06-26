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
            multiplo += 1
            if multiplo > 7:
                multiplo = 2
        resto = suma % 11
        dv_esperado = 11 - resto
        if dv_esperado == 11:
            dv_esperado = '0'
        elif dv_esperado == 10:
            dv_esperado = 'K'
        else:
            dv_esperado = str(dv_esperado)
        return dv == dv_esperado
