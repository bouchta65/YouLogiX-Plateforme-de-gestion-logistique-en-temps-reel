from fastapi import APIRouter, HTTPException, Depends, status
from app.controllers.livreur_controller import (create_livreur, update_livreur, delete_livreur, get_livreur_by_id, get_livreurs)
from app.controllers.colis_controller import get_colis_by_livreur
from app.schemas.livreur import (LivreurBase, LivreurRead, LivreurCreate, LivreurUpdate)
from app.schemas.colis import ColisRead
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/livreurs",
    tags=["Livreurs"],
    responses={
        404: {"description": "Livreur non trouvé"},
        500: {"description": "Erreur interne du serveur"}
    }
)



@router.post("/",
             response_model=LivreurRead,
             status_code=status.HTTP_201_CREATED,
             summary="Créer un nouveau livreur",
             description="Enregistre un nouveau livreur dans le système avec ses informations et zone assignée")
def create_livreur_route(livreur: LivreurCreate, db: Session = Depends(get_db)):
    """
    Crée un nouveau livreur.
    
    **Champs requis** :
    - **nom** : Nom du livreur
    - **prenom** : Prénom du livreur
    - **telephone** : Numéro de téléphone
    - **vehicule** : Type de véhicule (voiture, moto, vélo, etc.)
    - **zone_assignee** : Zone géographique d'intervention
    
    **Retour** :
    - Code 201 : Livreur créé avec succès
    
    L'action est enregistrée dans les logs système.
    """
    return create_livreur(db, livreur)



@router.get("/",
            response_model=list[LivreurRead],
            summary="Lister tous les livreurs",
            description="Récupère la liste complète de tous les livreurs enregistrés dans le système")
def get_livreurs_route(db: Session = Depends(get_db)):
    """
    Récupère tous les livreurs.
    
    **Retour** :
    - Liste de tous les livreurs avec leurs informations complètes
    - Inclut la zone assignée et le type de véhicule
    - Liste vide si aucun livreur n'est enregistré
    """
    return get_livreurs(db)


@router.get("/{livreur_id}",
            response_model=LivreurRead,
            summary="Récupérer un livreur par son ID",
            description="Récupère les détails complets d'un livreur spécifique")
def get_livreur_by_id_route(livreur_id: int, db: Session = Depends(get_db)):
    """
    Récupère un livreur spécifique par son identifiant.
    
    **Paramètres** :
    - **livreur_id** : Identifiant unique du livreur
    
    **Retour** :
    - Code 200 : Détails du livreur (nom, prénom, véhicule, zone, etc.)
    - Code 404 : Livreur non trouvé
    """
    livreur = get_livreur_by_id(db, livreur_id)
    if not livreur:
        raise HTTPException(status_code=404, detail="Livreur not found")
    return livreur



@router.get("/{livreur_id}/colis",
            response_model=list[ColisRead],
            summary="Récupérer tous les colis d'un livreur",
            description="Liste tous les colis assignés à un livreur spécifique avec leurs statuts")
def get_livreur_colis_route(livreur_id: int, db: Session = Depends(get_db)):
    """
    Récupère tous les colis assignés à un livreur.
    
    **Paramètres** :
    - **livreur_id** : Identifiant unique du livreur
    
    **Retour** :
    - Liste des colis avec leurs statuts et destinations
    - Liste vide si le livreur n'a pas de colis assignés
    - Code 404 si le livreur n'existe pas
    
    Utile pour voir la charge de travail actuelle d'un livreur.
    """
    # Verify livreur exists
    livreur = get_livreur_by_id(db, livreur_id)
    if not livreur:
        raise HTTPException(status_code=404, detail="Livreur not found")
    
    return get_colis_by_livreur(db, livreur_id)




@router.put("/{livreur_id}",
            response_model=LivreurRead,
            summary="Mettre à jour un livreur",
            description="Modifie les informations d'un livreur existant")
def update_livreur_route(livreur_id: int, livreur_update: LivreurUpdate, db: Session = Depends(get_db)):
    """
    Met à jour les informations d'un livreur.
    
    **Paramètres** :
    - **livreur_id** : Identifiant unique du livreur
    
    **Champs modifiables** :
    - nom, prenom, telephone, vehicule, zone_assignee
    - Seuls les champs fournis seront modifiés
    
    **Retour** :
    - Code 200 : Livreur mis à jour
    - Code 404 : Livreur non trouvé
    
    L'action est enregistrée dans les logs système.
    """
    livreur = update_livreur(db, livreur_id, livreur_update)
    if not livreur:
        raise HTTPException(status_code=404, detail="Livreur not found")
    return livreur




@router.delete("/{livreur_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Supprimer un livreur",
               description="Supprime définitivement un livreur du système")
def delete_livreur_route(livreur_id: int, db: Session = Depends(get_db)):
    """
    Supprime un livreur du système.
    
    **Paramètres** :
    - **livreur_id** : Identifiant unique du livreur à supprimer
    
    **Retour** :
    - Code 204 : Livreur supprimé avec succès
    - Code 404 : Livreur non trouvé
    
    Attention : Cette opération est irréversible.
    Les colis assignés à ce livreur devront être réassignés.
    La suppression est enregistrée dans les logs système.
    """
    livreur = delete_livreur(db, livreur_id)
    if not livreur:
        raise HTTPException(status_code=404, detail="Livreur not found")
    return None