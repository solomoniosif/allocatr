# allocatr

Allocatr is a personal finance management and budgeting web application built with Django. The app allows users to manage their personal finances by tracking their income, expenses, and savings goals.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Features
- User authentication and authorization
- Dashboard displaying income, expenses, and savings progress
- Categorization of income and expenses for easy tracking
- Budgeting tool to set spending goals and monitor progress
- Savings goals to help users save for future purchases or events
- Graphs and charts to visualize financial data

## Technologies Used
- Python 3.10.8
- Django 4.0,10
- Alpine JS 3.12
- htmx 1.8.6
- hyperscript 0.9.8
- Charts.js 4.2.1
- Tailwind CSS 3.2.7
- Sweetalert2 11.7.2
- Coloris 0.18.0
- PostgreSQL database
- Docker
- CapRover 1.10.1

## Basic Commands

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy allocatr

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
