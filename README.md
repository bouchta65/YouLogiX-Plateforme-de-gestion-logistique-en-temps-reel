# YouLogiX — Plateforme de gestion logistique en temps réel

## Description

YouLogiX est une plateforme de gestion logistique en temps réel destinée à YouExpress. Elle permet de moderniser et automatiser la gestion des opérations logistiques, offrant une meilleure visibilité sur l’état des colis pour les gestionnaires, livreurs, clients expéditeurs et destinataires.

La solution est basée sur un backend moderne développé avec **FastAPI**, **SQLAlchemy**, **Pydantic**, et utilise **PostgreSQL** pour la persistance des données. Elle est conteneurisée avec **Docker** et documentée avec **Swagger**.

## Fonctionnalités

* **Gestion des utilisateurs** : Clients expéditeurs, destinataires et livreurs.
* **Gestion des colis** : Création, modification, suppression, assignation.
* **Suivi des livraisons** : Mise à jour des statuts, historique et notifications.
* **Organisation logistique** : Gestion des zones et planification des tournées.
* **Infrastructure backend** : Architecture en couches, validation Pydantic, gestion des exceptions, conteneurisation Docker.

## Stack Technique

* **Backend** : FastAPI, SQLAlchemy, Pydantic
* **Base de données** : PostgreSQL
* **Conteneurisation** : Docker, Docker Compose
* **Tests unitaires** : Pytest
* **Documentation API** : Swagger

## Structure du projet

```
youlogix-backend/
│
├── app/
│   ├── main.py                  # Point d’entrée FastAPI, 
│   ├── core/                    # Configuration & sécurité
│   ├── models/                  # Couche Modèle (DB)
│   ├── controllers/             # Couche logique métier
│   ├── routes/                  # Couche API / endpoints
│   ├── utils/                   # Helpers
│   └── exceptions.py            # Gestion centralisée des 
├── tests/                       # Tests unitaires (pytest)
│
├── alembic/                      # Migrations PostgreSQL
│   └── versions/
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── .env
├── README.md
└── .gitignore

```

## Installation

1. Cloner le dépôt :

```bash
git clone <https://github.com/bouchta65/YouLogiX-Plateforme-de-gestion-logistique-en-temps-reel>
```

2. Configurer les variables d'environnement dans un fichier `.env`.
3. Lancer l'application avec Docker Compose :

```bash
docker-compose up --build
```

4. Accéder à l'API : `http://localhost:8000/docs` (Swagger).

## Contribution

1. Fork le projet.
2. Crée une branche pour votre fonctionnalité : `git checkout -b feature/nom_fonctionnalité`
3. Commit vos modifications : `git commit -m 'Ajouter une nouvelle fonctionnalité'`
4. Push sur la branche : `git push origin feature/nom_fonctionnalité`
5. Ouvrir un Pull Request.

## Licence

Ce projet est sous li
