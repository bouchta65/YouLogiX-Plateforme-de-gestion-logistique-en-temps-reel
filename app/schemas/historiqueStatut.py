from pydantic import BaseModel
from datetime import datetime

class HistoriqueStatutBase(BaseModel):
    id: int
    id_colis: int
    ancien_statut: str
    nouveau_statut: str
    timestamp: datetime
    id_livreur: int

class HistoriqueStatutCreate(HistoriqueStatutBase):
    pass 

class HistoriqueStatutUpdate(BaseModel):
    id_colis: int | None = None
    ancien_statut: str | None = None
    nouveau_statut: str | None = None
    timestamp: datetime | None = None
    id_livreur: int | None = None
    
class HistoriqueStatutRead(HistoriqueStatutBase):
    id: int
    
    class config:
        from_attributes = True
         



    