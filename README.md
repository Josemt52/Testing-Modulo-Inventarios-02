# Inventory Management Project

Este proyecto es una **aplicación de gestión de inventario** desarrollada con un backend en **Python (Flask + MySQL)** y un frontend en **React**. Permite registrar, actualizar y visualizar categorías, marcas, productos, almacenes y movimientos de inventario.

---

## 📁 Estructura del Proyecto

```
/inventory_management_project
│
├── /backend
│   ├── /app
│   │   ├── /routes            # Rutas de la API (endpoints)
│   │   ├── /models            # Modelos de base de datos
│   │   ├── /database.py       # Configuración de la conexión a MySQL
│   │   ├── /app.py            # Punto de entrada del backend
│   │
│   └── /venv                  # Entorno virtual de Python
│
├── /frontend
│   ├── /public
│   │   └── index.html         # HTML principal
│   │
│   ├── /src
│   │   ├── /components        # Componentes React (categorías, productos, etc.)
│   │   ├── /App.js            # Componente principal
│   │   ├── /index.js          # Punto de entrada de React
│   │
│   └── /node_modules          # Dependencias de Node.js
│
├── /requirements.txt          # Librerías del backend
├── /.gitignore                # Archivos ignorados por git
└── /README.md                 # Guía del proyecto
```

---

## ⚙️ Requisitos

### Backend
- Python 3.10+
- MySQL
- pip
- Virtualenv

### Frontend
- Node.js 16+
- npm o yarn

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/inventory_management_project.git
cd inventory_management_project
```

### 2. Configurar el Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate     # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Editar `database.py` con tus credenciales de conexión a MySQL.

Ejecutar la aplicación:

```bash
cd app
python app.py
```

### 3. Configurar el Frontend

```bash
cd ../../frontend
npm install
npm start
```

---

## 🔗 Endpoints principales

- `GET /categorias`
- `POST /categoria`
- `DELETE /categoria/<id>` → desactiva la categoría (`activo = 0`)
- `GET /productos`
- `POST /producto`
- `DELETE /producto/<id>` → desactiva el producto (`activo = 0`)
- Otros endpoints disponibles para marcas, almacenes y movimientos

---

## 🧪 Base de datos

Incluye tablas como:

- `categorias (id, nombre, activo)`
- `marcas (id, nombre, activo)`
- `productos (id, nombre, categoria_id, marca_id, stock_actual, activo)`
- `movimientos_inventario`
- `almacenes`
- `usuarios`

---

## 👥 Autores

- [Tu Nombre] - Desarrollador Backend & Frontend

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
