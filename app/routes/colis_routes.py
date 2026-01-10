from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from app.schemas.colis import ColisCreate, ColisUpdate, ColisRead
from app.controllers.colis_controller import (
    create_colis,
    get_all_colis,
    get_colis_by_id,
    update_colis,
    delete_colis,
    search_colis
)
from app.core.database import get_db
from typing import Optional

router = APIRouter(
    prefix="/colis",
    tags=["Colis"],
    responses={
        404: {"description": "Colis non trouvé"},
        500: {"description": "Erreur interne du serveur"}
    }
)

@router.post("/", 
             response_model=ColisRead, 
             status_code=status.HTTP_201_CREATED,
             summary="Créer un nouveau colis",
             description="Enregistre un nouveau colis dans le système avec toutes ses informations")
def create_colis_route(colis: ColisCreate, db: Session = Depends(get_db)):
    return create_colis(db, colis)


@router.get("/", 
            response_model=list[ColisRead],
            summary="Lister tous les colis",
            description="Récupère la liste complète de tous les colis enregistrés dans le système")
def get_all_colis_route(db: Session = Depends(get_db)):
    """
    Récupère tous les colis enregistrés.
    
    Retourne une liste vide si aucun colis n'est enregistré.
    """
    return get_all_colis(db)


@router.get("/search", 
            response_model=list[ColisRead],
            summary="Rechercher des colis avec filtres",
            description="Filtre les colis par statut, zone et/ou livreur")
def search_colis_route(
    db: Session = Depends(get_db),
    statut: Optional[str] = Query(None, description="Statut du colis (cree, collecte, en stock, en transit, livrE)"),
    zone_id: Optional[int] = Query(None, description="ID de la zone de livraison"),
    livreur_id: Optional[int] = Query(None, description="ID du livreur assigné")
):
    """
    Recherche des colis avec des filtres optionnels.
    
    Paramètres de filtrage :
    - **statut**: Statut du colis (cree, collecte, en stock, en transit, livrE)
    - **zone_id**: ID de la zone de livraison
    - **livreur_id**: ID du livreur assigné
    
    Tous les filtres sont optionnels et peuvent être combinés.
    Si aucun filtre n'est fourni, retourne tous les colis.
    """
    return search_colis(db, statut=statut, zone_id=zone_id, livreur_id=livreur_id)


@router.get("/{colis_id}", 
            response_model=ColisRead,
            summary="Récupérer un colis par son ID",
            description="Récupère les détails d'un colis spécifique à partir de son identifiant")
def get_colis_by_id_route(colis_id: int, db: Session = Depends(get_db)):
    """
    Récupère un colis spécifique par son ID.
    
    - **colis_id**: L'identifiant unique du colis
    
    Retourne une erreur 404 si le colis n'existe pas.
    """
    db_colis = get_colis_by_id(db, colis_id)
    if not db_colis:
        raise HTTPException(status_code=404, detail="Colis not found")
    return db_colis


@router.put("/{colis_id}", 
            response_model=ColisRead,
            summary="Mettre à jour un colis",
            description="Modifie les informations d'un colis existant")
def update_colis_route(colis_id: int, colis_update: ColisUpdate, db: Session = Depends(get_db)):
    """
    Met à jour un colis existant.
    
    - **colis_id**: L'identifiant unique du colis
    - Seuls les champs fournis seront mis à jour
    
    Champs modifiables :
    - description
    - poids
    - statut
    - ville_destination
    - id_livreur
    - id_zone
    
    Retourne une erreur 404 si le colis n'existe pas.
    """
    db_colis = update_colis(db, colis_id, colis_update)
    if not db_colis:
        raise HTTPException(status_code=404, detail="Colis not found")
    return db_colis


@router.delete("/{colis_id}", 
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Supprimer un colis",
               description="Supprime définitivement un colis du système")
def delete_colis_route(colis_id: int, db: Session = Depends(get_db)):
    """
    Supprime un colis du système.
    
    - **colis_id**: L'identifiant unique du colis à supprimer
    
    Retourne une erreur 404 si le colis n'existe pas.
    ⚠️ Attention : Cette opération est irréversible.
    """
    db_colis = delete_colis(db, colis_id)
    if not db_colis:
        raise HTTPException(status_code=404, detail="Colis not found")
    return None
