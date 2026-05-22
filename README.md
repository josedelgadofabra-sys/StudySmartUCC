# Instrucciones de instalación

A continuación se presentarán los siguentes pasos para configurar y ejecutar el proyecto localmente.


## 1. Clonar el repositorio

Descarga el proyecto desde GitHub:

```bash
git clone <URL_DEL_REPOSITORIO>
cd StudySmart_UCC
```

## 2. Crear y activar entorno virtual

Se recomienda usar un entorno virtual para aislar las dependencias del proyecto.

### Comaqndos para crear entorno virtual

```bash
python -m venv venv
```

Esto generará una carpeta llamada `venv/` que contendrá todas las librerías necesarias.

### Activación entorno virtual

### En Windows

```bash
venv\Scripts\activate
```

### En Linux o macOS

```bash
source venv/bin/activate
```

Si se activó correctamente, aparecerá algo como esto en la terminal:

```bash
(venv)
```

## 3. Instalar dependencias del proyecto

Instalar todas las librerías necesarias usando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 4. Configurar conexión a base de datos

El proyecto está configurado para trabajar con **SQLite3**, que es la base de datos predeterminada de Django y no requiere instalación adicional.

La conexión se encuentra definida en el archivo:

```bash
proyecto_UCC/settings.py
```

Configuración actual:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Crear base de datos y tablas

Ejecutar las migraciones para generar automáticamente la base de datos:

```bash
cd proyecto_UCC
python manage.py makemigrations
python manage.py migrate
```

Esto creará el archivo:

```bash
db.sqlite3
```

y todas las tablas necesarias para el funcionamiento del sistema.


## 5. Configurar variables de entorno (.env)

Para proteger información sensible como la **SECRET_KEY**, se recomienda usar un archivo `.env`.

### Instalar soporte para variables de entorno

```bash
pip install python-decouple
```

### Crear archivo `.env`

En la raíz del proyecto crear un archivo llamado:

```bash
.env
```

Contenido:

```env
SECRET_KEY= clave_elegida
DEBUG=True
```

### Modificar `settings.py`

Agregar al inicio:

```python
from decouple import config
```

Y reemplazar:

```python
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

## 6. Ejecutar servidor local

Iniciar la aplicación:

```bash
python manage.py runserver
```

Abrir en el navegador:

```bash
http://127.0.0.1:8000/
```

Si todos los pasos anteriores están correctamente ejecutados, el sistema Study Smart UCC estará funcionando localmente y puede ser ejecutado desde el navegador o en su defecto dando Cntrl + Click en "http://127.0.0.1:8000/".

## 7. Resumen de guia de conexion en localhost

1. Descomprimir el proyecto
cd StudySmart_UCC/proyecto_UCC

2. Crear entorno virtual
python -m venv venv

 3. Activar entorno virtual en Windows
venv\Scripts\activate

4. Instalar dependencias
pip install -r ../requirements.txt

5. Ejecutar migraciones
python manage.py migrate

6. Cargar fixtures de materias si aplica
python manage.py loaddata crud_app/fixtures/materias_fixture.json
python manage.py loaddata crud_app/fixtures/derecho_fixture.json
python manage.py loaddata crud_app/fixtures/nuevas_carreras_fixture.json

7. Ejecutar servidor
python manage.py runserver

# Grupo 7:

El proyecto Study Smart UCC presentado para la asignatura de herramientas computacionales para interpretación y validación de resultados fué desarrollado por los estudiantes:

Jose Alfonso Delgado Fabra.
Andrés Felipe Durango.
Jesús Manuel Oquendo Padilla.
Jesús Manuel Espitia Cogollo.


Departamento de Ing. de Sistemas.
Universidad Cooperativa de Colombia.
V Semestre - 20 de abril de 2026.
