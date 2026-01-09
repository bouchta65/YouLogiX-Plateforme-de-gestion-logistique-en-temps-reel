from pydantic import BaseModel , EmailStr

class GestionnaireLogistiqueCreate(BaseModel):
    nom : str
    prenom : str
    email : EmailStr
    telephone : str
    adresse : str
    
class GestionnaireLogistiqueRead(BaseModel):
    id: int
    nom: str
    prenom: str
    email: EmailStr
    telephone: str
    adresse: str
    
    class Config:
        orm_mode = True