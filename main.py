from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from db import engine, Base
from routers import auth, events, users, contact, admin
import os

app = FastAPI(title="EcoClean API", version="1.0.0")

# Create tables on startup (wrapped in try/except for Vercel stability)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database table creation skipped or failed: {e}")

# CORS = Allow your frontend to talk to your backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(events.router)
app.include_router(users.router)
app.include_router(contact.router)
app.include_router(admin.router)



try:
    if not os.path.exists("uploads"):
        os.makedirs("uploads", exist_ok=True)
    app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
except Exception as e:
    print(f"Skipping local uploads mount: {e}")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to EcoClean API"}
