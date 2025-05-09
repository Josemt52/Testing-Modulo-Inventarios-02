# 🧩 Proyecto Full Stack: Backend + Frontend

Este es un proyecto full stack con **Flask** como backend y **React** como frontend. La estructura está diseñada para ser escalable, mantenible y fácil de entender.

---
## 📁 Manual de usuario 
El siguiente proyecto se debera realizar en los siguientes pasos:
- implementar la base de datos que existe dentro del /database/base de datos(conlogin).txt en Mysql 
- crear un ambiente virtual con los requisitos del backend python -m venv env; pip install -r requirements.txt
- entrar al ambiente con .\env\Scripts\activate
- En Testing-Modulo-Inventarios-02/backend/api/database.py cambiar las permisos para la base de datos DATABASE_URL = "mysql+pymysql://root:(tu contraseña)@(donde esta alojado)/inventario_db"
- iniciar el backend uvicorn api.main:app --reload
- iniciar el frontend npm install; npm install react-scripts;npm start
 

## 📁 Estructura del Proyecto

├── /backend/                        # Carpeta del backend

│   ├── /app/                         # Carpeta donde se encuentra la lógica del backend

│   │   ├── __init__.py               # Inicializa el paquete de la app, permite importaciones relativas

│   │   ├── models.py                 # Define los modelos de base de datos, como Producto, Categoría, etc.

│   │   ├── controllers.py            # Gestiona la lógica de las rutas del API (peticiones GET, POST, etc.)

│   │   ├── routes.py                 # Define las rutas o endpoints del API (URL de acceso)

│   │   ├── services.py               # Contiene la lógica de negocio, procesamiento de datos o acciones específicas

│   │   ├── utils.py                  # Funciones y utilidades generales (helpers), como validaciones o transformaciones

│   │   └── config.py                 # Contiene la configuración del backend, como la conexión a la base de datos y configuraciones del servidor

│   ├── /tests/                       # Carpeta para las pruebas del backend

│   │   ├── test_models.py            # Pruebas unitarias para los modelos de base de datos

│   │   ├── test_controllers.py       # Pruebas unitarias para los controladores (endpoints del API)

│   │   └── test_routes.py            # Pruebas unitarias para las rutas del backend

│   ├── app.py                        # Archivo principal para iniciar el servidor de Flask

│   ├── requirements.txt              # Lista las dependencias de Python necesarias para el backend (por ejemplo, Flask, SQLAlchemy, etc.)

├── /frontend/                        # Carpeta del frontend

│   ├── /src/                         # Carpeta con los componentes React

│   │   ├── /components/              # Componentes reutilizables, como Header, Footer, etc.

│   │   ├── /views/                   # Vistas principales de la aplicación (ej. Dashboard, Login, etc.)

│   │   ├── /hooks/                   # Hooks personalizados de React para manejar el estado o lógica del frontend

│   │   ├── /context/                 # Carpeta para manejar el estado global usando React Context

│   │   ├── App.js                    # Componente raíz de la aplicación que contiene la estructura principal

│   │   └── index.js                  # Archivo principal de entrada para la aplicación React

│   ├── /public/                      # Archivos estáticos que se sirven directamente (HTML, imágenes, etc.)

│   │   └── index.html                # Archivo HTML principal donde se carga la aplicación React

│   ├── package.json                  # Configuración de las dependencias de Node.js para el frontend (React, React Router, etc.)

└── README.md                         # Documentación general del proyecto, instrucciones de instalación y uso

