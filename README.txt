multifactor_authentication
==========================

Built using cookiecutter gh:Pylons/pyramid-cookiecutter-alchemy --checkout 1.9-branch
as instructed here: https://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki2/installation.html

Getting Started
---------------

- Change directory into your newly created project.

    cd multifactor_authentication

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Configure the database.

    env/bin/initialize_multifactor_authentication_db development.ini

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini
