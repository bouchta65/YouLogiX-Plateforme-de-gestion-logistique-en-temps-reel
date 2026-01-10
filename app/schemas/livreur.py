from pydantic import BaseModel, ConfigDict
from typing import Optional


class LivreurBase(BaseModel):
    nom: str
    prenom: str
    telephone: str
    vehicule: Optional[str] = None
    zone_assignee: Optional[str] = None
       
class LivreurCreate(LivreurBase):
    pass

class LivreurUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None
    telephone: str | None = None 
    vehicule: str | None = None
    zone_assignee: str | None = None

class LivreurRead(LivreurBase):
    id: int
    model_config = ConfigDict(from_attributes=True) 
