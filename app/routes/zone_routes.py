from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.zone_controller import create_zone, get_all_zones, get_zone
from app.schemas.zone import ZoneBase, ZoneRead, ZoneUpdate, ZoneCreate

router = APIRouter(
    prefix="/zones",
    tags=["Zones"]
)


@router.post("/", response_model=ZoneRead, status_code=status.HTTP_201_CREATED)
def create_zone_route(zone: ZoneCreate, db: Session = Depends(get_db)):
    return create_zone(db, zone)


@router.get("/", response_model=list[ZoneRead])
def get_all_zones_route(db: Session = Depends(get_db)):
    return get_all_zones(db)


@router.get("/{id}", response_model=ZoneRead)
def get_zone_route(id: int, db: Session = Depends(get_db)):
    zone = get_zone(db, id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone
