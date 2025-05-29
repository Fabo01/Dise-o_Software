# Tutorial: Ejecución de pruebas BDD en el Sistema de Gestión de Restaurante

Este tutorial explica cómo ejecutar los tests BDD del proyecto utilizando `pytest-bdd`.

## 1. Requisitos previos
- Tener Python 3.8+ instalado.
- Tener el entorno virtual del proyecto activado.
- Instalar dependencias:

```bash
pip install -r requirements.txt
```

## 2. Estructura de pruebas
Las pruebas BDD se encuentran en:
- `Backend/tests/features/` → Archivos `.feature` (escenarios)
- `Backend/tests/` → Archivos `test_*.py` (step definitions)

## 3. Ejecución de los tests
Desde la raíz del proyecto, ejecuta:

```bash
pytest Backend/tests/
```

Esto ejecutará todos los escenarios BDD definidos.

## 4. Ejemplo de salida
```
============================= test session starts =============================
collected 12 items

Backend/tests/test_ingredientes.py ....
Backend/tests/test_usuarios.py ....
...
========================== 12 passed in 2.34s ================================
```

## 5. Consejos y buenas prácticas
- Escribe los escenarios en español y claros para todos los roles.
- Cada nueva funcionalidad debe tener su escenario y steps BDD.
- Si un test falla, revisa el step definition y la lógica de negocio.

---

**¡Listo! Ahora puedes validar el comportamiento del sistema de forma colaborativa y automatizada.**
