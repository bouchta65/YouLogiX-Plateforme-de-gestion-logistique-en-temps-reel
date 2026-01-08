from fastapi import APIRouter, HTTPException, Depends, status
from app.controllers.destinataire_controller import (create_destinataire, get_destinataires, get_destinataire_by_id, update_destinataire, delete_destinataire)
from app.schemas.destinataire import (DestinataireBase, DestinataireCreate, DestinataireRead, DestinataireUpdate)
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/destinataires",
    tags=["Destinataires"]
)

@router.post("/", response_model=DestinataireRead, status_code=status.HTTP_201_CREATED)
def create_destinataire_route(destinataire: DestinataireCreate, db: Session = Depends(get_db)):
    return create_destinataire(db, destinataire)

@router.get("/", response_model=list[DestinataireRead])
def get_destinataires_route(db: Session = Depends(get_db)):
    return get_destinataires(db)

@router.get("/{destinataire_id}", response_model=DestinataireRead)
def get_destinataire_by_id_route(destinataire_id: int, db: Session = Depends(get_db)):
    destinataire = get_destinataire_by_id(db, destinataire_id)
    if not destinataire:
        raise HTTPException(status_code=404, detail="Destinataire not found")
    return destinataire

@router.put("/{destinataire_id}", response_model=DestinataireRead)
def update_destinataire_route(destinataire_id: int, destinataire_update: DestinataireUpdate, db: Session = Depends(get_db)):
    destinataire = update_destinataire(db, destinataire_id, destinataire_update)
    if not destinataire:
        raise HTTPException(status_code=404, detail="Destinataire not found")
    return destinataire

@router.delete("/{destinataire_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_destinataire_route(destinataire_id: int, db: Session = Depends(get_db)):
    destinataire = delete_destinataire(db, destinataire_id)
    if not destinataire:
        raise HTTPException(status_code=404, detail="Destinataire not found")
    return None