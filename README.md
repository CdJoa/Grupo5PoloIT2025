# PetMatch🐾 Back End

### [Enlace al repositorio Front End](https://github.com/Alexus167/PetMatch)

## Guia instalacion

### Instalar Python 

### Crear entorno virtual sobre la carpeta del repositorio (En windows usar simplemente: python -m venv venv)
python3 -m venv venv

### Activar entorno virtual
cd venv/Scripts/activate  (source venv/bin/activate   en linux)

### Guardar dependencias en requirements.txt
pip install -r requirements.txt

### correr con el entorno virtual activado 

python manage.py runserver
(python3  manage.py runserver)

### mail de la pagina
matchpettest@gmail.com


### Notas Testing
no hay... falta alguna especie de validación para solicitar mascotas y chats cuando tienen el perfil incompleto

tambien sale error 404 cuando una sesion expiro pero como estas inactivo te desconecto y seguis viendo tu sesion hasta q interactuas con algun boton