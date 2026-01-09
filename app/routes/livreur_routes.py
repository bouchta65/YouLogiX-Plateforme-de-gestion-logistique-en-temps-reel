from fastapi import APIRouter, HTTPException, Depends, status
from app.controllers.livreur_controller import (create_livreur, update_livreur, delete_livreur, get_livreur_by_id, get_livreurs)
from app.schemas.livreur import (LivreurBase, LivreurRead, LivreurCreate, LivreurUpdate)
from app.schemas.colis import ColisRead
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/livreurs",
    tags=["Livreurs"]
)

@router.post("/", response_model=LivreurRead, status_code=status.HTTP_201_CREATED)
def create_livreur_route(livreur: LivreurCreate, db: Session = Depends(get_db)):
    try:
        return create_livreur(db, livreur)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.get("/", response_model=list[LivreurRead])
def get_livreurs_route(db: Session = Depends(get_db)):
    return get_livreurs(db)

@router.get("/{livreur_id}", response_model=LivreurRead)
def get_livreur_by_id_route(livreur_id: int, db: Session = Depends(get_db)):
    try:
        return get_livreur_by_id(db, livreur_id)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))

@router.get("/{livreur_id}/colis", response_model=list[ColisRead])
def get_colis_assignes_route(livreur_id: int, db: Session = Depends(get_db)):
    from app.controllers.livreur_controller import get_colis_assignes
    return get_colis_assignes(db, livreur_id)
    
@router.put("/{livreur_id}", response_model=LivreurRead)
def update_livreur_route(livreur_id: int, livreur_update: LivreurUpdate, db: Session = Depends(get_db)):
    try:
        return update_livreur(db, livreur_id, livreur_update)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))


@router.delete("/{livreur_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_livreur_route(livreur_id: int, db: Session = Depends(get_db)):
    try:
        return delete_livreur(db, livreur_id)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))