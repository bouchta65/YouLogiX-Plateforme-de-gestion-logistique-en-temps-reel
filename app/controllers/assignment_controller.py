from sqlalchemy.orm import Session
from app.models.colis import Colis, StatutColis
from app.models.livreur import Livreur
from app.models.zone import Zone
from app.schemas.assignment import AssignmentCreate
from typing import Optional
from app.utils.logger import get_logger

logger = get_logger(__name__)


def assign_colis_to_livreur(db: Session, assignment: AssignmentCreate):
    try:
        logger.info(f"Tentative d'assignation du colis ID {assignment.colis_id} au livreur ID {assignment.livreur_id}")
        
        colis = db.query(Colis).filter(Colis.id == assignment.colis_id).first()
        if not colis:
            logger.warning(f"Colis non trouvé pour l'assignation - ID: {assignment.colis_id}")
            return None, "Colis not found"
        
        livreur = db.query(Livreur).filter(Livreur.id == assignment.livreur_id).first()
        if not livreur:
            logger.warning(f"Livreur non trouvé pour l'assignation - ID: {assignment.livreur_id}")
            return None, "Livreur not found"
        
        if assignment.zone_id:
            zone = db.query(Zone).filter(Zone.id == assignment.zone_id).first()
            if not zone:
                logger.warning(f"Zone non trouvée pour l'assignation - ID: {assignment.zone_id}")
                return None, "Zone not found"
            colis.id_zone = assignment.zone_id
        
        old_statut = colis.statut
        colis.id_livreur = assignment.livreur_id
        
        if colis.statut == StatutColis.CREE:
            colis.statut = StatutColis.EN_TRANSIT
        
        db.commit()
        db.refresh(colis)
        
        logger.info(f"Colis assigné avec succès - Colis ID: {assignment.colis_id}, Livreur: {livreur.nom} {livreur.prenom}, Statut: {old_statut.value} -> {colis.statut.value}")
        return colis, "Colis assigned successfully"
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de l'assignation du colis ID {assignment.colis_id}: {str(e)}")
        raise


def get_assigned_colis(db: Session, livreur_id: Optional[int] = None):

    query = db.query(Colis).filter(Colis.id_livreur.isnot(None))
    
    if livreur_id:
        query = query.filter(Colis.id_livreur == livreur_id)
    
    return query.all()


def get_unassigned_colis(db: Session):
    return db.query(Colis).filter(Colis.id_livreur.is_(None)).all()
