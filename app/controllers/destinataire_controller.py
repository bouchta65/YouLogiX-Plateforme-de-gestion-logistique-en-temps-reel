from sqlalchemy.orm import Session
from app.models.destinataire import Destinataire
from app.schemas.destinataire import DestinataireCreate, DestinataireUpdate
from app.utils.logger import get_logger

logger = get_logger(__name__)

def create_destinataire(db: Session, destinataire: DestinataireCreate):
    try:
        logger.info(f"Tentative de création d'un destinataire: {destinataire.email}")
        db_client = Destinataire(
            nom=destinataire.nom,
            prenom=destinataire.prenom,
            email=destinataire.email,
            telephone=destinataire.telephone,
            adresse=destinataire.adresse
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        logger.info(f"Destinataire créé avec succès - ID: {db_client.id}, Email: {db_client.email}")
        return db_client
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la création du destinataire: {str(e)}")
        raise


def get_destinataires(db:Session):
    return db.query(Destinataire).all()


def get_destinataire_by_id(db:Session,destinataire_id:int):
    return db.query(Destinataire).filter(Destinataire.id == destinataire_id).first()

def update_destinataire(db: Session, destinataire_id: int, destinataire_update: DestinataireUpdate):
    try:
        logger.info(f"Tentative de modification du destinataire ID: {destinataire_id}")
        db_destinataire = get_destinataire_by_id(db, destinataire_id)
        if not db_destinataire:
            logger.warning(f"Destinataire non trouvé pour la modification - ID: {destinataire_id}")
            return None
        
        updated_fields = destinataire_update.model_dump(exclude_unset=True)
        for key, value in updated_fields.items():
            setattr(db_destinataire, key, value)
        db.commit()
        db.refresh(db_destinataire)
        logger.info(f"Destinataire modifié avec succès - ID: {destinataire_id}, Champs: {list(updated_fields.keys())}")
        return db_destinataire
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la modification du destinataire ID {destinataire_id}: {str(e)}")
        raise

def delete_destinataire(db: Session, destinataire_id: int):
    try:
        logger.info(f"Tentative de suppression du destinataire ID: {destinataire_id}")
        db_destinataire = get_destinataire_by_id(db, destinataire_id)
        if not db_destinataire:
            logger.warning(f"Destinataire non trouvé pour la suppression - ID: {destinataire_id}")
            return None
        
        destinataire_email = db_destinataire.email
        db.delete(db_destinataire)
        db.commit()
        logger.info(f"Destinataire supprimé avec succès - ID: {destinataire_id}, Email: {destinataire_email}")
        return db_destinataire
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la suppression du destinataire ID {destinataire_id}: {str(e)}")
        raise
