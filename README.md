# PetMatch🐾 Back End

### [Enlace al repositorio Front End](https://github.com/Alexus167/PetMatch)

## Guia instalacion

### Instalar Python 

### Crear entorno virtual sobre la carpeta del repositorio (En windows usar simplemente: python -m venv venv)
python3 -m venv venv

### Activar entorno virtual
cd venv/Scripts/activate

### Instalar Django y dependencias
pip install Django==4.2.11 gunicorn==21.2.0 dj-database-url==1.0.0 psycopg2-binary==2.9.9 python-dotenv==1.0.1 whitenoise==6.6.0

### Guardar dependencias en requirements.txt
pip freeze > requirements.txt

### correr con el entorno virtual activado 

python manage.py runserver
