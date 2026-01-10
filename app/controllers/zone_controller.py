from sqlalchemy.orm import Session
from app.models.zone import Zone
from app.schemas.zone import ZoneCreate, ZoneUpdate
from app.utils.logger import get_logger

logger = get_logger(__name__)


def create_zone(db: Session, zone: ZoneCreate):
    try:
        logger.info(f"Tentative de création d'une zone: {zone.nom}")
        db_zone = Zone(
            nom=zone.nom,
            description=zone.description
        )
        db.add(db_zone)
        db.commit()
        db.refresh(db_zone)
        logger.info(f"Zone créée avec succès - ID: {db_zone.id}, Nom: {db_zone.nom}")
        return db_zone
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la création de la zone: {str(e)}")
        raise


def get_all_zones(db: Session):
    return db.query(Zone).all()


def get_zone(db: Session, zone_id: int):
    return db.query(Zone).filter(Zone.id == zone_id).first()
