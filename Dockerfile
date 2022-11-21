FROM python:3.8-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /usr/src/app/requirements.txt

RUN apt-get update
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . /usr/src/app/

CMD ["gunicorn", "unicat.wsgi", "-b", ":8000"]