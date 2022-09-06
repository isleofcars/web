# Isle of Cars: WEB

## Installation

Supposed to work on the *nix machine.



###### 1. Run these commands for build back-end:
```bash
cd backend
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
> Notes:
> 1. If you are using linux, you need to install several packages for `mysqlclient` before running this command.
> ```bash
> sudo apt install python3-dev build-essential libssl1.1 libssl1.1=1.1.1f-1ubuntu2 libssl-dev libmysqlclient-dev
> ```
> 2. Before creating migrations(_or just before starting the project_) , make sure you have a `logs` folder in the `backend`


###### 2. In another session run these commands for build front-end:
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
