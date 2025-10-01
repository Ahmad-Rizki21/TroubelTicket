# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import tickets, users, auth, ticket_actions, roles, permissions


app = FastAPI(title="Sistem Tiket API")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Daftarkan setiap router ke aplikasi utama
app.include_router(tickets.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(ticket_actions.router)
app.include_router(roles.router)
app.include_router(permissions.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Selamat datang di API Sistem Tiket!"}