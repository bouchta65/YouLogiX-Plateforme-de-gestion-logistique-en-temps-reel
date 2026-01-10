from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.client_expediteur import ClientExpediteur
from app.schemas.client_expediteur import ClientExpediteurCreate, ClientExpediteurUpdate
from app.utils.logger import get_logger

logger = get_logger(__name__)

def create_client(db: Session, client: ClientExpediteurCreate):
    try:
        logger.info(f"Tentative de création d'un client: {client.email}")
        db_client = ClientExpediteur(
            nom=client.nom,
            prenom=client.prenom,
            email=client.email,
            telephone=client.telephone,
            adresse=client.adresse
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        logger.info(f"Client créé avec succès - ID: {db_client.id}, Email: {db_client.email}")
        return db_client
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Erreur d'intégrité lors de la création du client {client.email}: {str(e)}")
        raise ValueError(f"Un client avec l'email {client.email} existe déjà")
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur inattendue lors de la création du client: {str(e)}")
        raise

def get_clients(db: Session):
    return db.query(ClientExpediteur).all()

def get_clients_by_id(db: Session, client_id:int):
    return db.query(ClientExpediteur).filter(ClientExpediteur.id == client_id).first()

def update_client(db:Session , client_id: int , client_update: ClientExpediteurUpdate):
    try:
        logger.info(f"Tentative de modification du client ID: {client_id}")
        db_client = get_clients_by_id(db, client_id)
        if not db_client:
            logger.warning(f"Client non trouvé pour la modification - ID: {client_id}")
            return None
        
        updated_fields = client_update.model_dump(exclude_unset=True)
        for key, value in updated_fields.items():
            setattr(db_client,key,value)   
        db.commit()
        db.refresh(db_client)
        logger.info(f"Client modifié avec succès - ID: {client_id}, Champs: {list(updated_fields.keys())}")
        return db_client
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la modification du client ID {client_id}: {str(e)}")
        raise
        
def delete_client(db:Session, client_id:int):
    try:
        logger.info(f"Tentative de suppression du client ID: {client_id}")
        db_client = get_clients_by_id(db, client_id) 
        if not db_client:
            logger.warning(f"Client non trouvé pour la suppression - ID: {client_id}")
            return None
        
        client_email = db_client.email
        db.delete(db_client)
        db.commit()
        logger.info(f"Client supprimé avec succès - ID: {client_id}, Email: {client_email}")
        return db_client
    except Exception as e:
        db.rollback()
        logger.error(f"Erreur lors de la suppression du client ID {client_id}: {str(e)}")
        raise
