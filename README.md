# Explainability Techniques

A simple (and work-in-progress) Django app for interacting with a database of XAI techniques. 

## Quickstart

### Clone repository

```shell
git clone && cd TEA-XAI-DEMO
```

### Populate `.env` file

- Create a `.env` file in the root directory and ensure the following environment variables are set

```.env
# PostgreSQL settings
DB_USER=username
DB_PASSWORD=password
DB_HOST=localhost
DB_NAME=xai-techniques
DB_PORT=5432 # change if necessary in case of port conflicts
```

### Install Python dependancies and activate the virtual environment

> [!WARNING]  
> This repository contains a `pyproject.toml` file, created using [Poetry](https://python-poetry.org/docs/#installation) to manage virtual environments and packages. Instructions for poetry are below, but will need to be modified if using alternatives, such as conda or pyvenv.

```shell
poetry install
poetry shell
```

### Setup postgres database

1. Ensur environment variables are set (see above)
2. Create docker container using `docker compose up -d`
3. Test to ensure the container is running correctly using `docker ps`
4. Run `python md_to_db/sql_upload.py` to create the necessary tables and populate the database

### Run Django server

Once the virtual environment, packages, container, and database are created/running, you can start the Django web server.

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

You can then navigate to the API in a browser (or using an app, such as Postman): http://localhost:8000/api/.

## To DO

- [ ] Review DB scheme to ensure integrity and completeness 
- [ ] Update API endpoints to provide greater interactivity
- [ ] Build views and HTML templates for better navigation
- [ ] Integrate into TEA platform