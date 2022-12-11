# Isle of Cars: WEB

## Installation

Supposed to work on the *nix machine.


###### 1. Run these commands to run a server:

```bash
cd isleofcars
python3 -m venv env
source env/bin/activate
pip install -r isleofcars/requirements.txt
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

The website will be available on http://localhost:8000

## Troubleshooting

If there is no space left on the device run these commands
```bash
docker system prune
docker volume rm $(docker volume ls -qf dangling=true)
```

## TODO:

- [x] Change the domain to isleofcars.com
- [ ] Move frontend to django templates (no vue.js)
- [ ] Add reporting app (admin?)
  - [ ] просмотр логов сайта и парсеров
- [x] Личный кабинет с возможностью добавлять объявления
- [ ] Add test environment (test db + test.isleofcars.com domain)
- [ ] Develop style rules
- [ ] Implement images preview
- [ ] Show number of cars found in the header
- [ ] Add login via google account
- [ ] Add email verification on registration
- [ ] Разработка мобильного приложения android/iphone
- [ ] Setup SEO
