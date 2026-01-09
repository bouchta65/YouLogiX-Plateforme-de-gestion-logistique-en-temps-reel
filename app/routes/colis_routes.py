from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas.colis import ColisCreate, ColisUpdate, ColisRead
from app.controllers.colis_controller import (
    create_colis,
    get_all_colis,
    get_colis_by_id,
    update_colis,
    delete_colis,
    assign_colis_to_livreur
)
from app.core.database import get_db

router = APIRouter(
    prefix="/colis",
    tags=["Colis"]
)

@router.post("/", response_model=ColisRead, status_code=status.HTTP_201_CREATED)
def create_colis_route(colis: ColisCreate, db: Session = Depends(get_db)):
    try:
        return create_colis(db, colis)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    


@router.get("/", response_model=list[ColisRead])
def get_all_colis_route(db: Session = Depends(get_db)):
    return get_all_colis(db)


@router.get("/{colis_id}", response_model=ColisRead)
def get_colis_by_id_route(colis_id: int, db: Session = Depends(get_db)):
    try:
        return get_colis_by_id(db, colis_id)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))
    


@router.put("/{colis_id}", response_model=ColisRead)
def update_colis_route(colis_id: int, colis_update: ColisUpdate, db: Session = Depends(get_db)):
    try:
        return update_colis(db, colis_id, colis_update)
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.put("/{colis_id}/assign/{livreur_id}", response_model=ColisRead)
def assign_colis_to_livreur_route(colis_id: int, livreur_id: int, db: Session = Depends(get_db)):
    try:
        result = assign_colis_to_livreur(db, colis_id, livreur_id)
        if not result:
            raise HTTPException(status_code=404, detail="Colis non trouvé")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.delete("/{colis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_colis_route(colis_id: int, db: Session = Depends(get_db)):
    try:
        return delete_colis(db, colis_id)
    except ValueError as e:
        raise HTTPException(status_code=404,detail=str(e))
