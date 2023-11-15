# bsm_server

This project was generated using fastapi_template.

## Dependecies

Create isolated environment `python -m venv env`

Activate environment `source venv/bin/activate`

Run `pip install -r requirements.txt`

After installed new dependencies run `pip freeze > requirements.txt`

## Project structure

```bash
$ tree "bsm_server"
bsm_server
├── conftest.py  # Fixtures for all tests.
├── db  # module contains db configurations
│   ├── dao  # Data Access Objects. Contains different classes to interact with database.
│   └── models  # Package contains different models for ORMs.
├── __main__.py  # Startup script. Starts uvicorn.
├── services  # Package for different external services such as rabbit or redis etc.
├── settings.py  # Main configuration settings for project.
├── static  # Static content.
├── tests  # Tests for project.
└── web  # Package contains web server. Handlers, startup config.
    ├── api  # Package with all handlers.
    │   └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variables should start with "BSM_SERVER_" prefix.

For example if you see in your "bsm_server/settings.py" a variable named like
`random_parameter`, you should provide the "BSM_SERVER_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `bsm_server.settings.Settings.Config`.

An example of .env file:

```bash
BSM_SERVER_RELOAD="True"
BSM_SERVER_PORT="8000"
BSM_SERVER_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: <https://pydantic-docs.helpmanual.io/usage/settings/>

## Pre-commit

To install pre-commit simply run inside the shell:

```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:

* black (formats your code);
* isort (sorts imports in all files);

You can read more about pre-commit here: <https://pre-commit.com/>

## Migrations

To create migrations files run `aerich migrate`

To apply migrations to database run `aerich upgrade`
