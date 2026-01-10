from sqlalchemy.orm import Session
from app.models.livreur import Livreur
from app.schemas.livreur import LivreurCreate, LivreurUpdate
from app.utils.logger import get_logger

logger = get_logger(__name__)

def create_livreur(db: Session, livreur: LivreurCreate):
    try:
        logger.info(f"Tentative de création d'un livreur: {livreur.nom} {livreur.prenom}")
        db_livreur = Livreur(
            nom=livreur.nom,
            prenom=livreur.prenom,
            telephone=livreur.telephone,
            vehicule=livreur.vehicule,
            zone_assignee=livreur.zone_assignee
        )
        db.add(db_livreur)
        db.commit()
        db.refresh(db_livreur)
        logger.info(f"Livreur créé avec succès - ID: {db_livreur.id}, Nom: {db_livreur.nom} {db_livreur.prenom}")
        return db_livreur
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la création du livreur: {str(e)}")
        raise


def get_livreurs(db:Session):
    return db.query(Livreur).all()


def get_livreur_by_id(db:Session,livreur_id:int):
    return db.query(Livreur).filter(Livreur.id == livreur_id).first()

def update_livreur(db: Session, livreur_id: int, livreur_update: LivreurUpdate):
    try:
        logger.info(f"Tentative de modification du livreur ID: {livreur_id}")
        db_livreur = get_livreur_by_id(db, livreur_id)
        
        if not db_livreur:
            logger.warning(f"Livreur non trouvé pour la modification - ID: {livreur_id}")
            return None
        
        updated_fields = livreur_update.model_dump(exclude_unset=True)
        for key, value in updated_fields.items():
            setattr(db_livreur, key, value)
        db.commit()
        db.refresh(db_livreur)
        logger.info(f"Livreur modifié avec succès - ID: {livreur_id}, Champs: {list(updated_fields.keys())}")
        return db_livreur
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la modification du livreur ID {livreur_id}: {str(e)}")
        raise

def delete_livreur(db: Session, livreur_id: int):
    try:
        logger.info(f"Tentative de suppression du livreur ID: {livreur_id}")
        db_livreur = get_livreur_by_id(db, livreur_id)
        if not db_livreur:
            logger.warning(f"Livreur non trouvé pour la suppression - ID: {livreur_id}")
            return None
        
        livreur_name = f"{db_livreur.nom} {db_livreur.prenom}"
        db.delete(db_livreur)
        db.commit()
        logger.info(f"Livreur supprimé avec succès - ID: {livreur_id}, Nom: {livreur_name}")
        return db_livreur
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la suppression du livreur ID {livreur_id}: {str(e)}")
        raise
        