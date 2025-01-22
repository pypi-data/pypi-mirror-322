# spback (sun-praise backend) framework

[![PyPI](https://img.shields.io/pypi/v/spback.svg)](https://pypi.python.org/pypi/spback/)
[![Documentation Status](https://readthedocs.org/projects/spback/badge/?version=latest)](https://spback.readthedocs.io/en/latest/?badge=latest) [![Downloads](https://pepy.tech/badge/spback/week)](https://pepy.tech/project/spback)

This project is built on `django-ninja` and `django-ninja-extra`.

## Usage

Create your django project, start with the command: `django-admin startproject conf .`.

### Update `settings.py`

If you need to use the feature of `api`, you need to install `django-ninja-extra>=0.20.7`, `django-ninja-jwt>=5.3.1`.

Add `spback` supported apps,

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # for example, "apis",
    ...
    "ninja_extra",  # for spback
]
```

### API instance

create api instance.

```python
from spback.urls import create_api

api = create_api()
```

### JWT

If you want the JWT get authed, set the api with `JWTAuth`.

```python
from ninja_extra.router import Router
from ninja_jwt.authentication import JWTAuth

router = Router()


@router.get("/", auth=JWTAuth())
def protected_endpoint(request):
    return {"message": "This is a protected endpoint."}

```

### Error handler

register error handler

```python
from spback.handler.errors import register_error_handler

api = register_error_handler(api)
```

### Register to `urls.py`

With this code, the users could register `django-ninja` to urls.py

```python
api = create_api()
api = register_routers(api)

urlpatterns = [
    path("", api.urls),
]

```

### Register to `conf/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
```

## For Developer

Use `pdm run pip install -r requirements/dev.txt` to install dev packages.
