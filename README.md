# REST Scraper
A real estate scraper with a REST API built with Python and [FastAPI](https://fastapi.tiangolo.com/)

## Installation
First copy the `.env.example` file to `.env` and fill in the required values.

This application is built with docker and docker-compose. To run the application, you need to have docker and docker-compose installed on your machine. If you don't have them installed, you can follow the instructions [here](https://docs.docker.com/get-docker/) and [here](https://docs.docker.com/compose/install/).

After installing docker and docker-compose, you can clone this repository and run the following command in the root directory of the project:

Starting the application:
```bash
docker compose up -d
```

For rebuilding the images:
```bash
docker compose up -d --build
```

For stopping the application:
```bash
docker compose down
```

(Note: You can also use `docker-compose` instead of `docker compose`)

## Usage
After starting the application, you can access the API documentation at `http://localhost:8000/docs`. The application is available at `http://localhost:80`.

### API
I recommend using [Postman](https://www.postman.com/) for testing the API. To see the available routes and route documentation, you can visit the API documentation page at `http://localhost:8000/docs`.

### Database
This application uses [PostgreSQL](https://www.postgresql.org/) as the database. The database is available on port `5432`. The database name, the username and password are the same as the ones in the `.env` file.

For accessing the database, you can use [pgAdmin](https://www.pgadmin.org/). You can access the pgAdmin dashboard at `http://localhost:5050`. The username and password are the same as the ones in the `.env` file.

(Note: For now the pgAdmin dashboard will reset everytime you use `docker compose up -d` so you will need to re-add the server everytime.)

### Migration
This application uses [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations. To create a new migration, you can run the following command:
```bash
alembic revision --autogenerate -m "{migration message}"
```
This needs to be run before creating the tables in the database, otherwise the tables won't be created and will be altered. Migrations will be based on sqlalchemy models.

To run migrations, you can run the following command:
```bash
alembic upgrade head
```
(Note: This will also be run everytime the application is started with docker compose)

## Tests
Will be added soon.

## Changelog
[CHANGELOG.md](CHANGELOG.md)

## License
Will be added soon.

## Contributing
Will be added soon.

## Authors
- [Nick (kash-j)](https://github.com/kash-j)
