from sqlalchemy.orm import Session
from app.models.colis import Colis, StatutColis
from app.models.livreur import Livreur
from app.models.zone import Zone
from app.schemas.assignment import AssignmentCreate
from typing import Optional


def assign_colis_to_livreur(db: Session, assignment: AssignmentCreate):

    colis = db.query(Colis).filter(Colis.id == assignment.colis_id).first()
    if not colis:
        return None, "Colis not found"
    
    livreur = db.query(Livreur).filter(Livreur.id == assignment.livreur_id).first()
    if not livreur:
        return None, "Livreur not found"
    
    if assignment.zone_id:
        zone = db.query(Zone).filter(Zone.id == assignment.zone_id).first()
        if not zone:
            return None, "Zone not found"
        colis.id_zone = assignment.zone_id
    
    colis.id_livreur = assignment.livreur_id
    
    if colis.statut == StatutColis.CREE:
        colis.statut = StatutColis.EN_TRANSIT
    
    db.commit()
    db.refresh(colis)
    
    return colis, "Colis assigned successfully"


def get_assigned_colis(db: Session, livreur_id: Optional[int] = None):

    query = db.query(Colis).filter(Colis.id_livreur.isnot(None))
    
    if livreur_id:
        query = query.filter(Colis.id_livreur == livreur_id)
    
    return query.all()


def get_unassigned_colis(db: Session):
    return db.query(Colis).filter(Colis.id_livreur.is_(None)).all()
