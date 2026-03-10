from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from db import engine, Base
from routers import auth, events, users, contact, admin
import os

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="EcoClean API", version="1.0.0")

# CORS = Allow your frontend to talk to your backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(users.router)
app.include_router(contact.router)
app.include_router(admin.router)

# ─── Static file uploads ───
if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ─── Health check ───
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to EcoClean API"}
