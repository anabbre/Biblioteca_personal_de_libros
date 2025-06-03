from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Ruta del archivo de base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

#Motor de conexión a la base de datos SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#Creador de sesiones para cada endpoint
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base que heredarán los modelos de la base de datos
Base = declarative_base()

#Función de dependencia para obtener una sesión de base de datos. Se importa de los endpoints de main por 'Depends(get_db)
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()