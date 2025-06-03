from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Boolean
from database import Base 

# ---------- MODELOS Pydantic ----------

#Modelo base con los campos comunes para crear y mostrar los libros
class BookBase(BaseModel):
    title: str
    author: str
    year: int
    cover_url: Optional[HttpUrl] = None  #Es opcional y se valida como URL
    is_read: bool 

#Modelo para la creación de un libro, heredando de BookBase
class BookCreate(BookBase):
    pass

#Modelo para la respuesta de la API cuando se muestra un libro
class Book(BookBase):
    id: int #El ID es generado por la base de datos
    class Config:
        from_attributes = True  # Convierte modelo SQLAlchemy a dict automáticamente

#Modelo para actualizar el estado de lectura de un libro
class BookUpdateStatus(BaseModel): 
    is_read: bool


#Modelo SQLAlchemy para definir la estructura de la tabla en la BBDD
class DBBook(Base): #Hereda de la 'base' importada de database.py
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    cover_url = Column(String, nullable=True)
    is_read = Column(Boolean, default=False)
