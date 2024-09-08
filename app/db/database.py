from sqlalchemy import Integer, String, Boolean, Column, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'mysql+pymysql://root@localhost/fastapi_crud_db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Model
class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    description = Column(String(255))

class User(Base):
    __tablename__ = 'users'  
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    email = Column(String(255), index=True, unique=True)
    hashed_password = Column(String (255))  
    is_active = Column(Boolean, default=True)
    token = Column(String(500), nullable=True)  


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
