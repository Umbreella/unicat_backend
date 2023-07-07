# Online academy "Unicat" (Web API)

![python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![django](https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white)
![drf](https://img.shields.io/badge/django_rest_framework-A30000?style=for-the-badge&logo=django&logoColor=white)
![celery](https://img.shields.io/badge/celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![graphql](https://img.shields.io/badge/graphql-E10098?style=for-the-badge&logo=graphql&logoColor=white)
![docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

### Testing

![unittest](https://img.shields.io/badge/unittest-092E20?style=for-the-badge&logo=pytest&logoColor=white)
![codecov](https://img.shields.io/codecov/c/github/Umbreella/unicat_backend?style=for-the-badge&logo=codecov)

## Description

A web API that implements the work of the online academy. The work with the
following information was developed:

* teachers
* courses
* lessons
* news
* events
* reviews
* access restriction

## Getting Started

### Dependencies

![redis](https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![postgresql](https://img.shields.io/badge/postgresql_(patroni)-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![prometheus](https://img.shields.io/badge/prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![grafana](https://img.shields.io/badge/grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)

### Environment variables

* To run the application, you have to perform one of the options:
    * specify the **environment variables**
    * overwrite **.env** file
* The list of all environment variables is specified in the **[.env](.env)**

### Docker

* docker-compose.yml

```docker
version: "3"

services:
  unicat_backend:
    image: umbreella/unicat_backend:latest
    ports:
      - [your_open_port]:8000
    env_file:
      - [path_to_env_file]
    volumes:
      - [path_to_static_folder]:/usr/src/app/static/
      - [path_to_media_folder]:/usr/src/app/media/
```

* Docker-compose run

```commandline
docker-compose up -d
```

* Open bash in container

```commandline
docker exec --it unicat_backend bash
```

* Run commands

```commandline
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

### Celery and Flower

* Add in docker-compose for run **Celery**

```docker
command: celery -A unicat.celery.app worker
```

* Add in docker-compose for run **Flower**

```docker
command: celery -A unicat.celery.app flower
```

## Endpoints

### Main

* REST docs

```swagger codegen
[your_ip_address]/api/docs/
```

* GraphQL docs

```swagger codegen
[your_ip_address]/graphql/docs/
```

### Auxiliary

* Django admin

```swagger codegen
[your_ip_address]/api/admin/
```

* Prometheus data

```swagger codegen
[your_ip_address]/prometheus/
```
