from sqlalchemy import Column, Integer, String
from core.database import Base

class Livreur(Base):
    __tablename__ = "livreurs"

    id = Column(Integer, primary_key=True)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    vehicule = Column(String, nullable=True)
    zone_assignee = Column(String, nullable=True)
