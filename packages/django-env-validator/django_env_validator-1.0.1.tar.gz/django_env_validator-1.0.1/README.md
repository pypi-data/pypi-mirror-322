## Project Description

Django env validator is a package used to validate the .env file in a Django project using a set schema of rules.


## Installation

The package can be installed and used in your Django app with pip:

```python
pip install django-env-validator
```

Edit your settings.py file to include ‘django_env_validator’ in the INSTALLED_APPS listing.

```python
INSTALLED_APPS = [
    ...
    'django_env_validator',
]
```

## Usage

Define the variable `ENV_VALIDATOR_RULES` in your settings.py

The current available rules are:
 - required (boolean -- is the environment variable a required one or not)
 - min_length (integer -- minimum character length of the environment variable)
 - max_length (integer -- maximum character length of the environment variable)
 - choices (list, tuple, set -- specific values the environment variable can be)

### Example:

```python
ENV_VALIDATOR_RULES = {
    "API_KEY": {
        "required": True,
        "min_length": 15,
        "max_length": 50,
    },
    "CURRENT_ENVIRONMENT": {
        "required": True,
        "choices": ["dev", "staging", "testing", "production"],
    }
}
```
