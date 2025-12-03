# ECAA09 e-Oficina
Gestor de oficinas credenciadas e clientes.

Baseado no projeto:
[Get Started With Django: Build a Portfolio App](https://realpython.com/get-started-with-django-1/)

## Cria projeto base Django

```sh
pip install django
mkdir e-oficina
e-oficina/django-admin startproject principal .
```

## Cria aplicações do projeto

```sh
e-oficina/python manage.py startapp paginas
e-oficina/python manage.py startapp banco
```

### principal/settings.py

```python
INSTALLED_APPS = [
    'paginas.apps.PaginasConfig', # Páginas
    'banco.apps.BancoConfig', # Banco de dados
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# ...

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates', # diretorio do arquivo base.html
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```


## Monta banco de dados após modelo definido no app banco

```sh
e-oficina/python manage.py makemigrations banco
e-oficina/python manage.py migrate banco
```

## Carregar imagens para banco de dados

```sh
e-oficina/python manage.py carregar_imagens
```