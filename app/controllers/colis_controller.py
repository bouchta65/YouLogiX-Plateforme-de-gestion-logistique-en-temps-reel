from sqlalchemy.orm import Session
from app.models.colis import Colis, StatutColis
from app.schemas.colis import ColisCreate, ColisUpdate
from typing import Optional

def create_colis(db:Session,colis:ColisCreate):
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
    return db_colis

def get_all_colis(db:Session):
    return db.query(Colis).all()

def get_colis_by_id(db:Session,colis_id:int):
    return db.query(Colis).filter(Colis.id == colis_id).first()

def update_colis(db: Session, colis_id: int, colis: ColisUpdate):
    db_colis = get_colis_by_id(db, colis_id)
    if not db_colis:
        return None
    for key, value in colis.model_dump(exclude_unset=True).items():
        setattr(db_colis, key, value)
    db.commit()
    db.refresh(db_colis)
    return db_colis

def delete_colis(db: Session, colis_id: int):
    db_colis = get_colis_by_id(db, colis_id)
    if not db_colis:
        return None
    db.delete(db_colis)
    db.commit()
    return db_colis


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

