from sqlalchemy import Session 
from models.client_expediteur import ClientExpediteur
from schemas.client_expediteur import ClientExpediteurCreate , ClientExpediteurUpdate

def create_client(db: Session, client: ClientExpediteurCreate):
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
    return db_client

def get_clients(db: Session):
    return db.query(ClientExpediteur).all()

def get_clients_by_id(db: Session, client_id:int):
    return db.query(ClientExpediteur).filter(ClientExpediteur.id == client_id).first()

def update_client(db:Session , client_id: int , client_update: ClientExpediteurUpdate):
    db_client = get_clients_by_id(db, client_id)
    if not db_client:
        return None
    for key, value in client_update.dict(exclude_unset=True).items():
        setattr(db_client,key,value)   
    db.commit()
    db.refresh(db_client)
    return db_client
        
def delete_client(db:Session, client_id:int):
    db_client = get_clients_by_id(db, client_id) 
    if not db_client:
        return None
    db.delete(db_client)
    db.commit()
    return db_client
