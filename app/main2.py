from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import Base,engine
from routes import client_routes,destinataire_routes,livreur_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="YOULOGIX"
    description="Plateforme-de-gestion-logistique-en-temps-reel"
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

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API YouLogiX"} 

@app.get("/health")
def health_check():
    return {"status": "healthy"}