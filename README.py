# Critical_blox_backend

## Installation

### Projet git
```
git clone git@github.com:CriticalBlox/Backend
```

### Backend
```
python -m venv .venv
```
Sur Linux :
```
#
source .venv/bin/activate
pip install -r requirements.txt
```

## Build image
```
docker compose build
```
### Lancer backend
```
docker compose up
```

### fichier .env exemple a complété
```
#database
DATABASE_URL=postgresql+psycopg2://
DB_ECHO=True

#postgres
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

#JWT
SECRET_KEY=""
ALGORITHM=""
ACCESS_TOKEN_EXPIRE_MINUTES=

#X-api-key

API_KEY=

```
## Lancer les tests

```
docker compose exec app python -m pytest tests/ -v
```
