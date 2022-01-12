# WholeCarsMarket: WEB

## Installation

Supposed to work on a *nix machine. `git clone` the repository and then run these commands:

```bash
cd backend
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt  # 1 note
python3 manage.py runserver
```
> Notes:
> 1. If you are using linux, you need to install several packages for `mysqlclient` before running this command.
> ```bash
> sudo apt install python3-dev build-essential libssl1.1 libssl1.1=1.1.1f-1ubuntu2 libssl-dev libmysqlclient-dev
> ```

The website will be available on http://localhost:8080

## Troubleshooting

If there is no space left on the device run these commands
```bash
docker system prune
docker volume rm $(docker volume ls -qf dangling=true)
```
