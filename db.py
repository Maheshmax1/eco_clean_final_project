from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Provide a fallback if DATABASE_URL is not set (prevents crash on Vercel startup)
if not SQLALCHEMY_DATABASE_URL:
    print("WARNING: DATABASE_URL not found in environment variables. Falling back to local SQLite.")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite needs check_same_thread=False; PostgreSQL needs no extra args
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
except Exception as e:
    print(f"FAILED TO CREATE DATABASE ENGINE: {e}")
    # Still create a dummy engine if possible or handle gracefully
    engine = create_engine("sqlite:///./fallback.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
