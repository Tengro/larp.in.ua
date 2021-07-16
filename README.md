# larp_in_ua

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### List of services: ###

* Dev server: [https://larp.in.ua/](https://larp.in.ua/)

### Documentation: ###

* [Architecture overview](docs/architecture_overview.md)
* [Backend: Routine tasks](docs/commands.md)
* [Backend: Pre-commit hook](docs/pre_commit_hook.md)

### API documentation: ###

* ReDoc web UI: [https://larp.in.ua/_platform/docs/v1/redoc/](https://larp.in.ua/_platform/docs/v1/redoc/)
* Swagger web UI: [https://larp.in.ua/_platform/docs/v1/swagger/](https://larp.in.ua/_platform/docs/v1/swagger/)
* Swagger JSON: [https://larp.in.ua/_platform/docs/v1/swagger.json](https://larp.in.ua/_platform/docs/v1/swagger.json)
* Swagger YAML: [https://larp.in.ua/_platform/docs/v1/swagger.yaml](https://larp.in.ua/_platform/docs/v1/swagger.yaml)

### First run: ###

Install Python 3.8.6 & setup virtual environment. We recommend to use [pyenv](https://github.com/pyenv/pyenv) & [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv):

```bash
pyenv install 3.8.6
pyenv virtualenv 3.8.6 larp_in_ua
pyenv activate larp_in_ua
```

Update `pip` & `setuptools`, install `fabric`, `invoke` & `pip-tools`:

```bash
pip install -U fabric invoke pip pip-tools setuptools
```

Install Python requirements:

```bash
fab pip.sync
```

Copy initial settings for Django project:

```bash
cp ./api/.env.example ./api/.env
```

Generate `SECRET_KEY`:

```bash
./api/manage.py generate_secret_key
```

and write it to `./api/.env`:

```
LARP_IN_UA_SECRET_KEY=<your-generated-key>
```

Run backing services (require Docker):

```bash
fab compose.up -d
```

Run migrations:

```bash
./api/manage.py migrate
```

Run Django server:

```bash
fab run
```
