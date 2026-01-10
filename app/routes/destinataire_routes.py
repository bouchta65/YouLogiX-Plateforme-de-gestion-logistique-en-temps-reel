from fastapi import APIRouter, HTTPException, Depends, status
from app.controllers.destinataire_controller import (create_destinataire, get_destinataires, get_destinataire_by_id, update_destinataire, delete_destinataire)
from app.schemas.destinataire import (DestinataireBase, DestinataireCreate, DestinataireRead, DestinataireUpdate)
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/destinataires",
    tags=["Destinataires"],
    responses={
        404: {"description": "Destinataire non trouvé"},
        500: {"description": "Erreur interne du serveur"}
    }
)

@router.post("/",
             response_model=DestinataireRead,
             status_code=status.HTTP_201_CREATED,
             summary="Créer un nouveau destinataire",
             description="Enregistre un nouveau destinataire dans le système")
def create_destinataire_route(destinataire: DestinataireCreate, db: Session = Depends(get_db)):
    """
    Crée un nouveau destinataire.
    
    **Champs requis** :
    - **nom** : Nom du destinataire
    - **prenom** : Prénom du destinataire
    - **email** : Adresse email
    - **telephone** : Numéro de téléphone
    - **adresse** : Adresse de livraison complète
    
    **Retour** :
    - Code 201 : Destinataire créé avec succès
    
    L'action est enregistrée dans les logs système.
    """
    return create_destinataire(db, destinataire)

@router.get("/",
            response_model=list[DestinataireRead],
            summary="Lister tous les destinataires",
            description="Récupère la liste complète de tous les destinataires enregistrés")
def get_destinataires_route(db: Session = Depends(get_db)):
    """
    Récupère tous les destinataires.
    
    **Retour** :
    - Liste de tous les destinataires avec leurs coordonnées complètes
    - Liste vide si aucun destinataire n'est enregistré
    """
    return get_destinataires(db)

@router.get("/{destinataire_id}",
            response_model=DestinataireRead,
            summary="Récupérer un destinataire par son ID",
            description="Récupère les détails complets d'un destinataire spécifique")
def get_destinataire_by_id_route(destinataire_id: int, db: Session = Depends(get_db)):
    """
    Récupère un destinataire spécifique.
    
    **Paramètres** :
    - **destinataire_id** : Identifiant unique du destinataire
    
    **Retour** :
    - Code 200 : Détails du destinataire
    - Code 404 : Destinataire non trouvé
    """
    destinataire = get_destinataire_by_id(db, destinataire_id)
    if not destinataire:
        raise HTTPException(status_code=404, detail="Destinataire not found")
    return destinataire

@router.put("/{destinataire_id}",
            response_model=DestinataireRead,
            summary="Mettre à jour un destinataire",
            description="Modifie les informations d'un destinataire existant")
def update_destinataire_route(destinataire_id: int, destinataire_update: DestinataireUpdate, db: Session = Depends(get_db)):
    """
    Met à jour les informations d'un destinataire.
    
    **Paramètres** :
    - **destinataire_id** : Identifiant unique du destinataire
    
    **Champs modifiables** :
    - nom, prenom, email, telephone, adresse
    - Seuls les champs fournis seront modifiés
    
    **Retour** :
    - Code 200 : Destinataire mis à jour
    - Code 404 : Destinataire non trouvé
    
    L'action est enregistrée dans les logs système.
    """
    destinataire = update_destinataire(db, destinataire_id, destinataire_update)
    if not destinataire:
        raise HTTPException(status_code=404, detail="Destinataire not found")
    return destinataire

@router.delete("/{destinataire_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Supprimer un destinataire",
               description="Supprime définitivement un destinataire du système")
def delete_destinataire_route(destinataire_id: int, db: Session = Depends(get_db)):
    """
    Supprime un destinataire du système.
    
    **Paramètres** :
    - **destinataire_id** : Identifiant unique du destinataire à supprimer
    
    **Retour** :
    - Code 204 : Destinataire supprimé avec succès
    - Code 404 : Destinataire non trouvé
    
    Attention : Cette opération est irréversible.
    La suppression est enregistrée dans les logs système.
    """
    destinataire = delete_destinataire(db, destinataire_id)
    if not destinataire:
        raise HTTPException(status_code=404, detail="Destinataire not found")
    return None