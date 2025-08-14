# Requirements

- Python 3.13
- Poetry
- MariaDB/MySQL

# Setup

1. Clone the repository
2. Run `poetry install --with dev` to install the development dependencies
3. Activate the poetry environment
4. Configure a .env file by copying the sample.env file and filling in the values
5. In your terminal emulator run
   - `poetry run python klass/manage.py makemigrations` to create the database migrations
   - `poetry run python klass/manage.py migrate` to create the database
   - `poetry run python klass/manage.py createsuperuser` to create a superuser
   - `poetry run python klass/manage.py runserver` to start the development server
6. Setup your IDE to use mypy as your linter and checker.
   You need to set your `PYTHONPATH` env to `./src:$PYTHONPATH` otherwise mypy won't work.

# Tests

We are using the builtin unittest module for testing, according to the official django docs.
You can run the tests by running `poetry run python klass/manage.py test` in your terminal.
