# WholeCarsMarket: WEB

## Installation

Supposed to work on the *nix machine.

1. Run these commands:
```bash
cd backend
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
2. In another session run these commands:
```bash
cd frontend
npm i
npm run serve
```
The website will be available on http://localhost:8080

## Troubleshooting

If there is no space left on the device run these commands
```bash
docker system prune
docker volume rm $(docker volume ls -qf dangling=true)
```
