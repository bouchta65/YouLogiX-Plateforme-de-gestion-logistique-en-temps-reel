from pydantic import BaseModel
from enum import Enum
from typing import Optional


class StatutColis(str,Enum):
    CREE = "créé"
    COLLECTE = "collecté"
    EN_STOCK = "en stock"
    EN_TRANSIT = "en transit"
    LIVRE = "livré"
    
class ColisBase(BaseModel):
    description: str
    poids: str
    statut: StatutColis
    id_livreur: Optional[int]
    id_client_expediteur: int
    id_destinataire: int
    id_zone: Optional[int]
    ville_destination: str
    
class ColisCreate(ColisBase):
    pass 

class ColisUpdate(BaseModel):
    description: Optional[str] = None
    poids: Optional[str] = None
    statut: Optional[StatutColis] = None
    ville_destination: Optional[str] = None
    id_livreur: Optional[int] = None
    id_zone: Optional[int] = None
    
class ColisRead(ColisBase):
    id: int

    class Config:
        from_attributes = True