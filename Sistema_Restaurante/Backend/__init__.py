import os
import django

# Set up Django environment when used standalone
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.Config.settings')
    django.setup()

# Este archivo permite que Python trate el directorio como un paquete