from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.zone import ZoneCreate, ZoneRead, ZoneUpdate
from app.controllers.zone_controller import (create_zone,get_zone_by_id,get_all_zones,update_zone,delete_zone)
from app.core.database import get_db

router = APIRouter(prefix="/zones", tags=["Zones"])

@router.post("/", response_model=ZoneRead, status_code=status.HTTP_201_CREATED)
def api_create_zone(zone_data: ZoneCreate, db: Session = Depends(get_db)):
    try:
        return create_zone(db, zone_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{zone_id}", response_model=ZoneRead)
def api_get_zone(zone_id: int, db: Session = Depends(get_db)):
    try:
        return get_zone_by_id(db, zone_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[ZoneRead])
def api_get_all_zones(db: Session = Depends(get_db)):
    return get_all_zones(db)


@router.put("/{zone_id}", response_model=ZoneRead)
def api_update_zone(zone_id: int, zone_data: ZoneUpdate, db: Session = Depends(get_db)):
    try:
        return update_zone(db, zone_id, zone_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_zone(zone_id: int, db: Session = Depends(get_db)):
    try:
        delete_zone(db, zone_id)
        return {"detail": "Zone supprimée avec succès"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
