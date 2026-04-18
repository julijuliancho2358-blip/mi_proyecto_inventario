#  Sistema de Gestión de Inventario

Aplicación web para gestionar un inventario de productos, construida con FastAPI y Streamlit.

##  Tecnologías utilizadas

- **FastAPI** - Framework para construir la API
- **SQLite** - Base de datos local
- **SQLAlchemy** - ORM para manejar la base de datos
- **Pydantic** - Validación de datos
- **Streamlit** - Dashboard visual e interactivo
- **Uvicorn** - Servidor ASGI para correr FastAPI

##  Estructura del proyecto
mi_proyecto_inventario/
│
├── main.py        # Backend: API con FastAPI
├── app.py         # Frontend: Dashboard con Streamlit
├── inventario.db  # Base de datos SQLite (se crea automáticamente)
└── README.md      # Documentación del proyecto

##  Instalación y configuración

### 1. Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd mi_proyecto_inventario
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install fastapi uvicorn sqlalchemy streamlit requests pandas
```

##  Ejecución

La aplicación necesita dos terminales abiertas al mismo tiempo.

### Terminal 1 - Iniciar el Backend
```bash
uvicorn main:app --reload
```
La API estará disponible en: http://localhost:8000

### Terminal 2 - Iniciar el Dashboard
```bash
streamlit run app.py
```
El dashboard estará disponible en: http://localhost:8501

##  Funcionalidades

 Agregar nuevos productos al inventario
 Ver lista completa de productos
 Calcular valor total del inventario
 Eliminar productos
 Documentación automática de la API en http://localhost:8000/docs
 
 julian 