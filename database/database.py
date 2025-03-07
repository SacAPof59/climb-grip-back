from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_DIRECTORY = ".database"  # Name of your database directory
DATABASE_FILE = "data.db"        # Name of your database file

#Construct the full path using the directory and the file name
DATABASE_URL = f"sqlite:///{os.path.join(DATABASE_DIRECTORY, DATABASE_FILE)}"

# Create the database directory if it doesn't exist
os.makedirs(DATABASE_DIRECTORY, exist_ok=True)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Function to get the database session (moved here)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()