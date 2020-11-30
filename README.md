# Feed scraper with asynchronous feed updates.


## Getting Started

### Prerequisites

You need to have [docker](https://docs.docker.com/install/) & [docker-compose](https://docs.docker.com/compose/install/)

## Debuging

Django extensions shell
```bash
docker-compose exec web ./manage.py shell_plus
```

### Running

Just type this command on terminal and everything will be up and running

```bash
docker-compose up
```

This project is using `GraphQL` for the Apis. [Click here](graphql.md) to see what queries you can run.


## Built With

* [Django](https://www.djangoproject.com/) - For the web framework
* [Postgres](https://www.postgresql.org/) - For the database
* [GraphQL](https://graphql.org/) - For the Apis
* [Redis](https://redis.io/) - For the caching backend
* [Docker](https://www.docker.com/) - For easier deployment