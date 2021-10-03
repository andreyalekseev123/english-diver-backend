from invoke import task

from . import docker, start, system
from .common import print_green


@task
def manage(context, command):
    """Run ``manage.py`` command

    docker-compose run --rm web python3 manage.py <command>
    """
    return start.run_python(context, " ".join(["manage.py", command]))


@task
def makemigrations(context):
    """Run makemigrations command and chown created migrations
    """
    print_green("Django: Make migrations")
    manage(context, "makemigrations")
    migrate(context)
    if not start.is_local_python:
        system.chown(context)


@task
def migrate(context):
    """Run ``migrate`` command"""
    print_green("Django: Apply migrations")
    manage(context, "migrate")


@task
def resetdb(context):
    """Reset database to initial state (including test DB)"""
    print_green("Reset database to its initial state")
    manage(context, "drop_test_database --noinput")
    manage(context, "reset_db -c --noinput")
    makemigrations(context)
    migrate(context)
    createsuperuser(context)
    set_default_site(context)


def createsuperuser(context):
    """Create superuser
    """
    print_green("Create superuser")
    manage(context, "createsuperuser")


@task
def run(context):
    """Run development web-server"""

    # start dependencies (so even in local mode this command
    # is working successfully
    # if you need more default services to be started define them
    # below, like celery, etc.
    docker.startdb(context)
    print_green("Running web app")
    manage(
        context,
        "runserver 0.0.0.0:8000"
    )


@task
def shell(context, params=None):
    """Shortcut for manage.py shell_plus command

    Additional params available here:
        http://django-extensions.readthedocs.io/en/latest/shell_plus.html
    """
    print_green("Entering Django Shell")
    manage(context, "shell_plus --ipython {}".format(params or ""))


def set_default_site(context):
    """Set default site to localhost

    Set default site domain to `localhost:8000` so `get_absolute_url`
    works correctly in local environment
    """
    manage(
        context,
        "set_default_site --name localhost:8000 --domain localhost:8000"
    )
