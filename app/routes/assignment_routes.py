from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.assignment_controller import (
    assign_colis_to_livreur,
    get_assigned_colis,
    get_unassigned_colis
)
from app.schemas.assignment import AssignmentCreate, AssignmentResponse
from app.schemas.colis import ColisRead
from typing import Optional

router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"]
)


@router.post("/", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED,
             summary="Assigner un colis à un livreur",
             description="Assigne un colis spécifique à un livreur avec option de zone")
def create_assignment_route(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    """
    Assigne un colis à un livreur.
    
    - **colis_id**: ID du colis à assigner
    - **livreur_id**: ID du livreur qui recevra le colis
    - **zone_id**: (Optionnel) ID de la zone de livraison
    
    Le statut du colis sera automatiquement mis à jour vers "en transit" si il était "créé".
    
    Retourne une erreur 404 si le colis, le livreur ou la zone n'existe pas.
    """
    colis, message = assign_colis_to_livreur(db, assignment)
    
    if not colis:
        raise HTTPException(status_code=404, detail=message)
    
    return AssignmentResponse(
        colis_id=colis.id,
        livreur_id=colis.id_livreur,
        zone_id=colis.id_zone,
        message=message
    )


@router.get("/assigned", response_model=list[ColisRead],
            summary="Consulter les colis assignés",
            description="Récupère tous les colis assignés, avec filtre optionnel par livreur")
def get_assigned_colis_route(
    db: Session = Depends(get_db),
    livreur_id: Optional[int] = Query(None, description="Filtrer par ID du livreur")
):
    """
    Récupère tous les colis qui ont été assignés à un livreur.
    
    - **livreur_id**: (Optionnel) Filtre les résultats pour un livreur spécifique
    
    Retourne une liste vide si aucun colis n'est assigné.
    """
    return get_assigned_colis(db, livreur_id)


@router.get("/unassigned", response_model=list[ColisRead],
            summary="Consulter les colis non assignés",
            description="Récupère tous les colis qui n'ont pas encore été assignés à un livreur")
def get_unassigned_colis_route(db: Session = Depends(get_db)):
    """
    Récupère tous les colis qui ne sont pas encore assignés à un livreur.
    
    Utile pour voir quels colis sont en attente d'assignation.
    
    Retourne une liste vide si tous les colis sont assignés.
    """
    return get_unassigned_colis(db)
