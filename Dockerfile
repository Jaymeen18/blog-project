FROM python:3.8.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

RUN apt-get update -y
RUN apt-get install -y gcc musl-dev python3 python3-dev python3-pip \
        	libssl-dev libffi-dev libpq-dev build-essential

WORKDIR /code

COPY requirements.txt .
RUN pip install django_crontab

RUN python -m pip install --upgrade pip && python -m pip install --upgrade setuptools wheel

RUN pip install -r requirements.txt

COPY . .	

EXPOSE 8000

CMD ["python3","manage.py","runserver","0.0.0.0:8000"]