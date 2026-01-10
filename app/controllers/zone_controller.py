from sqlalchemy.orm import Session
from app.models.zone import Zone
from app.schemas.zone import ZoneCreate, ZoneUpdate


def create_zone(db: Session, zone: ZoneCreate):
    db_zone = Zone(
        nom=zone.nom,
        description=zone.description
    )
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone


def get_all_zones(db: Session):
    return db.query(Zone).all()


def get_zone(db: Session, zone_id: int):
    return db.query(Zone).filter(Zone.id == zone_id).first()
