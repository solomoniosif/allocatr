# allocatr

:warning: Work in progress

Allocatr is a web application that helps you track your personal expenses and plan your budget. It allows you to create budgets for different categories such as groceries, rent, entertainment, etc. You can also set spending limits for each category and track your progress throughout the month. Allocatr provides you with a clear overview of your spending habits and helps you make informed decisions about your finances. It's a great tool for anyone who wants to take control of their finances and save money.

- **Expense tracking**: Allow users to track their expenses by category and date. This will help them understand where their money is going and identify areas where they can cut back.

- **Budget planning**: Allow users to create budgets for different categories such as groceries, rent, entertainment, etc. You can also set spending limits for each category and track your progress throughout the month.

- **Goal setting**: Allow users to set financial goals such as saving for a vacation or paying off debt. You can provide them with tools to help them achieve these goals such as a savings calculator or debt payoff planner.

- **Reminders**: Allow users to set reminders for upcoming bills or payments. This will help them avoid late fees and keep their finances organized.

- **Reports**: Provide users with detailed reports on their spending habits and budget progress. This will help them make informed decisions about their finances and identify areas where they can improve.

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
- [Python 3.10.8](https://www.python.org/)
- [Django 4.0.10](https://www.djangoproject.com/)
- [Alpine.js 3.12](https://alpinejs.dev/)
- [htmx 1.8.6](https://htmx.org/)
- [Tailwind CSS 3.3.1](https://tailwindcss.com/)
- Charts.js 4.2.1 | to be replaced
- [Apache Echarts 5.4.2](https://echarts.apache.org/)
- [List.js 2.3.1](https://listjs.com/)
- [Sweetalert2 11.7.2](https://sweetalert2.github.io/)
- [Coloris Color Picker 0.18.0](https://coloris.js.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [CapRover 1.10.1](https://caprover.com/)

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
