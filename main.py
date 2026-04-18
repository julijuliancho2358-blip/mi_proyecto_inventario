# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel
from typing import List

# ==========================================
# 1. CONFIGURACION DE BASE DE DATOS (SQLite)
# ==========================================
SQLALCHEMY_DATABASE_URL = "sqlite:///./inventario.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==========================================
# 2. MODELOS DE BASE DE DATOS (SQLAlchemy)
# ==========================================
class ProductoDB(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
    cantidad = Column(Integer)

Base.metadata.create_all(bind=engine)

# ==========================================
# 3. ESQUEMAS DE VALIDACION (Pydantic)
# ==========================================
class ProductoBase(BaseModel):
    nombre: str
    precio: float
    cantidad: int

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int
    class Config:
        orm_mode = True

# ==========================================
# 4. CONFIGURACION DE FASTAPI
# ==========================================
app = FastAPI(title="API de Inventario")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# 5. RUTAS CRUD
# ==========================================

# C - CREATE (Crear un producto)
@app.post("/productos/", response_model=ProductoResponse)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    nuevo_producto = ProductoDB(**producto.dict())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

# R - READ (Leer todos los productos)
@app.get("/productos/", response_model=List[ProductoResponse])
def obtener_productos(db: Session = Depends(get_db)):
    productos = db.query(ProductoDB).all()
    return productos

# U - UPDATE (Actualizar un producto)
@app.put("/productos/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, producto_actualizado: ProductoCreate, db: Session = Depends(get_db)):
    producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.nombre = producto_actualizado.nombre
    producto.precio = producto_actualizado.precio
    producto.cantidad = producto_actualizado.cantidad
    db.commit()
    db.refresh(producto)
    return producto

# D - DELETE (Borrar un producto)
@app.delete("/productos/{producto_id}")
def borrar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {"mensaje": "Producto eliminado exitosamente"}