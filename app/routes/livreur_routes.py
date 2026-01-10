from fastapi import APIRouter, HTTPException, Depends, status
from app.controllers.livreur_controller import (create_livreur, update_livreur, delete_livreur, get_livreur_by_id, get_livreurs)
from app.controllers.colis_controller import get_colis_by_livreur
from app.schemas.livreur import (LivreurBase, LivreurRead, LivreurCreate, LivreurUpdate)
from app.schemas.colis import ColisRead
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/livreurs",
    tags=["Livreurs"]
)



@router.post("/", response_model=LivreurRead, status_code=status.HTTP_201_CREATED)
def create_livreur_route(livreur: LivreurCreate, db: Session = Depends(get_db)):
    return create_livreur(db, livreur)



@router.get("/", response_model=list[LivreurRead])
def get_livreurs_route(db: Session = Depends(get_db)):
    return get_livreurs(db)


@router.get("/{livreur_id}", response_model=LivreurRead)
def get_livreur_by_id_route(livreur_id: int, db: Session = Depends(get_db)):
    livreur = get_livreur_by_id(db, livreur_id)
    if not livreur:
        raise HTTPException(status_code=404, detail="Livreur not found")
    return livreur



@router.get("/{livreur_id}/colis", response_model=list[ColisRead],
            summary="Récupérer tous les colis d'un livreur",
            description="Liste tous les colis assignés à un livreur spécifique")
def get_livreur_colis_route(livreur_id: int, db: Session = Depends(get_db)):
    """
    Récupère tous les colis assignés à un livreur.
    
    - **livreur_id**: L'identifiant unique du livreur
    
    Retourne une liste vide si le livreur n'a pas de colis assignés.
    Retourne une erreur 404 si le livreur n'existe pas.
    """
    # Verify livreur exists
    livreur = get_livreur_by_id(db, livreur_id)
    if not livreur:
        raise HTTPException(status_code=404, detail="Livreur not found")
    
    return get_colis_by_livreur(db, livreur_id)




@router.put("/{livreur_id}", response_model=LivreurRead)
def update_livreur_route(livreur_id: int, livreur_update: LivreurUpdate, db: Session = Depends(get_db)):
    livreur = update_livreur(db, livreur_id, livreur_update)
    if not livreur:
        raise HTTPException(status_code=404, detail="Livreur not found")
    return livreur




@router.delete("/{livreur_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_livreur_route(livreur_id: int, db: Session = Depends(get_db)):
    livreur = delete_livreur(db, livreur_id)
    if not livreur:
        raise HTTPException(status_code=404, detail="Livreur not found")
    return None