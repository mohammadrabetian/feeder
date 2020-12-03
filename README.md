# Feed scraper with asynchronous feed updates.


## Getting Started

### Prerequisites

You need to have [docker](https://docs.docker.com/install/) & [docker-compose](https://docs.docker.com/compose/install/)

### Secrets

Create a .env file inside config folder using .env.example as a template.
You need to create a secret key for Django and put it inside .env file. See config/.env.example

You can create one using django-extensions generate_secret_key command,
or you can create one [here](https://djecrety.ir/)

The other secrets like database passwords and etc have a default value just for the sake of simplicity for this project, 
but in case of using this project in production, you should consider doing as above. See config/.env.example

### Running

Just type this command on terminal and everything will be up and running

```bash
docker-compose up
```

## Debuging

Django extensions shell
```bash
docker-compose exec web ./manage.py shell_plus
```

This project is using `GraphQL` for the Apis. [Click here](graphql.md) to see what queries you can run.

## Tests

Run tests with pytest
```bash
docker-compose exec web pytest
```

## Built With

* [Django](https://www.djangoproject.com/) - For the web framework
* [Postgres](https://www.postgresql.org/) - For the database
* [GraphQL](https://graphql.org/) - For the Apis
* [Redis](https://redis.io/) - For the caching backend
* [Docker](https://www.docker.com/) - For easier deployment
