from pydantic import BaseModel , EmailStr


class ClientExpediteurBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    telephone: str
    adresse: str
    

class ClientExpediteurCreate(ClientExpediteurBase):
    pass
    
class ClientExpediteurUpdate(BaseModel):
    nom: str | None = None
    prenom: str | None = None
    email: EmailStr | None = None
    telephone: str | None = None
    adresse: str | None = None
    
    
class ClientExpediteurRead(ClientExpediteurBase):
    id: int
    class Config:
        orm_mode = True