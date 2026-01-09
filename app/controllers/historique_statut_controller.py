from sqlalchemy.orm import Session 
from app.schemas.historiqueStatut import (HistoriqueStatutBase,HistoriqueStatutCreate,HistoriqueStatutRead,HistoriqueStatutUpdate)
from app.models.historique_statut import HistoriqueStatut
from datetime import datetime
from app.models.colis import Colis

VALID_TRANSITIONS = {
    "créé": ["collecté"],
    "collecté": ["en stock"],
    "en stock": ["en transit"],
    "en transit": ["livré"],
}


def create_historique(db:Session,historique_data:HistoriqueStatutCreate):
    
    db_colis = db.query(Colis).filter(Colis.id == historique_data.id_colis).first()
    if not db_colis:
        raise ValueError("Colis non trouvé")
    
    check_colis_modifiable(db_colis)
    
    ancien_statut = db_colis.statut
    
    validate_transition(ancien_statut,historique_data.nouveau_statut)
 
    db_historique = HistoriqueStatut(
        id_colis=historique_data.id_colis,
        ancien_statut=ancien_statut,
        nouveau_statut=historique_data.nouveau_statut,
        timestamp=historique_data.timestamp or datetime.utcnow(),
        id_livreur=historique_data.id_livreur
    )
    
    db_colis.statut = historique_data.nouveau_statut
    
    db.add(db_historique)
    db.commit()
    db.refresh(db_historique)
    return db_historique


def get_historique_by_colis(db:Session,colis_id:int):
    return db.query(HistoriqueStatut).filter(HistoriqueStatut.id_colis == colis_id).order_by(HistoriqueStatut.timestamp.asc()).all()


def get_historique_by_livreur(db:Session,livreur_id:int):
    return db.query(HistoriqueStatut).filter(HistoriqueStatut.id_livreur == livreur_id).order_by(HistoriqueStatut.timestamp.asc()).all()


def validate_transition(ancien_statut: str, nouveau_statut: str):
    if nouveau_statut not in VALID_TRANSITIONS.get(ancien_statut,[]):
        raise ValueError(f"Transition invalide : {ancien_statut} → {nouveau_statut}")
    
def check_colis_modifiable(db_colis: Colis):
    if db_colis.statut == "livré":
        raise ValueError("Ce colis est déjà livré et ne peut plus être modifié.")
        
    


