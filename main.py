from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import db
import routes

app = FastAPI(
    title="Task Manager API",
    description="Manage your tasks easily with this FastAPI app.",
    version="1.0"
)

# CORS so you can play with the API anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    db.create_db_and_tables()


# Attach routes from routes.py
app.include_router(routes.router)


@app.get("/", tags=["Info"])
def home():
    """Just tells you what's here."""
    return {
        "msg": "Welcome to the Task Manager API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Info"])
def health():
    return {"ok": True}
