Manual de Usuario
Backend

Para iniciar el servidor backend con FastAPI, sigue estos pasos:

    Activar tu entorno virtual (asumiendo que ya tienes uno creado):

# Windows
.\env\Scripts\activate

# Linux / MacOS
source env/bin/activate

    Instalar las dependencias necesarias:

pip install fastapi uvicorn sqlalchemy pymysql passlib[bcrypt]
pip install pydantic[email]
pip install cryptography

    Iniciar el servidor con Uvicorn:

uvicorn api.main:app --reload

    El parámetro --reload permite que el servidor se reinicie automáticamente cuando detecta cambios en el código.

Frontend

Para ejecutar la aplicación frontend hecha con React:

    Abre una terminal en la carpeta del frontend.

    Ejecuta la instalación de dependencias:

npm install

    Inicia la aplicación React:

npm start

    Si aún no tienes instalado react-router-dom (para manejo de rutas), instálalo con:

npm install react-router-dom
