FROM python:3.8.10

WORKDIR /usr/src/app


RUN pip install --upgrade pip
RUN pip install virtualenv
RUN python3 -m venv env
RUN /bin/bash -c "source env/bin/activate"
COPY ./requirements.txt /usr/src/app 
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir ./logs
RUN chmod 777 ./logs

COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
