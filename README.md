# Fast API Studies

Projects to study Fast API, a Python framework for building fast and well documented APIs :rocket:

## :key: Requirements

- [Python](https://www.python.org/downloads/)
- [Pyenv](https://github.com/pyenv/pyenv) 
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Fast API](https://fastapi.tiangolo.com/tutorial/)

## :open_file_folder: Projects

### `fast-api-starting-api`

Simple API to run Fast API.

### `fast-api-learning-api`

Simple API to apply basic concepts of Fast API.

### `fast-api-sqlalchemy-api`

API to manage courses using SQLAlchemy as database along with Fast API resources.

The database is PostgreSQL by Docker and Docker Compose to make local development easier :smiley:

The tables are defined at `create_tables.py` and to create you'll need to run

```bash
# If Makefile exists and command is defined
make create-tables
```
or 
```bash
python create_tables.py
```

## Local running

- Is important to set the Python version defined at `.python-version` using Pyenv.
- Install the dependencies in the *Virtual Env* shell using pip.
- Some resources may not work depending on Python and modules versions defined at `requirements.txt` file

When it's all set up, run:

```bash
# If Makefile exists and command is defined
make run
```
or 

```bash
python main.py
```



---
Made with :heart: by RafaelEmery for studies.
