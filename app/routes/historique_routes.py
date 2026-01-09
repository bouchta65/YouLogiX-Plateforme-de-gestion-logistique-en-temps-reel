from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas.historiqueStatut import (HistoriqueStatutCreate,HistoriqueStatutRead)
from app.controllers.historique_statut_controller import (create_historique,get_historique_by_colis,get_historique_by_livreur)
from app.core.database import get_db

router = APIRouter(
    prefix="/historique",
    tags=["Historique"]
)

@router.post("/", response_model=HistoriqueStatutRead, status_code=status.HTTP_201_CREATED)
def create_historique_route(historique: HistoriqueStatutCreate, db: Session = Depends(get_db)):
    try:
        return create_historique(db, historique)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/colis/{colis_id}", response_model=list[HistoriqueStatutRead])
def get_historique_by_colis_route(colis_id: int, db: Session = Depends(get_db)):
    try:
        return get_historique_by_colis(db, colis_id)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))

@router.get("/livreur/{livreur_id}", response_model=list[HistoriqueStatutRead])
def get_historique_by_livreur_route(livreur_id: int, db: Session = Depends(get_db)):
    try:
        return get_historique_by_livreur(db, livreur_id)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))
