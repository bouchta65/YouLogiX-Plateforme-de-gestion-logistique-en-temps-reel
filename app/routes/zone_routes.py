from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.zone_controller import create_zone, get_all_zones, get_zone
from app.schemas.zone import ZoneBase, ZoneRead, ZoneUpdate, ZoneCreate

router = APIRouter(
    prefix="/zones",
    tags=["Zones"],
    responses={
        404: {"description": "Zone non trouvée"},
        500: {"description": "Erreur interne du serveur"}
    }
)


@router.post("/",
             response_model=ZoneRead,
             status_code=status.HTTP_201_CREATED,
             summary="Créer une nouvelle zone de livraison",
             description="Enregistre une nouvelle zone géographique de livraison")
def create_zone_route(zone: ZoneCreate, db: Session = Depends(get_db)):
    """
    Crée une nouvelle zone de livraison.
    
    **Champs requis** :
    - **nom** : Nom de la zone (ex: "Centre-Ville", "Zone Nord", etc.)
    - **description** : Description de la zone (secteur géographique, points de repère, etc.)
    
    **Retour** :
    - Code 201 : Zone créée avec succès
    
    Les zones permettent d'organiser efficacement les livraisons.
    L'action est enregistrée dans les logs système.
    """
    return create_zone(db, zone)


@router.get("/",
            response_model=list[ZoneRead],
            summary="Lister toutes les zones de livraison",
            description="Récupère la liste complète de toutes les zones de livraison")
def get_all_zones_route(db: Session = Depends(get_db)):
    """
    Récupère toutes les zones de livraison.
    
    **Retour** :
    - Liste de toutes les zones avec leurs détails
    - Liste vide si aucune zone n'est configurée
    
    Utile pour afficher la couverture géographique disponible.
    """
    return get_all_zones(db)


@router.get("/{id}",
            response_model=ZoneRead,
            summary="Récupérer une zone par son ID",
            description="Récupère les détails d'une zone de livraison spécifique")
def get_zone_route(id: int, db: Session = Depends(get_db)):
    """
    Récupère une zone de livraison spécifique.
    
    **Paramètres** :
    - **id** : Identifiant unique de la zone
    
    **Retour** :
    - Code 200 : Détails de la zone
    - Code 404 : Zone non trouvée
    """
    zone = get_zone(db, id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone
