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
    tags=["Assignations"],
    responses={
        404: {"description": "Ressource non trouvée (colis, livreur ou zone)"},
        500: {"description": "Erreur interne du serveur"}
    }
)


@router.post("/",
             response_model=AssignmentResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Assigner un colis à un livreur",
             description="Assigne un colis spécifique à un livrer avec option de zone")
def create_assignment_route(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    """
    Assigne un colis à un livreur.
    
    **Champs requis** :
    - **colis_id** : ID du colis à assigner
    - **livreur_id** : ID du livreur qui recevra le colis
    
    **Champs optionnels** :
    - **zone_id** : ID de la zone de livraison (si applicable)
    
    Le statut du colis sera automatiquement mis à jour vers "en transit" si il était "créé".
    
    Retourne une erreur 404 si le colis, le livreur ou la zone n'existe pas.

    **Retour** :
    - Code 201 : Assignation créée avec succès
    - Code 404 : Colis, livreur ou zone non trouvé
    
    Permet d'organiser efficacement les tournées de livraison.
    L'action est enregistrée dans les logs système.
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


@router.get("/assigned",
            response_model=list[ColisRead],
            summary="Consulter les colis assignés",
            description="Liste tous les colis qui ont un livreur assigné, avec filtre optionnel par livreur")
def get_assigned_colis_route(
    db: Session = Depends(get_db),
    livreur_id: Optional[int] = Query(None, description="Filtrer par ID du livreur spécifique")
):
    """
    Récupère tous les colis qui ont été assignés à un livreur.
    
    **Paramètres optionnels** :
    - **livreur_id** : Filtre les résultats pour un livreur spécifique
    
    **Retour** :
    - Liste des colis assignés avec leurs informations complètes
    - Liste vide si aucun colis n'est assigné
    
    Utile pour suivre l'état des assignations en cours.
    """
    return get_assigned_colis(db, livreur_id)


@router.get("/unassigned",
            response_model=list[ColisRead],
            summary="Consulter les colis non assignés",
            description="Liste tous les colis en attente d'assignation à un livreur")
def get_unassigned_colis_route(db: Session = Depends(get_db)):
    """
    Récupère tous les colis qui ne sont pas encore assignés à un livreur.
    
    **Retour** :
    - Liste des colis en attente d'assignation
    - Liste vide si tous les colis sont assignés
    
    **Cas d'usage** :
    - Voir les colis nécessitant une assignation
    - Planifier les prochaines tournées
    - Identifier les retards de traitement
    
    Ces colis requirent une action pour être pris en charge.
    """
    return get_unassigned_colis(db)
