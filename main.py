#main.py
from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from unidecode import unidecode
from typing import List
#Importaciones desde database.py
from database import Base, engine, get_db
#Importaciones desde models.py 
from models import Book, BookCreate, BookUpdateStatus, DBBook

#Tablas para crear la base de datos si no existen
Base.metadata.create_all(bind=engine)

#Instancia de la aplicación
app = FastAPI(
    title="Biblioteca personal de lectura",
    description="API para registrar, consultar y actualizar el estado de lectura de los libros de nuestra colección personal.",
    version="1.0.0"
)

#----ENDPOINTS----

#POST para añadir libros 
@app.post("/books/", response_model=Book, status_code=status.HTTP_201_CREATED)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    print(f"📘 Título recibido: {book.title}")
    normalized_title = unidecode(book.title).lower() #Normaliza el título para evitar problemas con tildes o caracteres especiales 

    #Busca si ya existe
    existing_books = db.query(DBBook).all()
    for b in existing_books: #Itera sobre los libros ya existentes en la base de datos 
        if unidecode(b.title).lower() == normalized_title:
            raise HTTPException( #Si se encuentra un duplicado, lanza una excepción 409
                status_code=status.HTTP_409_CONFLICT,
                detail="El libro ya existe"
            )
    #Si no existe el libro en la BBDD, creamos el nuevo
    book_data = book.model_dump()  #Convierte el objeto Pydantic BookCreate a un diccionario
    if book_data.get("cover_url") is not None: 
        book_data["cover_url"] = str(book_data["cover_url"])  #Lo convierte a string si hay valor

    #Crea una instancia del modelo DBBook usando los datos del diccionario 'book_data'
    db_book = DBBook(**book_data) # Ahora cover_url será un string
    db.add(db_book) #Agrega el nuevo libro
    db.commit() #Guarda cambios
    db.refresh(db_book) #Actualiza 'db_book' con los datos mas recientes
    return db_book #Devuelve el nuevo libro


#GET para obtener todos los libros 
@app.get("/books/", response_model=List[Book])
def get_books(db: Session = Depends(get_db)):
    return db.query(DBBook).all() #Devuelve todos los libros de la BBDD

#GET para buscar un libro por su título
@app.get("/books/{title}", response_model=Book)
def get_book_by_title(title: str, db: Session = Depends(get_db)):
    normalized_title = unidecode(title).lower()
    books = db.query(DBBook).all()
    for book in books: #Itera pra encontrar la coincidencia en el título
        if unidecode(book.title).lower() == normalized_title:
            return book
    #Si el bucle termina sin encontrar el libro, lanza el 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Libro no encontrado"
    )

#PUT para actualizar si ha sido leido el libro
@app.put("/books/{title}", response_model=Book)
def update_read_status(title: str, update_data: BookUpdateStatus, db: Session = Depends(get_db)):
    normalized_title = unidecode(title).lower()
    books = db.query(DBBook).all()
    for book in books:
        if unidecode(book.title).lower() == normalized_title:
            book.is_read = update_data.is_read #Actualiza al estado 'is read' 
            db.commit()
            db.refresh(book)
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Libro no encontrado"
    )
    

#DELETE para eliminar un libro por su título
@app.delete("/books/{title}", response_model=Book)
def delete_book(title: str, db: Session = Depends(get_db)):
    normalized_title = unidecode(title).lower()
    books = db.query(DBBook).all()
    for book in books:
        if unidecode(book.title).lower() == normalized_title: 
            db.delete(book) #Elimina el libro de la BBDD
            db.commit()
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Libro no encontrado"
    )