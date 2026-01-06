from sqlalchemy import Session 
from models.destinataire import Destinataire
from schemas.destinataire import DestinataireCreate,DestinataireUpdate

def create_destinataire(db: Session, destinataire: DestinataireCreate):
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
    return db_client


def get_destinataires(db:Session):
    return db.query(Destinataire).all()


def get_destinataire_by_id(db:Session,destinataire_id:int):
    return db.query(Destinataire).filter(Destinataire.id == destinataire_id).first()

def update_destinataire(db:Session,destinataire_id:int,destinataire_update=DestinataireUpdate):
    db_destinataire = get_destinataire_by_id(destinataire_id)
    if not db_destinataire:
        return None
    for key,value in destinataire_update.dict(exclude_unset=True).items():
        setattr(db_destinataire,key,value)
    db.commit()
    db.refresh(db_destinataire)
    return db_destinataire

def delete_destinataire(db:Session,destinataire_id):
    db_destinataire = get_destinataire_by_id(destinataire_id)
    if not db_destinataire:
        return None
    db.delete(db_destinataire)
    db.commit()
    return db_destinataire
