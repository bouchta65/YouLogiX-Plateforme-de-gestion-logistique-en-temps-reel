from sqlalchemy.orm import Session
from typing import List
from app.models.zone import Zone
from app.schemas.zone import ZoneCreate, ZoneRead, ZoneUpdate

def create_zone(db: Session, zone_data: ZoneCreate) -> Zone:
    db_zone = Zone(
        nom=zone_data.nom,
        code_postal=zone_data.code_postal
    )
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

def get_zone_by_id(db: Session, zone_id: int) -> Zone:
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise ValueError("Zone non trouvée")
    return zone

def get_all_zones(db: Session) -> List[Zone]:
    return db.query(Zone).order_by(Zone.nom.asc()).all()

def update_zone(db: Session, zone_id: int, zone_data: ZoneUpdate) -> Zone:
    db_zone = get_zone_by_id(db, zone_id)
    db_zone.nom = zone_data.nom or db_zone.nom
    db_zone.code_postal = zone_data.code_postal or db_zone.code_postal
    db.commit()
    db.refresh(db_zone)
    return db_zone

def delete_zone(db: Session, zone_id: int) -> None:
    db_zone = get_zone_by_id(db, zone_id)
    db.delete(db_zone)
    db.commit()
