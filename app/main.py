from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.routes import client_routes, destinataire_routes, livreur_routes, colis_routes, zone_routes, assignment_routes

# Import all models to ensure they're registered with Base
from app.models import client_expediteur, destinataire, livreur, colis, zone, historique_statut

# Create tables only if not in test environment
import os
if os.getenv("TESTING") != "1":
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="YOULOGIX API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

app.include_router(client_routes.router)
app.include_router(destinataire_routes.router)
app.include_router(livreur_routes.router)
app.include_router(colis_routes.router)
app.include_router(zone_routes.router)
app.include_router(assignment_routes.router)

@app.get("/")
def root():
    return {
        "message": "Bienvenue sur l'API YouLogiX",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc": "/redoc"
    } 

@app.get("/health")
def health_check():
    return {"status": "healthy"}