# On-Demand
Proyecto personal de servicios.

# Instalar todas las dependencias del proyecto
pip install -r requirements.txt

# Activar entorno virtual - cmd
.venv\Scripts\activate

# Inicializar la app -entorno virtual
uvicorn microservice_servicerequest.main:app --reload



# git Command...
# Subir al Repositorio:

  # saber branch
git branch
  # saber status
git status


git init
git remote add origin https://github.com/Nico-jimenez16/On-Demand-MicroserviceRequest.git
git add .
git commit -m "Conexion con la base de datos"
git branch -M main 
git push -u origin main

# Crear otra Rama:
git checkout -b dev
git push -u origin dev

# Agregar cosas nuevas:
git add .
git commit -m "Agregando SRS y .gitignore al gateway"
git push origin dev
git push origin main

# Cambiar de Rama:
git checkout main
git checkout dev



