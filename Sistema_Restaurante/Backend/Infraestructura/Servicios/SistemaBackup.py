# Backend/Infraestructura/Servicios/SistemaBackup.py
# S3-31, S3-32, S3-33: Sistema de respaldo y recuperación
import os
import json
import shutil
import zipfile
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.serializers import serialize, deserialize
from django.apps import apps
import logging

logger = logging.getLogger(__name__)


class SistemaBackup:
    """Sistema completo de respaldo y recuperación de datos"""
    
    def __init__(self):
        self.backup_dir = getattr(settings, 'BACKUP_DIR', os.path.join(settings.BASE_DIR, 'backups'))
        self.max_backups = getattr(settings, 'MAX_BACKUPS', 30)  # Mantener 30 días de backups
        self._ensure_backup_directory()
    
    def _ensure_backup_directory(self):
        """Asegurar que el directorio de backups existe"""
        os.makedirs(self.backup_dir, exist_ok=True)
        logger.info(f"Directorio de backup configurado: {self.backup_dir}")
    
    def crear_backup_completo(self) -> Dict[str, Any]:
        """
        Crear un backup completo del sistema
        S3-31: Implementar sistema de respaldo completo
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_completo_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        try:
            os.makedirs(backup_path, exist_ok=True)
            
            # 1. Backup de base de datos
            db_backup_path = self._backup_database(backup_path)
            
            # 2. Backup de archivos de configuración
            config_backup_path = self._backup_configuration(backup_path)
            
            # 3. Backup de archivos estáticos y media
            media_backup_path = self._backup_media_files(backup_path)
            
            # 4. Crear manifiesto del backup
            manifest = self._crear_manifiesto_backup(
                backup_name, 
                db_backup_path, 
                config_backup_path, 
                media_backup_path
            )
            
            # 5. Comprimir backup
            zip_path = self._comprimir_backup(backup_path, backup_name)
            
            # 6. Limpiar backups antiguos
            self._limpiar_backups_antiguos()
            
            logger.info(f"Backup completo creado exitosamente: {zip_path}")
            
            return {
                'success': True,
                'backup_name': backup_name,
                'backup_path': zip_path,
                'timestamp': timestamp,
                'manifest': manifest
            }
            
        except Exception as e:
            logger.error(f"Error creando backup completo: {str(e)}")
            # Limpiar archivos parciales en caso de error
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
            
            return {
                'success': False,
                'error': str(e),
                'timestamp': timestamp
            }
    
    def _backup_database(self, backup_path: str) -> str:
        """Crear backup de la base de datos"""
        db_backup_path = os.path.join(backup_path, 'database')
        os.makedirs(db_backup_path, exist_ok=True)
        
        # Backup usando dumpdata de Django
        fixture_path = os.path.join(db_backup_path, 'full_data.json')
        
        with open(fixture_path, 'w', encoding='utf-8') as f:
            call_command('dumpdata', 
                        '--natural-foreign', 
                        '--natural-primary',
                        '--exclude=contenttypes',
                        '--exclude=auth.permission',
                        '--exclude=sessions',
                        stdout=f)
        
        # Backup de esquema (migraciones aplicadas)
        migrations_path = os.path.join(db_backup_path, 'migrations.json')
        migration_info = self._obtener_info_migraciones()
        
        with open(migrations_path, 'w', encoding='utf-8') as f:
            json.dump(migration_info, f, indent=2, default=str)
        
        logger.info(f"Backup de base de datos creado: {db_backup_path}")
        return db_backup_path
    
    def _backup_configuration(self, backup_path: str) -> str:
        """Backup de archivos de configuración"""
        config_backup_path = os.path.join(backup_path, 'configuration')
        os.makedirs(config_backup_path, exist_ok=True)
        
        # Backup de settings
        settings_info = {
            'DEBUG': getattr(settings, 'DEBUG', False),
            'ALLOWED_HOSTS': getattr(settings, 'ALLOWED_HOSTS', []),
            'INSTALLED_APPS': getattr(settings, 'INSTALLED_APPS', []),
            'DATABASE_ENGINE': settings.DATABASES['default']['ENGINE'],
            'STATIC_URL': getattr(settings, 'STATIC_URL', '/static/'),
            'MEDIA_URL': getattr(settings, 'MEDIA_URL', '/media/'),
        }
        
        settings_path = os.path.join(config_backup_path, 'settings_backup.json')
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings_info, f, indent=2)
        
        # Backup de requirements.txt si existe
        req_file = os.path.join(settings.BASE_DIR, 'requirements.txt')
        if os.path.exists(req_file):
            shutil.copy2(req_file, config_backup_path)
        
        logger.info(f"Backup de configuración creado: {config_backup_path}")
        return config_backup_path
    
    def _backup_media_files(self, backup_path: str) -> str:
        """Backup de archivos media"""
        media_backup_path = os.path.join(backup_path, 'media')
        
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        if media_root and os.path.exists(media_root):
            shutil.copytree(media_root, media_backup_path)
            logger.info(f"Backup de archivos media creado: {media_backup_path}")
        else:
            # Crear directorio vacío si no hay archivos media
            os.makedirs(media_backup_path, exist_ok=True)
            logger.info("No se encontraron archivos media para respaldar")
        
        return media_backup_path
    
    def _obtener_info_migraciones(self) -> Dict[str, List[str]]:
        """Obtener información de migraciones aplicadas"""
        from django.db.migrations.executor import MigrationExecutor
        from django.db import connections
        
        connection = connections['default']
        executor = MigrationExecutor(connection)
        
        migration_info = {}
        for app_name in apps.get_app_configs():
            applied_migrations = []
            for migration in executor.loader.applied_migrations:
                if migration[0] == app_name.label:
                    applied_migrations.append(migration[1])
            
            if applied_migrations:
                migration_info[app_name.label] = sorted(applied_migrations)
        
        return migration_info
    
    def _crear_manifiesto_backup(self, backup_name: str, db_path: str, 
                                config_path: str, media_path: str) -> Dict[str, Any]:
        """Crear manifiesto del backup"""
        manifest = {
            'backup_name': backup_name,
            'created_at': datetime.now().isoformat(),
            'django_version': getattr(settings, 'DJANGO_VERSION', 'unknown'),
            'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}",
            'components': {
                'database': os.path.basename(db_path),
                'configuration': os.path.basename(config_path),
                'media': os.path.basename(media_path)
            },
            'file_counts': {
                'database_files': len(os.listdir(db_path)) if os.path.exists(db_path) else 0,
                'config_files': len(os.listdir(config_path)) if os.path.exists(config_path) else 0,
                'media_files': self._contar_archivos_recursivo(media_path) if os.path.exists(media_path) else 0
            }
        }
        
        return manifest
    
    def _contar_archivos_recursivo(self, directorio: str) -> int:
        """Contar archivos recursivamente en un directorio"""
        count = 0
        for root, dirs, files in os.walk(directorio):
            count += len(files)
        return count
    
    def _comprimir_backup(self, backup_path: str, backup_name: str) -> str:
        """Comprimir el backup en un archivo ZIP"""
        zip_path = f"{backup_path}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, backup_path)
                    zipf.write(file_path, arc_name)
        
        # Limpiar directorio temporal
        shutil.rmtree(backup_path)
        
        return zip_path
    
    def _limpiar_backups_antiguos(self):
        """Limpiar backups antiguos según política de retención"""
        backups = []
        for file in os.listdir(self.backup_dir):
            if file.startswith('backup_completo_') and file.endswith('.zip'):
                file_path = os.path.join(self.backup_dir, file)
                stat = os.stat(file_path)
                backups.append((file_path, stat.st_mtime))
        
        # Ordenar por fecha (más reciente primero)
        backups.sort(key=lambda x: x[1], reverse=True)
        
        # Eliminar backups que excedan el límite
        if len(backups) > self.max_backups:
            for backup_path, _ in backups[self.max_backups:]:
                try:
                    os.remove(backup_path)
                    logger.info(f"Backup antiguo eliminado: {backup_path}")
                except Exception as e:
                    logger.error(f"Error eliminando backup antiguo {backup_path}: {str(e)}")
    
    def restaurar_backup(self, backup_path: str) -> Dict[str, Any]:
        """
        Restaurar sistema desde un backup
        S3-32: Implementar sistema de recuperación
        """
        try:
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f"Archivo de backup no encontrado: {backup_path}")
            
            # Crear directorio temporal para extracción
            temp_dir = os.path.join(self.backup_dir, f"restore_temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Extraer backup
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Leer manifiesto
            manifest_path = os.path.join(temp_dir, 'manifest.json')
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
            else:
                manifest = {}
            
            # Restaurar componentes
            restore_results = {}
            
            # 1. Restaurar base de datos
            db_path = os.path.join(temp_dir, 'database')
            if os.path.exists(db_path):
                restore_results['database'] = self._restaurar_database(db_path)
            
            # 2. Restaurar archivos media
            media_path = os.path.join(temp_dir, 'media')
            if os.path.exists(media_path):
                restore_results['media'] = self._restaurar_media_files(media_path)
            
            # Limpiar directorio temporal
            shutil.rmtree(temp_dir)
            
            logger.info(f"Backup restaurado exitosamente desde: {backup_path}")
            
            return {
                'success': True,
                'backup_path': backup_path,
                'manifest': manifest,
                'restore_results': restore_results,
                'restored_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error restaurando backup: {str(e)}")
            
            # Limpiar en caso de error
            if 'temp_dir' in locals() and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            
            return {
                'success': False,
                'error': str(e),
                'backup_path': backup_path
            }
    
    def _restaurar_database(self, db_path: str) -> Dict[str, Any]:
        """Restaurar base de datos desde backup"""
        try:
            fixture_path = os.path.join(db_path, 'full_data.json')
            
            if not os.path.exists(fixture_path):
                raise FileNotFoundError(f"Archivo de datos no encontrado: {fixture_path}")
            
            # Limpiar base de datos actual (PELIGROSO - solo en restauración)
            with transaction.atomic():
                # Cargar datos desde fixture
                call_command('loaddata', fixture_path)
            
            return {
                'success': True,
                'fixture_path': fixture_path,
                'message': 'Base de datos restaurada exitosamente'
            }
            
        except Exception as e:
            logger.error(f"Error restaurando base de datos: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _restaurar_media_files(self, media_backup_path: str) -> Dict[str, Any]:
        """Restaurar archivos media desde backup"""
        try:
            media_root = getattr(settings, 'MEDIA_ROOT', None)
            
            if not media_root:
                return {
                    'success': False,
                    'error': 'MEDIA_ROOT no configurado'
                }
            
            # Backup de archivos actuales antes de restaurar
            if os.path.exists(media_root):
                backup_current = f"{media_root}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.move(media_root, backup_current)
                logger.info(f"Archivos media actuales respaldados en: {backup_current}")
            
            # Restaurar archivos desde backup
            shutil.copytree(media_backup_path, media_root)
            
            return {
                'success': True,
                'media_root': media_root,
                'message': 'Archivos media restaurados exitosamente'
            }
            
        except Exception as e:
            logger.error(f"Error restaurando archivos media: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def listar_backups(self) -> List[Dict[str, Any]]:
        """
        Listar backups disponibles
        S3-33: Sistema de gestión de backups
        """
        backups = []
        
        for file in os.listdir(self.backup_dir):
            if file.startswith('backup_completo_') and file.endswith('.zip'):
                file_path = os.path.join(self.backup_dir, file)
                stat = os.stat(file_path)
                
                backup_info = {
                    'name': file,
                    'path': file_path,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'created_at': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'age_days': (datetime.now() - datetime.fromtimestamp(stat.st_mtime)).days
                }
                
                backups.append(backup_info)
        
        # Ordenar por fecha de creación (más reciente primero)
        backups.sort(key=lambda x: x['created_at'], reverse=True)
        
        return backups
    
    def validar_backup(self, backup_path: str) -> Dict[str, Any]:
        """Validar integridad de un backup"""
        try:
            if not os.path.exists(backup_path):
                return {
                    'valid': False,
                    'error': 'Archivo de backup no encontrado'
                }
            
            # Verificar que es un ZIP válido
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                # Verificar integridad del ZIP
                corrupted_files = zipf.testzip()
                if corrupted_files:
                    return {
                        'valid': False,
                        'error': f'Archivos corruptos encontrados: {corrupted_files}'
                    }
                
                # Verificar estructura esperada
                file_list = zipf.namelist()
                required_components = ['database/', 'configuration/', 'media/']
                
                missing_components = []
                for component in required_components:
                    if not any(file.startswith(component) for file in file_list):
                        missing_components.append(component)
                
                if missing_components:
                    return {
                        'valid': False,
                        'error': f'Componentes faltantes: {missing_components}'
                    }
            
            return {
                'valid': True,
                'message': 'Backup válido',
                'components_found': len([f for f in file_list if '/' in f])
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Error validando backup: {str(e)}'
            }


class ComandoBackup(BaseCommand):
    """Comando de Django para gestión de backups desde línea de comandos"""
    
    help = 'Gestión de backups del sistema'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            choices=['crear', 'restaurar', 'listar', 'validar'],
            help='Acción a realizar'
        )
        parser.add_argument(
            '--backup-path',
            type=str,
            help='Ruta del backup para restaurar o validar'
        )
    
    def handle(self, *args, **options):
        sistema_backup = SistemaBackup()
        action = options['action']
        
        if action == 'crear':
            self.stdout.write('Creando backup completo...')
            result = sistema_backup.crear_backup_completo()
            
            if result['success']:
                self.stdout.write(
                    self.style.SUCCESS(f'Backup creado exitosamente: {result["backup_path"]}')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'Error creando backup: {result["error"]}')
                )
        
        elif action == 'restaurar':
            backup_path = options.get('backup_path')
            if not backup_path:
                self.stdout.write(self.style.ERROR('Se requiere --backup-path para restaurar'))
                return
            
            self.stdout.write(f'Restaurando backup desde: {backup_path}')
            result = sistema_backup.restaurar_backup(backup_path)
            
            if result['success']:
                self.stdout.write(self.style.SUCCESS('Backup restaurado exitosamente'))
            else:
                self.stdout.write(self.style.ERROR(f'Error restaurando: {result["error"]}'))
        
        elif action == 'listar':
            backups = sistema_backup.listar_backups()
            
            if not backups:
                self.stdout.write('No se encontraron backups')
                return
            
            self.stdout.write('Backups disponibles:')
            for backup in backups:
                self.stdout.write(
                    f"  - {backup['name']} ({backup['size_mb']}MB, {backup['age_days']} días)"
                )
        
        elif action == 'validar':
            backup_path = options.get('backup_path')
            if not backup_path:
                self.stdout.write(self.style.ERROR('Se requiere --backup-path para validar'))
                return
            
            result = sistema_backup.validar_backup(backup_path)
            
            if result['valid']:
                self.stdout.write(self.style.SUCCESS(f'Backup válido: {result["message"]}'))
            else:
                self.stdout.write(self.style.ERROR(f'Backup inválido: {result["error"]}'))
