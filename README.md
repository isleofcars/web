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

## TODO:
- [ ] **Speed up the db**
- [ ] Make beautiful details design
- [ ] Fix the essential bugs
- [ ] Check wisited ads - ???
- [ ] Make the default location + Any distance by default (add this point right next to 500 mi)
- [ ] Add AdSense advertisement
- [ ] 
- [ ] 
- [ ]
- [x] Create the website
