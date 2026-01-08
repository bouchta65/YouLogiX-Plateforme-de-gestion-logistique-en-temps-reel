from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.schemas.colis import ColisCreate, ColisUpdate, ColisRead
from app.controllers.colis_controller import (
    create_colis,
    get_all_colis,
    get_colis_by_id,
    update_colis,
    delete_colis
)
from app.core.database import get_db

router = APIRouter(
    prefix="/colis",
    tags=["Colis"]
)

@router.post("/", response_model=ColisRead, status_code=status.HTTP_201_CREATED)
def create_colis_route(colis: ColisCreate, db: Session = Depends(get_db)):
    return create_colis(db, colis)


@router.get("/", response_model=list[ColisRead])
def get_all_colis_route(db: Session = Depends(get_db)):
    return get_all_colis(db)


@router.get("/{colis_id}", response_model=ColisRead)
def get_colis_by_id_route(colis_id: int, db: Session = Depends(get_db)):
    db_colis = get_colis_by_id(db, colis_id)
    if not db_colis:
        raise HTTPException(status_code=404, detail="Colis not found")
    return db_colis


@router.put("/{colis_id}", response_model=ColisRead)
def update_colis_route(colis_id: int, colis_update: ColisUpdate, db: Session = Depends(get_db)):
    db_colis = update_colis(db, colis_id, colis_update)
    if not db_colis:
        raise HTTPException(status_code=404, detail="Colis not found")
    return db_colis


@router.delete("/{colis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_colis_route(colis_id: int, db: Session = Depends(get_db)):
    db_colis = delete_colis(db, colis_id)
    if not db_colis:
        raise HTTPException(status_code=404, detail="Colis not found")
    return None
