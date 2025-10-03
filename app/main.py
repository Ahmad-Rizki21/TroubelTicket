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

# Daftarkan setiap router ke aplikasi utama dengan prefix /api untuk production
app.include_router(tickets.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(ticket_actions.router, prefix="/api")
app.include_router(roles.router, prefix="/api")
app.include_router(permissions.router, prefix="/api")
app.include_router(remotes.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    print("-------------------------------------------------------------------")
    print("  Ticket System built by Artacom")
    print("  Developed by Ahmad (Instagram: @amad.dyk)")
    print("-------------------------------------------------------------------")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Selamat datang di API Sistem Tiket!"}