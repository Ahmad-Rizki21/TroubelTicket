# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Importing all the application routers
from .routers import tickets, users, auth, ticket_actions, roles, permissions, remotes, reports, dashboard


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
app.include_router(remotes.router)
app.include_router(reports.router)
app.include_router(dashboard.router)

@app.on_event("startup")
async def startup_event():
    print("-------------------------------------------------------------------")
    print("  Ticket System built by Artacom")
    print("  Developed by Ahmad (Instagram: @amad.dyk)")
    print("-------------------------------------------------------------------")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Selamat datang di API Sistem Tiket!"}