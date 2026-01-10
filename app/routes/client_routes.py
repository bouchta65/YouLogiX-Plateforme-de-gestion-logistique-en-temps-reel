from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.client_controller import (create_client, update_client, delete_client, get_clients, get_clients_by_id)
from app.schemas.client_expediteur import (ClientExpediteurBase, ClientExpediteurRead, ClientExpediteurUpdate, ClientExpediteurCreate)

router = APIRouter(
    prefix="/clients",
    tags=["Clients Expéditeurs"],
    responses={
        404: {"description": "Client non trouvé"},
        409: {"description": "Conflit - Email déjà utilisé"},
        500: {"description": "Erreur interne du serveur"}
    }
)

@router.post("/",
             response_model=ClientExpediteurRead,
             status_code=status.HTTP_201_CREATED,
             summary="Créer un nouveau client expéditeur",
             description="Enregistre un nouveau client expéditeur dans le système")
def create_client_route(client: ClientExpediteurCreate,db: Session = Depends(get_db)):
    """
    Crée un nouveau client expéditeur.
    
    **Champs requis** :
    - **nom** : Nom du client
    - **prenom** : Prénom du client
    - **email** : Adresse email unique
    - **telephone** : Numéro de téléphone
    - **adresse** : Adresse complète
    
    **Retour** :
    - Code 201 : Client créé avec succès
    - Code 409 : Email déjà utilisé par un autre client
    
    L'email doit être unique dans le système.
    """
    try:
        return create_client(db,client)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/",
            response_model=list[ClientExpediteurRead],
            summary="Lister tous les clients expéditeurs",
            description="Récupère la liste complète de tous les clients expéditeurs enregistrés")
def get_client_route(db:Session = Depends(get_db)):
    """
    Récupère tous les clients expéditeurs.
    
    **Retour** :
    - Liste de tous les clients avec leurs informations complètes
    - Liste vide si aucun client n'est enregistré
    """
    return get_clients(db)


@router.get("/{client_id}",
            response_model=ClientExpediteurRead,
            summary="Récupérer un client par son ID",
            description="Récupère les détails complets d'un client expéditeur spécifique")
def get_client_by_id_route(client_id: int, db: Session = Depends(get_db)):
    """
    Récupère un client expéditeur spécifique par son identifiant.
    
    **Paramètres** :
    - **client_id** : Identifiant unique du client
    
    **Retour** :
    - Code 200 : Détails du client
    - Code 404 : Client non trouvé
    """
    client = get_clients_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}",
            response_model=ClientExpediteurRead,
            summary="Mettre à jour un client",
            description="Modifie les informations d'un client expéditeur existant")
def update_client_route(client_id: int, client_update: ClientExpediteurUpdate, db: Session = Depends(get_db)):
    """
    Met à jour les informations d'un client expéditeur.
    
    **Paramètres** :
    - **client_id** : Identifiant unique du client
    
    **Champs modifiables** :
    - nom, prenom, email, telephone, adresse
    - Seuls les champs fournis seront modifiés
    
    **Retour** :
    - Code 200 : Client mis à jour
    - Code 404 : Client non trouvé
    
    L'action est enregistrée dans les logs système.
    """
    client = update_client(db, client_id, client_update)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.delete("/{client_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Supprimer un client",
               description="Supprime définitivement un client expéditeur du système")
def delete_client_route(client_id: int, db: Session = Depends(get_db)):
    """
    Supprime un client expéditeur du système.
    
    **Paramètres** :
    - **client_id** : Identifiant unique du client à supprimer
    
    **Retour** :
    - Code 204 : Client supprimé avec succès
    - Code 404 : Client non trouvé
    
    Attention : Cette opération est irréversible.
    La suppression est enregistrée dans les logs système.
    """
    client = delete_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return None