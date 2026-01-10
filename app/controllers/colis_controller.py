from sqlalchemy.orm import Session
from app.models.colis import Colis, StatutColis
from app.schemas.colis import ColisCreate, ColisUpdate
from typing import Optional
from app.utils.logger import get_logger

logger = get_logger(__name__)

def create_colis(db:Session,colis:ColisCreate):
    try:
        logger.info(f"Tentative de création d'un colis - Description: {colis.description}, Destination: {colis.ville_destination}")
        db_colis = Colis(
            description=colis.description,
            poids=colis.poids,
            statut=colis.statut,
            ville_destination=colis.ville_destination,
            id_livreur=colis.id_livreur,
            id_client_expediteur=colis.id_client_expediteur,
            id_destinataire=colis.id_destinataire,
            id_zone=colis.id_zone
        )
        
        db.add(db_colis)
        db.commit()
        db.refresh(db_colis)
        logger.info(f"Colis créé avec succès - ID: {db_colis.id}, Statut: {db_colis.statut.value}")
        return db_colis
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la création du colis: {str(e)}")
        raise

def get_all_colis(db:Session):
    return db.query(Colis).all()

def get_colis_by_id(db:Session,colis_id:int):
    return db.query(Colis).filter(Colis.id == colis_id).first()

def update_colis(db: Session, colis_id: int, colis: ColisUpdate):
    try:
        logger.info(f"Tentative de modification du colis ID: {colis_id}")
        db_colis = get_colis_by_id(db, colis_id)
        if not db_colis:
            logger.warning(f"Colis non trouvé pour la modification - ID: {colis_id}")
            return None
        
        updated_fields = colis.model_dump(exclude_unset=True)
        for key, value in updated_fields.items():
            setattr(db_colis, key, value)
        db.commit()
        db.refresh(db_colis)
        logger.info(f"Colis modifié avec succès - ID: {colis_id}, Champs: {list(updated_fields.keys())}")
        return db_colis
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la modification du colis ID {colis_id}: {str(e)}")
        raise

def delete_colis(db: Session, colis_id: int):
    try:
        logger.info(f"Tentative de suppression du colis ID: {colis_id}")
        db_colis = get_colis_by_id(db, colis_id)
        if not db_colis:
            logger.warning(f"Colis non trouvé pour la suppression - ID: {colis_id}")
            return None
        
        colis_desc = db_colis.description
        db.delete(db_colis)
        db.commit()
        logger.info(f"Colis supprimé avec succès - ID: {colis_id}, Description: {colis_desc}")
        return db_colis
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la suppression du colis ID {colis_id}: {str(e)}")
        raise


def search_colis(
    db: Session, 
    statut: Optional[str] = None, 
    zone_id: Optional[int] = None, 
    livreur_id: Optional[int] = None
):
  
    query = db.query(Colis)
    
    if statut:
        try:
            statut_enum = StatutColis(statut)
            query = query.filter(Colis.statut == statut_enum)
        except ValueError:
            return []
    
    if zone_id is not None:
        query = query.filter(Colis.id_zone == zone_id)
    
    if livreur_id is not None:
        query = query.filter(Colis.id_livreur == livreur_id)
    
    return query.all()


def get_colis_by_livreur(db: Session, livreur_id: int):
    """
    Get all colis assigned to a specific livreur
    """
    return db.query(Colis).filter(Colis.id_livreur == livreur_id).all()

