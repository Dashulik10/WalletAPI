from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from databases import Database

from dotenv import load_dotenv
import os

load_dotenv()
DATA_BASE_URL = os.getenv("DATABASE_URL")


databases = Database(DATA_BASE_URL)
metadata = MetaData()

engine = create_engine(DATA_BASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()