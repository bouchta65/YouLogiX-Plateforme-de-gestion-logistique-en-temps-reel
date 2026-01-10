from sqlalchemy.orm import Session
from app.models.livreur import Livreur
from app.schemas.livreur import LivreurCreate, LivreurUpdate

def create_livreur(db: Session, livreur: LivreurCreate):
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
    return db_livreur


def get_livreurs(db:Session):
    return db.query(Livreur).all()


def get_livreur_by_id(db:Session,livreur_id:int):
    return db.query(Livreur).filter(Livreur.id == livreur_id).first()

def update_livreur(db: Session, livreur_id: int, livreur_update: LivreurUpdate):
    db_livreur = get_livreur_by_id(db, livreur_id)
    
    if not db_livreur:
        return None
    
    for key, value in livreur_update.model_dump(exclude_unset=True).items():
        setattr(db_livreur, key, value)
    db.commit()
    db.refresh(db_livreur)
    return db_livreur

def delete_livreur(db: Session, livreur_id: int):
    db_livreur = get_livreur_by_id(db, livreur_id)
    if not db_livreur:
        return None
    db.delete(db_livreur)
    db.commit()
    return db_livreur
        