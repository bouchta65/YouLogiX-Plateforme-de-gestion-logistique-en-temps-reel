from sqlalchemy import Column, Integer, String , ForeignKey , Enum
from core.database import Base
import enum

class StatutColis(enum.Enum):
    CREE = "créé"
    COLLECTE = "collecté"
    EN_STOCK = "en stock"
    EN_TRANSIT = "en transit"
    LIVRE = "livré"
    
    
class Colis(Base):
    __tablename__ = "colis"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    poids = Column(String, nullable=False)
    statut = Column(Enum(StatutColis), default=StatutColis.CREE)
    id_livreur = Column(Integer, ForeignKey("livreurs.id"), nullable=True)
    id_client_expediteur = Column(Integer, ForeignKey("client_expediteur.id"), nullable=False)
    id_destinataire = Column(Integer, ForeignKey("destinataires.id"), nullable=False)
    id_zone = Column(Integer, ForeignKey("zones.id"), nullable=True)
    ville_destination = Column(String, nullable=False)
