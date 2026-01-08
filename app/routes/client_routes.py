from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.client_controller import (create_client, update_client, delete_client, get_clients, get_clients_by_id)
from app.schemas.client_expediteur import (ClientExpediteurBase, ClientExpediteurRead, ClientExpediteurUpdate, ClientExpediteurCreate)

router = APIRouter(
    prefix="/clients",
    tags=["Clients Expéditeurs"]
)

@router.post("/",response_model=ClientExpediteurRead,status_code=status.HTTP_201_CREATED)
def create_client_route(client: ClientExpediteurCreate,db: Session = Depends(get_db)):
    return create_client(db,client)

@router.get("/",response_model=list[ClientExpediteurRead])
def get_client_route(db:Session = Depends(get_db)):
    return get_clients(db)


@router.get("/{client_id}", response_model=ClientExpediteurRead)
def get_client_by_id_route(client_id: int, db: Session = Depends(get_db)):
    client = get_clients_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=ClientExpediteurRead)
def update_client_route(client_id: int, client_update: ClientExpediteurUpdate, db: Session = Depends(get_db)):
    client = update_client(db, client_id, client_update)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client_route(client_id: int, db: Session = Depends(get_db)):
    client = delete_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return None